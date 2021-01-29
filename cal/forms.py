from django.forms import ModelForm, DateInput
from .models import Event, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'date_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'notification_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['notification_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('template', 'show_year', 'cross',)
        CHOICES = [("table.css", "Таблица"), ("modern.css", "Современный")]
        widgets = {
            'template': forms.RadioSelect(choices=CHOICES)
        }


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'})