from django.contrib import admin
from .models import Event
from .models import EventCategory
from .models import Icon
from .models import Color
from .models import Profile

admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(Icon)
admin.site.register(Color)
admin.site.register(Profile)

# Register your models here.
