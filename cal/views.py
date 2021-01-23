from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import calendar

from .models import *
from .utils import Yearcal
from .forms import EventForm, ProfileForm, CreateUserForm


class CalendarViewMonth(generic.ListView):
    model = Event
    template_name = 'cal/calendar_month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Yearcal(d.year, d.month, self.request)
        html_cal = cal.formatcustomrow(theyear=d.year, start_month=d.month, length=1, rows=1)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class CalendarView3Months(generic.ListView):
    model = Event
    template_name = 'cal/calendar_3months.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Yearcal(d.year, d.month, self.request)
        html_cal = cal.formatcustomrow(theyear=d.year, start_month=d.month, length=3, rows=1)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class CalendarView6Months(generic.ListView):
    model = Event
    template_name = 'cal/calendar_6months.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Yearcal(d.year, d.month, self.request)
        html_cal = cal.formatcustomrow(theyear=d.year, start_month=d.month, length=6, rows=2)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class CalendarViewYear(generic.ListView):
    model = Event
    template_name = 'cal/calendar_year.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('year', None))
        cal = Yearcal(d.year, request=self.request)
        html_cal = cal.formatcustomrow(d.year, start_month=1,  length=12, rows=4)
        context['calendar'] = mark_safe(html_cal)
        context['prev_year'] = prev_year(d)
        context['next_year'] = next_year(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_m = first - timedelta(days=1)
    month = 'month=' + str(prev_m.year) + '-' + str(prev_m.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_m = last + timedelta(days=1)
    month = 'month=' + str(next_m.year) + '-' + str(next_m.month)
    return month


def prev_year(d):
    prev_y = d.replace(year=d.year - 1)
    year = 'year=' + str(prev_y.year) + '-' + str(prev_y.month)
    return year


def next_year(d):
    next_y = d.replace(year =d.year + 1)
    year = 'year=' + str(next_y.year) + '-' + str(next_y.month)
    return year


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    initial_dict = {
        "template": request.user.profile.template,
        "show_year": request.user.profile.show_year,
        "cross": request.user.profile.cross,
    }
    form = ProfileForm(request.POST, initial=initial_dict, instance=request.user.profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
    else:
        form = ProfileForm(initial=initial_dict, instance=request.user.profile)
    if form.is_valid():
        form.save()
        # return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/profile.html', {'form': form})


def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
