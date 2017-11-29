from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from django.conf import settings


def natural_key(self):
    return ({'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name})

User.add_to_class("natural_key", natural_key)


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    user = models.ManyToManyField(User);

    def __str__(self):
        return self.name



class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=1)
    branch = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userinfo.save()
