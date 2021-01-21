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
    def __init__(self, year=None, month=None, request=None):
        self.year = year
        self.month = month
        self.request = request
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
        crossed = "crossed" if datetime.date.today() > day and self.request.user.profile.cross else ""
        if day.month == self.month:
            return f"<div class='day-container {crossed}' id='{date_id}' onclick='dayEvents(this)'><span class='date %s'>{day.day}</span><ul></ul></div>" % \
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
    def formatmonth(self, theyear, themonth):
        cal = ''
        weekday_names = f'<div class="weekday-names">\
                        <div class="weekday-empty"></div>\
                        <div class="weekday-names-container">\
                        <div class="weekday-name"></div>\
                        <div class="weekday-name">Пн.</div>\
                        <div class="weekday-name">Вт.</div>\
                        <div class="weekday-name">Ср.</div><div class="weekday-name">Чт.</div>\
                        <div class="weekday-name">Пн.</div><div class="weekday-name">Сб.</div>\
                        <div class="weekday-name">Вс.</div></div></div>'
        # cal += weekday_names
        weeks = self.monthdatescalendar(theyear, themonth)
        cal += f'<div class="flex-row">'
        cal += weekday_names
        cal += f'<div class="month-container">'
        cal += f'<div class="month">{month_names[themonth]} {theyear}</div>'
        cal += f'<div class="flex-row">'
        for week in weeks:
            if isleap(week[3].year):
                month_length = mdays_leap
            else:
                month_length = mdays
            # if week[0].day > month_length[week[0].month] - 3 or week[0].day < 5:

            cal += self.formatweek(week)
            # if week[6].day >= month_length[week[6].month] - 3 or week[6].day <= 3:
        cal += '</div>'  # month-container
        cal += '</div>'  # flex-row
        cal += '</div>'  # flex-row
        return cal

    def format3months(self, theyear, start_month):
        cal = ''
        weeks = []
        last_week = None
        month = start_month - 1
        weekday_names = f'<div class="weekday-names">\
                        <div class="weekday-empty"></div>\
                        <div class="weekday-names-container">\
                        <div class="weekday-name"></div>\
                        <div class="weekday-name">Пн.</div>\
                        <div class="weekday-name">Вт.</div>\
                        <div class="weekday-name">Ср.</div><div class="weekday-name">Чт.</div>\
                        <div class="weekday-name">Пт.</div><div class="weekday-name">Сб.</div>\
                        <div class="weekday-name">Вс.</div></div></div>'
        # cal += weekday_names
        cal += f'<div class="flex-row">'
        cal += weekday_names
        for _ in range(3):
            # if month + 1 <= 12:
            #     month += 1
            # else:
            #     theyear += 1
            #     month = 1
            month = max(1, (month + 1) % 13)
            cal += f'<div class="month-container">'
            cal += f'<div class="month">{month_names[month]} {theyear}</div>'
            cal += f'<div class="flex-row">'
            for week in self.monthdatescalendar(theyear, month):
                # if last_week in self.monthdatescalendar(theyear, month):
                if not is_month_week(week, month):
                    # weeks.append(week)
                    # last_week = None
                    continue
                cal += self.formatweek(week)
            last_week = self.monthdatescalendar(theyear, month)[-1]
            cal += '</div>'  # month-container
            cal += '</div>'  # flex-row
        cal += '</div>'  # flex-row'
        return cal

    def format6months(self, theyear, start_month):
        cal = ''
        weeks = []
        last_week = None
        month = start_month - 1
        weekday_names = f'<div class="weekday-names">\
                        <div class="weekday-empty"></div>\
                        <div class="weekday-names-container">\
                        <div class="weekday-name"></div>\
                        <div class="weekday-name">Пн.</div>\
                        <div class="weekday-name">Вт.</div>\
                        <div class="weekday-name">Ср.</div><div class="weekday-name">Чт.</div>\
                        <div class="weekday-name">Пт.</div><div class="weekday-name">Сб.</div>\
                        <div class="weekday-name">Вс.</div></div></div>'
        # cal += weekday_names

        for _ in range(2):
            cal += f'<div class="flex-row">'
            cal += weekday_names
            for _ in range(3):
                month = max(1, (month + 1) % 13)
                current_year = theyear + 1 if start_month > month else theyear
                cal += f'<div class="month-container">'
                cal += f'<div class="month">{month_names[month]} {current_year}</div>'
                cal += f'<div class="flex-row">'
                for week in self.monthdatescalendar(current_year, month):
                    if not is_month_week(week, month):
                        continue
                    cal += self.formatweek(week)
                last_week = self.monthdatescalendar(current_year, month)[-1]
                cal += '</div>'  # month-container
                cal += '</div>'  # flex-row
            cal += '</div>'  # flex-row
        return cal

    def formatanyrow(self, theyear, month=1, length=12, rows=3):
        row = ''
        weekday_names = f'<div class="weekday-names">\
                <div class="weekday-empty"></div>\
                <div class="weekday-names-container">\
                <div class="weekday-name"></div>\
                <div class="weekday-name">Пн.</div>\
                <div class="weekday-name">Вт.</div>\
                <div class="weekday-name">Ср.</div><div class="weekday-name">Чт.</div>\
                <div class="weekday-name">Пт.</div><div class="weekday-name">Сб.</div>\
                <div class="weekday-name">Вс.</div></div></div>'
        week_dict = {}
        flag_first = True
        length, rows = max(1, length), min(length, rows)
        current_month = month
        weeks_in_year = max(get_week_number(datetime.date(theyear + 1, 1, 1)), 52)
        for i in range(length):
            # current_month = month + i if not (month + i) % 12 else (month + i) % 12
            month_weeks = self.monthdatescalendar(theyear, current_month)
            for week in month_weeks:
                if get_week_number(week[0]) not in week_dict.keys():
                    week_dict.update({get_week_number(week[0]): week})
                    if flag_first:
                        first_week_number = get_week_number(week[0])
                        flag_first = False
                else:
                    continue
            if current_month + 1 <= 12:
                current_month += 1
            else:
                theyear += 1
                current_month = 1
        weeks_in_row = len(week_dict) // rows

        for i in range(0, rows):
            row += f'<div class="row{rows} flex-row">\n'
            row += weekday_names
            if first_week_number == 53:
                j = first_week_number
                row += f'<div class="month-container">'
                row += f'<div class="month">{month_names[week_dict[53][6].month]} {week_dict[53][6].year}</div>'
                row += f'{self.formatweek(week_dict[j], events)}'
                first_week_number = 1
                for j in range(first_week_number + i * weeks_in_row, weeks_in_row + i * weeks_in_row):
                    row += f'{self.formatweek(week_dict[j], events)}'
                    # row += f'{j % 54}'
                row += f'</div>\n'
            else:
                for j in range(first_week_number + i * weeks_in_row,
                               weeks_in_row + i * weeks_in_row + first_week_number):
                    row += f'{self.formatweek(week_dict[j], events)}\n' if j <= weeks_in_year \
                        else f'{self.formatweek(week_dict[j % weeks_in_year], events)}\n'
                    # row += f'{j % 54}'
                row += f'</div>\n'

        return row

    def formatcustomrow(self, theyear, start_month=1, length=12, rows=3):
        cal = ''
        month = start_month - 1
        weekday_names = f'<div class="weekday-names">\
                                <div class="weekday-empty"></div>\
                                <div class="weekday-names-container">\
                                <div class="weekday-name"></div>\
                                <div class="weekday-name">Пн.</div>\
                                <div class="weekday-name">Вт.</div>\
                                <div class="weekday-name">Ср.</div><div class="weekday-name">Чт.</div>\
                                <div class="weekday-name">Пт.</div><div class="weekday-name">Сб.</div>\
                                <div class="weekday-name">Вс.</div></div></div>'
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
                if self.request.user.profile.show_year:
                    cal += f'<div class="month">{month_names[month]} {current_year}</div>'
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
