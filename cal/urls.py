from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cal'

urlpatterns = [
    url(r'^profile/', views.profile, name='profile_edit'),
    url(r'^calendar/month/$', views.CalendarViewMonth.as_view(), name='calendar_month'),
    url(r'^calendar/3months/$', views.CalendarView3Months.as_view(), name='calendar_3months'),
    url(r'^calendar/6months/$', views.CalendarView6Months.as_view(), name='calendar_6months'),
    url(r'^calendar/year/$', views.CalendarViewYear.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]