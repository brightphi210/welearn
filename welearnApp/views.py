from django.shortcuts import render
from rest_framework import generics, status,permissions
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import APIView
from .serializers import VerifyUserSerializer
from .models import User
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import pyotp




# Create your views here.


# # ================= USER CREATE ========================
# class UserGetCreate(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

    # def create(self, request, *args, **kwargs):

    #     # Check if a user with the given email already exists
    #     email = request.data.get('email', None)
    #     if email and User.objects.filter(email=email).exists():

    #         return Response(
    #             {'message': 'User with this email already exists'}, 
    #             status=400
    #         )

    #     response = super().create(request, *args, **kwargs)

    #     # Check if the creation was successful
    #     if response.status_code == status.HTTP_201_CREATED:
    #         return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    #     else:
    #         # Registration failed, customize the error message
    #         error_message = {'message': 'User registration failed. Please check the provided data.'}
    #         response.data = error_message
    #         return response


class UserGetCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            print("True")
            base32secret3232 = pyotp.random_base32()
            otp = pyotp.TOTP(base32secret3232, interval=1000, digits=6)
            time_otp = otp.now()
            user_type = serializer.validated_data.get('user_type')
            otp_secret = base32secret3232
            user = serializer.save(otp=time_otp, user_type=user_type, otp_secret=otp_secret)
            user.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'User registration failed. Please check the provided data.'}, status=status.HTTP_400_BAD_REQUEST)
     



# ============ ACCOUNT VERIFICATION VIA OTP =============
# class ActivateAccountView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         otp = request.data.get('otp')

#         try:
#             user = User.objects.get(email=email)
#             if user.otp == otp and not user.is_active:
#                 user.is_active = True
#                 user.otp = ''  # Clear OTP after successful activation
#                 user.save()
#                 return Response({'message': 'Account activated successfully!'})
#             else:
#                 return Response({'message': 'Invalid OTP or account already activated'}, status=400)
#         except User.DoesNotExist:
#             return Response({'message': 'User with this email not found'}, status=404)


class ActivateAccountView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyUserSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        print(otp)
        try:
            user = User.objects.get(email=email, otp=otp)
            print(user)
        except:
            data = {'message': "User Does not exists"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        if  pyotp.TOTP(user.otp_secret, interval=1000, digits=6).verify(otp):
            user.is_active = True
            user.save()
            data = {
                'user': user.email
            }
            return Response(data=data, status=status.HTTP_200_OK)
            # return redirect('http://localhost:8000/api/token')
            
        else:
            data = {'message': "Token has Expired"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        



class UserGetUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


# ============== GET INSTRUCTORS PROFILE =================

class InstructorProfileGet(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer




# =============GET UPDATE, DELETE INSTRUCTORS PROFILE ===========
class InstructorProfileUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer
    lookup_field = 'pk'

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)
    

# ============== GET STUDENTS PROFILE =================
class StudentProfileGet(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentSerializer

# =============GET UPDATE, DELETE INSTRUCTORS PROFILE ===========
class StudentProfileUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'pk'

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)
    


# ============== CREATING CLASS =======================
class ClassListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'Class created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Creation failed, customize the error message
            error_message = {'message': 'Class creation failed😒😒'}
            response.data = error_message
            return response


# =============GET UPDATE, DELETE INSTRUCTORS PROFILE ===========
class ClassUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'pk'

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)


# =============== BOOKING CLASS =====================
class BookingListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()

    # Define both serializers
    serializer_class_get = BookingSerializerGet
    serializer_class_post = BookingSerializerPost

    # Override get_serializer_class to choose the serializer based on the request method
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.serializer_class_post
        return self.serializer_class_get

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'Booking successful'}, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Booking creation failed'}, status=status.HTTP_400_BAD_REQUEST)



# =============GET UPDATE, DELETE INSTRUCTORS PROFILE ===========
class BookingUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializerGet
    lookup_field = 'pk'

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'Reviewed successful'}, status=status.HTTP_201_CREATED)
        else:
            # Creation failed, customize the error message
            error_message = {'message': 'Review creation failed😒😒'}
            response.data = error_message
            return response

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



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(new_password)
            self.object.save()
            return Response({"detail": "Password changed successfully."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InstructorRemarkCreateView(generics.ListCreateAPIView):
    serializer_class = InstructorRemarkSerializer
    queryset = InstructorRemark.objects.all()
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'Remark successful'}, status=status.HTTP_201_CREATED)
        else:
            # Creation failed, customize the error message
            error_message = {'message': 'Remark creation failed😒😒'}
            response.data = error_message
            return response


class StudentRemarkCreateView(generics.ListCreateAPIView):
    serializer_class = StudentRemarkSerializer
    queryset = StudentRemark.objects.all()
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'Remark successful'}, status=status.HTTP_201_CREATED)
        else:
            # Creation failed, customize the error message
            error_message = {'message': 'Remark creation failed😒😒'}
            response.data = error_message
            return response


class PaymentSuccessView(generics.ListCreateAPIView):
    serializer_class = PaymentSuccessSerializer
    queryset = PaymentSuccess.objects.all()
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'Payement Successfull'}, status=status.HTTP_201_CREATED)
        else:
            # Creation failed, customize the error message
            error_message = {'message': 'Payment failed😒😒'}
            response.data = error_message
            return response
        


class DeleteAccountView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




class AdminSeeView(generics.ListAPIView):
    serializer_class = AdminSeeRemarkSerializer
    queryset = AdminSeeRemarks.objects.all()
