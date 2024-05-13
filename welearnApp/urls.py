from django.urls import path
from .views import *

urlpatterns = [

    # ================= USER CREATE ========================
    path('user/',UserGetCreate.as_view(), name='user'),


    # ================= ACCOUNT OTP ========================
    path('account-otp/', ActivateAccountView.as_view(), name='otp'),

    # ================= PROFILES ========================
    path('instructor-profiles/', InstructorProfileGet.as_view(), name='instructor'),
    path('instructor-profiles/update/<str:pk>/', InstructorProfileUpdateDelete.as_view(), name='instructor'),
    
    path('student-profiles/', StudentProfileGet.as_view(), name='student'),
    path('student-profiles/update/<str:pk>/', StudentProfileUpdateDelete.as_view(), name='student'),
]