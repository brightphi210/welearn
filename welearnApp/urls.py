from django.urls import path
from .views import *

urlpatterns = [

    # ================= USER CREATE ========================
    path('user/',UserGetCreate.as_view(), name='user'),
    path('user/update/<str:pk>/',UserGetUpdateDelete.as_view(), name='user'),

    # ================= ACCOUNT OTP ========================
    path('account-otp/', ActivateAccountView.as_view(), name='otp'),

    # ================= PROFILES ========================
    path('instructor-profiles/', InstructorProfileGet.as_view(), name='instructor'),
    path('instructor-profiles/update/<str:pk>/', InstructorProfileUpdateDelete.as_view(), name='instructor'),
    
    path('student-profiles/', StudentProfileGet.as_view(), name='student'),
    path('student-profiles/update/<str:pk>/', StudentProfileUpdateDelete.as_view(), name='student'),

    # ================ Forget Password ==================
    path('password-forgot/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('password-reset/', ResetPasswordView.as_view(), name='reset_password'),

    path('classes/', ClassListCreateAPIView.as_view(), name='class-list-create'),
    path('classes/update/<str:pk>/', ClassUpdateDelete.as_view(), name='class-update-delete'),


    path('class-bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('class-bookings/update/<str:pk>/', BookingUpdateDelete.as_view(), name='booking-update-delete'),


    path('reviews/', ReviewListCreateAPIView.as_view(), name='reviews'),

    # ============= CHANGE PASSWORD ====================
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    path('instructor-remarks/', InstructorRemarkCreateView.as_view(), name='remark-list-create'),
    path('student-remarks/', StudentRemarkCreateView.as_view(), name='remark-list-create'),
]