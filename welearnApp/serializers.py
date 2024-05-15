from .models import *
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers


import random

def generate_otp():
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return otp


# ================ CREATING OF USER ===================
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'user_type']

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
    


# ================ INSTRUCTIOR ======================
class InstructorSerializer(ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        depth = 1



# ===================== STUDENT ========================
class StudentSerializer(ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'



class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
    
# ================= FORGET PASSWORD AND RESET PASSWORD ============

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'
