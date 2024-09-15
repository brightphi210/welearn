
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'Student':
            StudentProfile.objects.create(user=instance)
            print('Student profile created successfully')
        elif instance.user_type == 'Instructor':
            InstructorProfile.objects.create(user=instance)
            print('Instructor profile created successfully')
        else:
            print('Invalid user type. Profile not created.')



@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    
    try:
        if created == False:
            if instance.user_type == 'Instructor':
                instance.InstructorProfile.save()
                print('Profile updated successfully')

            if instance.user_type == 'Student':
                instance.StudentProfile.save()
                print('Profile updated successfully')
    except:
        instance.userprofile = None



@receiver(post_save, sender=User)
def send_email_confirmation(sender, instance, created, **kwargs):
    if created:
        print("called")
        subject = 'Your Account has been created successfully'
        message = 'Welcome to Welearn Global click the link to very your mail https://www.welearnglobal.org/'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]   
        
        send_mail(subject, message, from_email, recipient_list)


        
