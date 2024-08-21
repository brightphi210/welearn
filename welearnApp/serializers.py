from .models import *
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


import random

def generate_otp():
    otp = ''.join([str(random.randint(0, 30)) for _ in range(4)])
    return otp


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        profile = InstructorProfile.objects.get(user=user)
        token['profile_id'] = profile.id
        return token    


# ================ CREATING OF USER ===================
class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'user_type']
        depth = 1
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.otp = generate_otp()  
        user.set_password(password)
        user.save()
        return user
    

# ==================== VERIFY USER SERIALIZER =======================
class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('Invalid email address')
        if user.is_active or not user.otp == otp:
            raise serializers.ValidationError('Invalid OTP code')
        return attrs

    def update(self, instance, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.is_active = True
        user.otp = ''
        user.save()
        return user
    


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        depth = 1




# Remarks
class InstructorRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorRemark
        fields = '__all__'
        # depth = 1


class StudentRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRemark
        fields = '__all__'
        # depth = 1



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        depth = 2

# ================ INSTRUCTIOR ======================
class InstructorSerializer(ModelSerializer):
    
    classes = ClassSerializer(many=True)
    instructorRemark = InstructorRemarkSerializer(many=True)
    
    
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        depth = 1

# ===================== STUDENT ========================
class StudentSerializer(ModelSerializer):
    
    hiredInstructors = BookingSerializer(many=True)
    studentRemark = StudentRemarkSerializer(many=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        depth = 1


    
# ================= FORGET PASSWORD AND RESET PASSWORD ============

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
        
        
# change Password
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    
