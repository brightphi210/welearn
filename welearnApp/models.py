from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin

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
    





# ======================== Creatives =============================
class User(AbstractBaseUser, PermissionsMixin):
    auto_id = models.PositiveBigIntegerField(unique=False, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    otp = models.CharField(max_length=6, blank=True)


    USER_TYPE_CHOICES = (
        ('Instructor', 'Instructor'),
        ('Student', 'Student'),
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

    def save(self, *args, **kwargs):
        count_id = User.objects.all().count()
        self.auto_id = count_id+1
        super(User, self).save(*args, **kwargs)

    def _str_(self):
        return self.name
    

class InstructorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    EXPERIENCE = (
        ('One', '1-2'),
        ('Two', '3-5'),
        ('Three', '6 above'),
    )
    occupation = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.CharField(max_length=255, choices=EXPERIENCE, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_hired = models.BooleanField(default=False)
    number_of_trained_students = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    dob = models.CharField(max_length=255, blank=True, null=True)
    bio_data = models.TextField(max_length=255, blank=True, null=True)


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
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    DURATION = (
        ('ONE', 'TWO WEEKS'),
        ('TWO', 'ONE MONTHS'),
        ('THREE', 'TWO MONTHS'),
        ('FOUR', 'THREE MONTHS'),
        ('FIVE', 'FOUR MONTHS'),
        ('SIX', 'FIVE MONTHS'),
        ('SEVEN', 'SIX MONTHS'),
        ('EIGHT', 'ONE YEAR ABOVE'),
    )
    durtion = models.CharField(max_length=255, blank=True, null=True, choices=DURATION)
    price = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.class_name


class Booking(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    class_booked = models.ForeignKey(Class, on_delete=models.CASCADE)
    location = models.CharField(max_length=225, null=True, blank=True)
    day = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.class_booked.class_name


# ==================== PASSWORD FORGET AND RESET =====================

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


