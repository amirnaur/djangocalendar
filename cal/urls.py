from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'cal'

urlpatterns = [
    url(r'^profile/', views.profile, name='profile_edit'),
    url(r'^calendar/month/$',
        login_required(views.CalendarViewMonth.as_view(), login_url='login'), name='calendar_month'),
    url(r'^calendar/3months/$',
        login_required(views.CalendarView3Months.as_view(), login_url='login'), name='calendar_3months'),
    url(r'^calendar/6months/$',
        login_required(views.CalendarView6Months.as_view(), login_url='login'), name='calendar_6months'),
    url(r'^calendar/year/$',
        login_required(views.CalendarViewYear.as_view(), login_url='login'), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]