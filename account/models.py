from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/')
    country = CountryField(multiple=False,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    street_address = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=13,null=True,blank=True)

    def __str__(self):
        return self.user.last_name+' '+self.user.first_name




@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()