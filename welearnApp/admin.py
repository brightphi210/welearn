from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)
admin.site.register(Class)
admin.site.register(Booking)
admin.site.register(PasswordReset)
admin.site.register(Review)
