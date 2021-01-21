from rest_framework import serializers

from ..models import Event, EventCategory, Icon, Color, Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory
        fields = '__all__'


class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model = Icon
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'
