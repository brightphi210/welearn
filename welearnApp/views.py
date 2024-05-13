from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import APIView
from .models import User
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated



# Create your views here.


# ================= USER CREATE ========================
class UserGetCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):


        # Check if a user with the given email already exists
        email = request.data.get('email', None)
        if email and User.objects.filter(email=email).exists():

            return Response(
                {'message': 'User with this email already exists'}, 
                status=400
            )

        response = super().create(request, *args, **kwargs)

        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Registration failed, customize the error message
            error_message = {'message': 'User registration failed. Please check the provided data.'}
            response.data = error_message
            return response



# ============ ACCOUNT VERIFICATION VIA OTP =============
class ActivateAccountView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            if user.otp == otp and not user.is_active:
                user.is_active = True
                user.save()
                return Response({'message': 'Account activated successfully!'})
            else:
                return Response({'message': 'Invalid OTP or account already activated'}, status=400)
        except User.DoesNotExist:
            return Response({'message': 'User with this email not found'}, status=404)
        


# ============== GET INSTRUCTORS PROFILE =================

class InstructorProfileGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer




# =============GET UPDATE, DELETE INSTRUCTORS PROFILE ===========
class InstructorProfileUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer
    lookup_field = 'pk'

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)
    

# ============== GET STUDENTS PROFILE =================
class StudentProfileGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentSerializer

# =============GET UPDATE, DELETE INSTRUCTORS PROFILE ===========
class StudentProfileUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'pk'

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)