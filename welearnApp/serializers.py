from .models import *
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        token['user_type'] = user.user_type

        # Try to get InstructorProfile first
        try:
            profile = InstructorProfile.objects.get(user=user)
            token['profile_id'] = profile.id
        except InstructorProfile.DoesNotExist:
            # If InstructorProfile does not exist, try StudentProfile
            try:
                profile = StudentProfile.objects.get(user=user)
                token['profile_id'] = profile.id
            except StudentProfile.DoesNotExist:
                # Handle the case where neither profile exists
                token['profile_id'] = None

        return token


# ================ CREATING OF USER ===================
# class UserSerializer(ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = ['id', 'name', 'email', 'password', 'user_type']
#         depth = 1
        

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.otp = generate_otp()  
#         user.set_password(password)
#         user.save()
#         return user

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'user_type']
        depth = 1
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True)
#     id = serializers.UUIDField(read_only=True,)
#     talentprofile = TalentProfileSerializer(read_only=True)
     

#     class Meta:
#         model = User
#         fields = ['id', 'name', 'email', 'password', 'user_type']
#         depth = 1  

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

# ==================== VERIFY USER SERIALIZER =======================
# class VerifyUserSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     otp = serializers.CharField(required=True)

#     def validate(self, attrs):
#         email = attrs['email']
#         otp = attrs['otp']
#         user = User.objects.filter(email=email).first()
#         if not user:
#             raise serializers.ValidationError('Invalid email address')
#         if user.is_active or user.otp != otp:
#             raise serializers.ValidationError('Invalid OTP code')
#         return attrs
    

# class VerifyUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email','otp',)

    

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        # depth = 1



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


class PaymentSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSuccess
        fields = '__all__'
        depth = 2



class BookingSerializerPost(serializers.ModelSerializer):
    isPayed = PaymentSuccessSerializer(required=False, many=False)
    class Meta:
        model = Booking
        fields = '__all__'
        # depth = 4
        

class BookingSerializerGet(serializers.ModelSerializer):
    isPayed = PaymentSuccessSerializer(required=False, many=False)
    class Meta:
        model = Booking
        fields = '__all__'
        depth = 4
    

# ================ INSTRUCTIOR ======================
class InstructorSerializer(ModelSerializer):
    classes = ClassSerializer(many=True)
    instructorRemark = InstructorRemarkSerializer(many=True)
    allBookings = BookingSerializerGet(many=True)
    
    
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        depth = 1

# ===================== STUDENT ========================
class StudentSerializer(ModelSerializer):
    hiredInstructors = BookingSerializerGet(many=True)
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
    


class AdminSeeRemarkSerializer(serializers.ModelSerializer):
    instructorAdminRemark = InstructorRemarkSerializer(many=True)
    studentAdminRemark = StudentRemarkSerializer(many=True)
    
    class Meta:
        model = AdminSeeRemarks
        fields = '__all__'


class DeleteUserByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email address found.")
        return value