import json

from celery import shared_task
from .models import *
from datetime import datetime, timedelta
from django.conf import settings
import requests

today = datetime.now().date()
yesterday = today - timedelta(days=1)


@shared_task
def update_holidays():
    today = datetime.now().date()
    holidays_this_year = Holidays.objects.filter(date__date__year=today.year)

    if len(holidays_this_year) == 0:
        response = requests.get(
            f'https://calendarific.com/api/v2/holidays?api_key={settings.CALENDAR_API_KEY}&country=IN&year=2021'
        )
        # print(response.content)
        json_response = json.loads(response.content)
        for h in json_response['response']['holidays']:
            h_name = str(h['name'])
            d = h['date']['iso'].split('T')[0]
            h_date = datetime.strptime(d, '%Y-%m-%d')
            h_type = str(h['type'][0])
            holiday = Holidays(name=h_name, date=h_date, type=h_type)

            holiday.save()
            print(holiday)
            print('\n')

        return 'Holidays Updated'


@shared_task
def calculation():
    all_users = UserProfile.objects.all()
    for user in all_users:
        last_day_totals = Payable.objects.filter(date__date=yesterday)
        totals_today = Payable.objects.filter(date__date=today)
        children_count = 1
        amount = float(user.joining_amt)
        revenue = 0
        joining_date = user.user.date_joined.date()

        my_re = Reinvestment.objects.filter(profile=user).order_by('date')

        final_d = []
        if len(my_re) != 0:
            for x in my_re:
                if len(final_d) != 0:
                    amount = final_d[len(final_d) - 1][1]
                re_date = x.date.date()
                diff = (re_date - joining_date).days
                rev = diff * (0.75 / 100) * float(amount)
                left_of_initial_amount = float(amount) - rev
                final_d.append([left_of_initial_amount, (left_of_initial_amount + float(x.amount))])

        if len(final_d) != 0:
            amount = final_d[len(final_d) - 1][1]

        final_amount = float(amount)
        revenue_rate = float(final_amount) * (0.75 / 100)
        date_difference = (today - joining_date).days

        if date_difference < 266:
            delta = date_difference
        else:
            delta = 266

        for i in range(delta + 1):
            day = joining_date + timedelta(days=i)
            is_holiday = Holidays.objects.filter(date__date=day).first()
            if day.weekday() == 5 or day.weekday() == 6 or is_holiday:
                pass
            else:
                revenue += revenue_rate

        total_ref_earning = 0

        children_list = []

        children = user.get_all_children()

        # calculate commission
        if len(children) != 1:
            # loop through the first 10 parents
            for t in children[1:]:
                # get level difference
                difference = int(t.level) - int(user.level)
                # calculate commission
                if difference == 1:
                    commission = 5
                else:
                    commission = 0.05

                if difference <= 20:

                    children_count += 1

                    children_list.append(t)

                    calculated_commission = float(t.joining_amt) * (commission / 100)

                    if int(t.level) - int(user.level) >= 2:
                        if t.user.date_joined.date() - datetime.now().date() <= timedelta(days=133):
                            total_ref_earning += calculated_commission
                    else:
                        total_ref_earning += calculated_commission
        else:
            total_ref_earning = 0

        total_earning = revenue + total_ref_earning

        if yesterday.weekday() == 5:
            last_day = today - timedelta(days=2)
            yesterday_payable = Payable.objects.filter(user=user, date__date=last_day).first()
        elif yesterday.weekday() == 6:
            last_day = today - timedelta(days=3)
            yesterday_payable = Payable.objects.filter(user=user, date__date=last_day).first()
        elif Holidays.objects.filter(date__date=yesterday):
            last_day = today - timedelta(days=2)
            yesterday_payable = Payable.objects.filter(user=user, date__date=last_day).first()
        else:
            yesterday_payable = last_day_totals.filter(user=user).first()

        if not yesterday_payable:
            total_yesterday = 0.0
        else:
            total_yesterday = yesterday_payable.total_earning

        # check if today is holiday or weekend
        is_holiday_today = Holidays.objects.filter(date__date=today).first()
        if today.weekday() == 5 or today.weekday() == 6 or is_holiday_today:
            payable = 0
        else:
            payable_temp = total_earning - total_yesterday
            payable = payable_temp - (payable_temp * 0.1)

        if totals_today.filter(user=user).first() is None:
            total_earning_for_this_user = Payable(user=user, total_earning=total_earning, payable=payable)
            total_earning_for_this_user.save()
        else:
            this_users_payable = totals_today.filter(user=user).first()
            if this_users_payable.total_earning != total_earning or this_users_payable.payable != payable:
                this_users_payable.total_earning = total_earning
                this_users_payable.payable = payable
                this_users_payable.save()

    return 'done'


@shared_task
def clean_payable():
    date = datetime.now().date() - timedelta(days=10)
    payables = Payable.objects.filter(date__date__lte=date)
    payables.delete()
    return 'cleaned'