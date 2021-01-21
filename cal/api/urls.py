from django.urls import path
from rest_framework import routers
from .views import EventViewSet, EventCategoryViewSet, IconViewSet, ColorViewSet, ProfileViewSet

router = routers.SimpleRouter()
router.register('events', EventViewSet, basename='events')
router.register('categories', EventCategoryViewSet, basename='categories')
router.register('icons', IconViewSet, basename='icons')
router.register('colors', ColorViewSet, basename='colors')
router.register('profiles', ProfileViewSet, basename='profiles')

urlpatterns = []
urlpatterns += router.urls
