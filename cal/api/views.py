from rest_framework import viewsets

from .serializers import EventSerializer, EventCategorySerializer, IconSerializer, ColorSerializer, ProfileSerializer
from ..models import Event, EventCategory, Icon, Color, Profile


class EventCategoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return EventCategory.objects.filter(user=user)
    serializer_class = EventCategorySerializer


class EventViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(user=user)
    serializer_class = EventSerializer


class IconViewSet(viewsets.ModelViewSet):

    queryset = Icon.objects.all()
    serializer_class = IconSerializer


class ColorViewSet(viewsets.ModelViewSet):

    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)
    serializer_class = ProfileSerializer

