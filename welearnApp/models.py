from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import random

from django.conf import settings
# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)



# from django.contrib.auth.models import BaseUserManager

# class UserManager(BaseUserManager):
#     def create_user(self,email,password=None,**extra_fields):
#        if not (email):
#            raise ValueError('User must have an email address')
       
#        email = self.normalize_email(email)
#        user = self.model(email=self.normalize_email(email),**extra_fields)
       
#        user.set_password(password)
#        user.is_active = True
#        user.save(using=self.db)
#        return user
        

#     def create_superuser(self, email,password=None,**extra_fields):
#         user = self.create_user(email,password,**extra_fields)
#         user.is_admin=True
        
#         user.save(using=self.db)
#         return user
    




# ======================== Creatives =============================
class User(AbstractBaseUser, PermissionsMixin):
    auto_id = models.PositiveBigIntegerField(unique=False, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    # otp_secret = models.CharField(max_length=500, null=True,)
    # otp = models.CharField(max_length=6, blank=True)


    USER_TYPE_CHOICES = (
        ('Instructor', 'Instructor'),
        ('Student', 'Student'),
        ('Admin', 'Admin'),
    )

    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES, null=True, blank=True)
    profile_pic = models.ImageField(default='default.png', blank=True, null=True, upload_to='profile_pics/')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Only generate OTP for new users
    #         self.generate_otp()  # Generate unique OTP before saving
    #         count_id = User.objects.all().count()
    #         self.auto_id = count_id + 1
    #     super(User, self).save(*args, **kwargs)

    # def generate_otp(self):
    #     self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP


    def _str_(self):
        return self.name
    

class InstructorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_hired = models.BooleanField(default=False)
    number_of_trained_students = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    dob = models.CharField(max_length=255, blank=True, null=True)
    bio_data = models.TextField(max_length=255, blank=True, null=True)
    LGA = models.CharField(max_length=255, blank=True, null=True) 
    state = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.user.name
    


class Review(models.Model):
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name='reviews')
    student_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"This is review for this instructor{self.instructor.user.name}"




class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.user.name
    


class Class(models.Model):
    instructor = models.ForeignKey(InstructorProfile, related_name='classes', on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    DURATION = (
        ('TWO WEEKS', 'TWO WEEKS'),
        ('ONE MONTHS', 'ONE MONTHS'),
        ('TWO MONTHS', 'TWO MONTHS'),
        ('THREE MONTHS', 'THREE MONTHS'),
        ('FOUR MONTHS', 'FOUR MONTHS'),
        ('FIVE MONTHS', 'FIVE MONTHS'),
        ('SIX MONTHS', 'SIX MONTHS'),
        ('ONE YEAR ABOVE', 'ONE YEAR ABOVE'),
    )
    duration = models.CharField(max_length=255, blank=True, null=True, choices=DURATION)
    price = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.class_name


class Booking(models.Model):
    
    DAYS = (
        ('MONDAY', 'MONDAY'),
        ('TUESDAY', 'TUESDAY'),
        ('WEDNESDAY', 'WEDNESDAY'),
        ('THURSDAY', 'THURSDAY'),
        ('FRIDAY', 'FRIDAY'),
        ('SATURDAY', 'SATURDAY'),
    )


    TIMES = (
        ('10am-12pm', '10am-12pm'),
        ('12pm-2pm', '12pm-2pm'),
        ('2pm-4pm', '2pm-4pm'),
        ('4pm-6pm', '4pm-6pm'),
    )
    
    student = models.ForeignKey(StudentProfile, related_name='hiredInstructors', on_delete=models.CASCADE)
    instructor = models.ForeignKey(InstructorProfile, related_name='allBookings', on_delete=models.CASCADE, null=True, blank=True)
    class_booked = models.ForeignKey(Class, on_delete=models.CASCADE)
    location = models.CharField(max_length=225, null=True, blank=True)
    dayone = models.CharField(max_length=255, blank=True, null=True, choices=DAYS)
    daytwo = models.CharField(max_length=255, blank=True, null=True, choices=DAYS)
    daythree = models.CharField(max_length=255, blank=True, null=True, choices=DAYS)
    timeone = models.CharField(max_length=255, blank=True, null=True, choices=TIMES)
    timetwo = models.CharField(max_length=255, blank=True, null=True, choices=TIMES)
    timethree = models.CharField(max_length=255, blank=True, null=True, choices=TIMES)


    def clean(self):
        # Check if an instructor has more than three classes on the same day
        days_times = {
            'dayone': 'timeone',
            'daytwo': 'timetwo',
            'daythree': 'timethree'
        }
        for day_field, time_field in days_times.items():
            day = getattr(self, day_field)
            time = getattr(self, time_field)
            if day and time:
                # Check for maximum classes per day
                if Booking.objects.filter(instructor=self.instructor, **{day_field: day, time_field: time}).count() >= 3:
                    raise ValidationError(_(f'The instructor already has the maximum number of classes at {time} on {day}'))
                # Check for overlapping time slots
                if Booking.objects.filter(instructor=self.instructor, **{day_field: day, **{time_field: time}}).exists():
                    raise ValidationError(_(f'The time slot {time} on {day} is already booked for this instructor'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.class_booked.class_name


class PaymentSuccess(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='isPayed')
    isPaymentSuccessful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'Payment successful for booking: {self.isPaymentSuccessful}'

# ==================== PASSWORD FORGET AND RESET =====================

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class AdminSeeRemarks(models.Model):
    admin = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Admin:'

class InstructorRemark(models.Model):
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name='instructorRemark', blank=True, null=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, blank=True, null=True)
    booked_clasd = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    admin_remark = models.ForeignKey(AdminSeeRemarks, related_name='instructorAdminRemark', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Remark from {self.instructor.user.email} to {self.student.user.email}'
    


class StudentRemark(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='studentRemark', blank=True, null=True)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, blank=True, null=True)
    booked_clasd = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    admin_remark = models.ForeignKey(AdminSeeRemarks, related_name='studentAdminRemark', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Remark from {self.student.user.email} to {self.instructor.user.email}'
    



    


