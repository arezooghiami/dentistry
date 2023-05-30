from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from rest_framework import serializers




class User(AbstractBaseUser):
    # profile=models.OneToOneField('Profile',on_delete=models.CASCADE)

    name= models.CharField(max_length=50, blank=True, null=True,)
    password = models.CharField(max_length=120)
    username = models.CharField(db_index=True, max_length=50, unique=True, blank=False, null=False)
    pezeshki_code = models.IntegerField(verbose_name='شماره نظام پزشکی', blank=True, null=True, )
    email = models.EmailField(unique=False, max_length=50, blank=True, null=True, default=None)
    phone = models.BigIntegerField(verbose_name='موبایل', blank=True, null=True, )
    last_login = models.DateTimeField(_("last login"), default=timezone.now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["name", 'password']



    def __str__(self):
        return str(self.username)
class Expertise(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Example(models.Model):
    text=models.TextField(null=True)
    image=models.ImageField(null=True)
    expertise=models.ForeignKey(Expertise,on_delete=models.CASCADE)
    doctor=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.doctor.username+' : '+self.text[:20]


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    pezeshki_code = models.IntegerField(verbose_name='شماره نظام پزشکی', blank=True, null=True, )
    name=models.CharField(max_length=50,null=True,blank=True)
    working_hour=models.TextField(null=True,max_length=120)
    bio = models.TextField(null=True,blank=True)
    birth_year = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/',null=True,blank=True)
    expertise=models.ManyToManyField(Expertise)

    def __str__(self):
        return self.user.username

def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()



post_save.connect(save_profile_user,sender=User)



