from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TEMPLATES = [
        ("table.css", "Таблица"),
        ("modern.css", "Современный"),
    ]
    template = models.CharField(max_length=30, choices=TEMPLATES, default="modern.css", verbose_name="Вид календаря")
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


class EventCategory(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    # icon = models.ImageField()

    def __str__(self):
        return self.name


class Color(models.Model):
    GRAY = '757575'
    ORANGE = 'F2994A'
    YELLOW = 'F2C94C'
    GREEN = '00CCA7'
    BLUE = '2D9CDB'
    RED = 'EB5757'
    BLACK = '4F4F4F'
    COLORS = [
        (GRAY, 'gray'),
        (ORANGE, 'orange'),
        (YELLOW, 'yellow'),
        (GREEN, 'green'),
        (BLUE, 'blue'),
        (RED, 'red'),
        (BLACK, 'black')
    ]
    color = models.CharField(
        max_length=8,
        choices=COLORS,
        default=GRAY,
    )
    # name = models.CharField(max_length=12, default="gray")

    def __str__(self):
        return self.color


class Icon(models.Model):

    name = models.CharField(max_length=50)
    # icon = models.FileField(upload_to='icons/', blank=True, null=True)
    inline_svg = models.CharField(max_length=2000, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.icon.name.endswith('.svg'):
    #         self.inline_svg = self.icon.read().decode('utf-8')
    #         super().save(*args, **kwargs)

    def __str__(self):
        return format_html(self.inline_svg + self.name)
        # return self.icon.url


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_time = models.DateField()
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    notification_time = models.DateTimeField(blank=True, null=True)
    event_category = models.ForeignKey(EventCategory, null=True, blank=True, on_delete=models.SET_NULL)
    icon = models.ForeignKey(Icon, null=True, blank=True, on_delete=models.SET_NULL)
    event_color = models.ForeignKey(Color, null=True, default=1, on_delete=models.PROTECT, related_name="event_color")
    icon_color = models.ForeignKey(Color, null=True, default=None, on_delete=models.PROTECT, related_name="icon_color")

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<button data-target="#exampleModal" data-toggle="modal" data-id="{self.id}"> {self.title} </button>'

    def __str__(self):
        return self.title