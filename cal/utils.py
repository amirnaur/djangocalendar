import datetime
from calendar import HTMLCalendar, isleap, day_abbr

January = 1
mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
mdays_leap = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_names = [0, "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
               "Ноябрь", "Декабрь"]


# secondary functions
def get_week_number(date):
    return datetime.date(date.year, date.month, date.day).isocalendar()[1]


def is_month_week(week, month):
    # Проверка недели содержащей 1-ое число текущего месяца
    if isleap(week[3].year):
        month_length = mdays_leap
    else:
        month_length = mdays
    if week[0].month < month:
        if week[3].month == month:
            return True
        else:
            return False
    elif week[6].month > month:
        if week[3].month == month:
            return True
        else:
            return False
    else:
        return True


class Yearcal(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Yearcal, self).__init__()

    # CSS classes for the day <td>s
    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    # CSS classes for the day <th>s
    cssclasses_weekday_head = cssclasses

    # CSS class for the days before and after current month
    cssclass_noday = "noday"

    # CSS class for the month's head
    cssclass_month_head = "month"

    # CSS class for the month
    cssclass_month = "month"

    # CSS class for the year's table head
    cssclass_year_head = "year"

    # CSS class for the whole year table
    cssclass_year = "year"

    # formats a day as a td
    # filter events by day
    def formatday(self, day):
        date_id = day.strftime('%Y-%m-%d')
        crossed = "crossed" if datetime.date.today() > day and self.user.profile.cross else ""
        if day.month == self.month:
            return f"<div class='day-container {crossed}' id='{date_id}' " \
                   f"onclick='dayEvents(this)'><span class='date %s'>{day.day}</span><ul></ul></div>" % \
                   self.cssclasses[day.weekday()]

        return f"<div class='day-container {crossed}' id='{date_id}' onclick='dayEvents(this)'>" \
               f"<span class='date'>{day.day}</span><ul></ul></div>"

    def formatweek(self, theweek):
        cnt = 0  # Counter for week number
        v = []
        s = v.append

        s('<div class="weekday">')
        for d in theweek:
            if d.weekday() == 0:
                s(f'<div class="week-num">{d.isocalendar()[1]}</div>')
            s(self.formatday(d))
        s('</div>')
        return ''.join(v)

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<b class="%s day-name">%s</b>' % (
            self.cssclasses_weekday_head[day], day_abbr[day])

    # formats a month as a table
    # filter events by year and month

    def formatcustomrow(self, theyear, start_month=1, length=12, rows=3):
        cal = ''
        month = start_month - 1
        weekday_names = f'<div class="weekday-names">\
                                <div class="weekday-empty"></div>\
                                <div class="weekday-names-container">\
                                <div class="weekday-name"></div>\
                                <div class="weekday-name">пн</div>\
                                <div class="weekday-name">вт</div>\
                                <div class="weekday-name">ср</div><div class="weekday-name">чт</div>\
                                <div class="weekday-name">пт</div><div class="weekday-name">пт</div>\
                                <div class="weekday-name">вс</div></div></div>'
        # cal += weekday_names

        for _ in range(rows):
            cal += f'<div class="flex-row">'
            cal += weekday_names
            for _ in range(length // rows):
                # if month + 1 <= 12:
                #     month += 1
                # else:
                #     theyear += 1
                #     month = 1
                month = max(1, (month + 1) % 13)
                current_year = theyear + 1 if start_month > month else theyear
                cal += f'<div class="month-container">'
                if self.user.profile.show_year:
                    cal += f'<div class="month">{month_names[month]} <span class="year">{current_year}</span></div>'
                else:
                    cal += f'<div class="month">{month_names[month]}</div>'
                cal += f'<div class="flex-row">'
                for week in self.monthdatescalendar(current_year, month):
                    # if last_week in self.monthdatescalendar(theyear, month):
                    if not is_month_week(week, month):
                        # weeks.append(week)
                        # last_week = None
                        continue
                    cal += self.formatweek(week)
                last_week = self.monthdatescalendar(theyear, month)[-1]
                cal += '</div>'  # month-container
                cal += '</div>'  # flex-row
            cal += '</div>'  # flex-row
        return cal
