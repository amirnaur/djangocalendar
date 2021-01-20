from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TEMPLATES = [
        ("table.css", "Таблица"),
        ("modern.css", "Современный"),
    ]
    template = models.CharField(max_length=30, choices=TEMPLATES, default="modern.css", verbose_name="Шаблон")
    show_year = models.BooleanField(default=True, verbose_name="Показывать год")
    cross = models.BooleanField(default=True, verbose_name="Зачеркивание")

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)