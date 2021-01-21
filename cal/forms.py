from django.forms import ModelForm, DateInput
from .models import Event, Profile


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
        # widgets = {
        #     'template': 'modern.css',
        #     'show_year': True,
        #     'cross': True,
        # }
        fields = ('template', 'show_year', 'cross',)

