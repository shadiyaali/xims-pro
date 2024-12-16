import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework import generics
from rest_framework.exceptions import NotFound

logger = logging.getLogger(__name__)

class AdminLoginView(APIView):
    def post(self, request, *args, **kwargs):
        print("request",request.data)
        email = request.data.get('email')
        password = request.data.get('password')

        logger.info(f"Attempting to login user with email: {email}")

        if email is None or password is None:
            return Response({'error': 'Email and password must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_staff and user.is_superuser:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        logger.warning(f"Failed login attempt for user: {email}")
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


 

 

class CreateCompanyView(APIView):
    def post(self, request, *args, **kwargs):
        print("Request data: %s", request.data)
        serializer = CompanySerializer(data=request.data)
        
        if serializer.is_valid():
            company = serializer.save()
            return Response({
                "message": "Company created successfully!",
                "company_id": company.id
            }, status=status.HTTP_201_CREATED)
        else:
            print("serializer.errors", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyGetSerializer

class CompanyUpdateView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer

    def get_object(self):
        company_id = self.kwargs['id']
        return generics.get_object_or_404(Company, id=company_id)

    def perform_update(self, serializer):
     
        print("Request Data:", self.request.data)
        
 
        serializer.save()

    def update(self, request, *args, **kwargs):
      
        print("Incoming request data:", request.data)
        return super().update(request, *args, **kwargs)


class ChangeCompanyStatusView(APIView):

    def post(self, request, id):
        try:
            company = Company.objects.get(id=id)
        except Company.DoesNotExist:
            raise NotFound("Company not found")

        action = request.data.get('action')   
        
        if action == 'block':
            company.status = 'blocked'
            company.save()
            return Response({"message": "Company has been blocked successfully."}, status=status.HTTP_200_OK)
        
        elif action == 'active':
            company.status = 'active'
            company.save()
            return Response({"message": "Company has been unblocked successfully."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid action. Use 'block' or 'unblock'."}, status=status.HTTP_400_BAD_REQUEST)
    


class DeleteCompanyView(APIView):
   def delete(self, request,  id):
        try:
            company = Company.objects.get(id= id)
        except Company.DoesNotExist:      
            raise NotFound("Company not found") 
        company.delete()
        return Response({"message": "Company has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class PermissionListView(APIView):
    def get(self, request, *args, **kwargs):
        print("request.data",request.data)
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SingleCompanyListView(generics.ListAPIView):
    serializer_class = CompanySingleSerializer

    def get_queryset(self):
      
        company_id = self.kwargs['id']
       
        try:
            company = Company.objects.get(id=company_id)
            return Company.objects.filter(id=company.id) 
        except Company.DoesNotExist:
            raise NotFound(detail="Company with the given id does not exist")
        
class CompanyCountView(APIView):
  
    def get(self, request, *args, **kwargs):
        company_count = Company.objects.count()
        return Response({"count": company_count}, status=status.HTTP_200_OK)