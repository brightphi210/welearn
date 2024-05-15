from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import APIView
from .models import User
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.conf import settings




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
    


class ClassListCreateAPIView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# {
#   "email" : "pbright103@gmail.com"
# }

# ================ FORGET PASSWORD ===================

import random
from django.core.mail import send_mail

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            reset_code = random.randint(1000, 9999)
            PasswordReset.objects.create(user=user, reset_code=reset_code)

            subject = 'Confirm your email'
            message = f'This is your code: {reset_code}'
            from_email = 'smtp.gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)


            return Response({"message": "Reset code sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        reset_code = request.data.get('reset_code')
        password = request.data.get('password')
        
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        password_reset = PasswordReset.objects.filter(user=user, reset_code=reset_code).first()
        if not password_reset:
            return Response({"error": "Invalid reset code."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        password_reset.delete()
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
