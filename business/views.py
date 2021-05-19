from django.shortcuts import render,redirect
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.conf import settings
import requests
import json
from .decorators import unapproved_user

# from .service import calculateProfit
# SabziCartb2c66468   sabzi7455127
# SabziCartb2c76860	sabzi6052640
# SabziCartb2c49766   sabzi6725097
# SabziCartb2c30871	sabzi9265713
					# sabzi3925600

# @login_required(login_url='/')
# def business(request):
# 	referral_code = None
# 	all_data = UserProfile.objects.get(user=request.user)
# 	myreferralid = all_data.user_referral
# 	amt = all_data.joining_amt
# 	applicant_name = all_data.applicant

# 	total_referrar = UserProfile.objects.filter(referral_code=myreferralid).count()
	

# 	# my_referrar = UserProfile.objects.filter(referral_code=referral_code)
# 	my_referrar = UserProfile.objects.filter(referral_code=myreferralid)
# 	total_earn = []
# 	for i in my_referrar:
# 		bb = int(i.joining_amt)
# 		total_earn.append(bb)
# 	full_list = sum(total_earn)
# 	tre = full_list*5/100
# 	revenue = int(amt)*1/100
# 	#

# 	tte = tre + revenue
# 		# print(bb//3)

	
# 	# total_referrar = UserProfile.objects.filter(referral_code=referral_code, user=request.user).count()
# 	# print(total_referrar,1111)
# 	user = UserProfile.objects.filter(user=request.user)
# 	if user.exists():
# 		profit = []
# 		referral_code = user[0].referral_code
# 		for i in range(0, 5):
# 			if(referral_code is not None):
# 				referredBy = UserProfile.objects.filter(user_referral=referral_code)
# 				percentage = 5/2**i
# 				profitAmount = float(user[0].joining_amt)*percentage/100
# 				profit.append((referredBy[0], percentage, profitAmount))
# 				referral_code = referredBy[0].referral_code
# 			else:
# 				break
# 		print(profit,545445)
# 	# print("user not found")	
# 	# return "User not found"

# 	# abc = calculateProfit(all_data.id)
# 	# print(abc,111111111111)

# 	return render(request, 'dashboard/admin_base.html', {'myreferralid':myreferralid,'tte':tte, 'revenue':revenue, 'tre':tre, 'fee':amt, 'applicant_name':applicant_name, 'my_referrar':my_referrar, 'total_referrar':total_referrar})

def update_holidays(request):
    today = datetime.now().date()
    holidays_this_year = Holidays.objects.filter(date__date__year=today.year)

    if len(holidays_this_year) == 0:
        response = requests.get(
            f'https://calendarific.com/api/v2/holidays?api_key={settings.CALENDAR_API_KEY}&country=IN&year=2021'
        )
        # print(response.content)
        json_response = json.loads(response.content)
        for h in json_response['response']['holidays']:
            # print(h)
            # print('\n')
            h_name = str(h['name'])
            d = h['date']['iso'].split('T')[0]
            h_date = datetime.strptime(d, '%Y-%m-%d')
            h_type = str(h['type'][0])
            holiday = Holidays(name=h_name, date=h_date, type=h_type)

            holiday.save()
            print(holiday)
            print('\n')
        return HttpResponse('tested')

    else:
        return redirect('profile')


# @login_required(login_url='/')
# def business(request):
#     # get all users in descending order of level
#     #all_users = UserProfile.objects.all().order_by('-level')

#     # loop through each user
#     # for user in all_users:
#         # get all direct and indirect parents of this user
		
# 	user = UserProfile.objects.get(user=request.user)
# 	referral_code = user.user_referral
# 	username = user.applicant
# 	children = user.get_all_children()
# 	children_count = 1
# 	amount = float(user.joining_amt)
# 	revenue_rate = amount * (0.75/100)
# 	revenue = 0
# 	total_earning = 0

# 	joining_date = request.user.date_joined.date()
# 	today = datetime.now().date()

# 	date_difference = (today - joining_date).days

# 	if date_difference < 270:
# 		delta = date_difference
# 	else:
# 		delta = 270

# 	for i in range(delta+1):
# 		day = joining_date + timedelta(days=i)
# 		if day.weekday() != 5 and day.weekday() != 6:
# 			revenue += revenue_rate

# 		print(f'{day} => {day.weekday()}')

# 	total_ref_earning = 0
# 	print(f'\ncurrent user => {user.applicant} ({user.user})\n')
# 	if len(children) != 1:
# 		# loop through the first 10 parents
# 		for t in children[1:]:
# 			# get level difference
# 			difference = int(t.level) - int(user.level)
# 			# calculate commission
# 			if difference == 1:
# 				commission = 5
# 			else:
# 				commission = 0.05

# 			if difference <= 10:
# 				offset = '-' * difference

# 				children_count += 1

# 				calculated_commission = float(t.joining_amt) * (commission / 100)
# 				total_ref_earning += calculated_commission

# 				print(f'{offset}{t.applicant} {difference} {commission}% of {t.joining_amt} => {calculated_commission}')

# 			# get the parent who will get the commission
# 			# if len(children) > index_t + 1:
# 			#
# 			#     parent = children[index_t+1]
# 			#     commission_money = amount * (commission / 100)
# 			#     if difference != -1:
# 			#         # adding up total commission earned by user
# 			#         if f'{parent}' not in final_data:
# 			#             final_data[f'{parent}'] = 0
# 			#
# 			#         final_data[f'{parent}'] += commission_money
# 			#
# 			#     # calculate commission money amount
# 			#
# 			#     # print data
# 			#     print(f'{offset}{parent.applicant} {index_t} gets {commission}% of {amount} = {commission_money}')

# 		print(children_count)
# 		total_earning = revenue + total_ref_earning
# 	context = {'revenue':revenue_rate, 'total_ref_earning':total_ref_earning, 'total_earning':total_earning, 'children_count':children_count, 'amount':amount, 'referral_code':referral_code, 'username':username, 'children':children}
# 	return render(request, 'dashboard/admin_base.html', context)

@login_required(login_url='/')
@unapproved_user
def business(request):
    # get all users in descending order of level
    # all_users = UserProfile.objects.all()
    today = datetime.now().date()

    yesterday = today - timedelta(days=1)

    last_day_totals = Payable.objects.filter(date__date=yesterday)
    totals_today = Payable.objects.filter(date__date=today)

    current_user = UserProfile.objects.get(user=request.user)
    all_users = current_user.get_all_children()
    my_childern_list =[]

    referral_id = current_user.user_referral
    parent_ref_id = current_user.referral_code
    my_revenue = 0
    my_revenue_rate = float(current_user.joining_amt) * (0.75/100)
    my_total_ref_earning = 0
    amt = current_user.joining_amt
    my_payable = 0		
    # children = user.get_all_children()

    final_data = []
    for user in all_users:
        # get all direct and indirect parents of this user
        children_count = 1
        amount = float(user.joining_amt)
        revenue_rate = amount * (0.75/100)
        print(revenue_rate)
        revenue = 0

        joining_date = user.user.date_joined.date()

        date_difference = (today - joining_date).days

        if date_difference < 270:
            delta = date_difference
        else:
            delta = 270

        for i in range(delta+1):
            day = joining_date + timedelta(days=i)
            is_holiday = Holidays.objects.filter(date__date=day).first()
            if day.weekday() == 5 or day.weekday() == 6 or is_holiday:
                pass
            else:
                revenue += revenue_rate

            # print(f'{day} => {day.weekday()}')

        print(date_difference)

        total_ref_earning = 0

        children_list = []

        children = user.get_all_children()

        print(f'\ncurrent user => {user.applicant} ({user.user})\n')
        my_difference = int(user.level) - int(current_user.level)
        if my_difference <= 10:
            my_childern_list.append(user)
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

                if difference <= 10:
                    offset = '-' * difference

                    children_count += 1

                    children_list.append(t)

                    calculated_commission = float(t.joining_amt) * (commission / 100)
                    total_ref_earning += calculated_commission

                    print(f'{offset}{user} got {calculated_commission} from {t}')
            print(children_count)
        else:
            total_ref_earning = 0

        print(f' total ref +> {total_ref_earning}')

        if user == current_user:
            my_revenue = revenue
            my_total_ref_earning = total_ref_earning

        total_earning = revenue + total_ref_earning

        print(f'{total_earning}  {revenue}')

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

        is_holiday_today = Holidays.objects.filter(date__date=today).first()
        if today.weekday() == 5 or today.weekday() == 6 or is_holiday_today:
            payable = 0
        else:
            payable_temp = total_earning - total_yesterday
            payable = payable_temp - (payable_temp * 0.1)
        if user == current_user:
            my_payable = payable
        if not totals_today.filter(user=user).first():
            total_earning_for_this_user = Payable(user=user, total_earning=total_earning, payable=payable)
            total_earning_for_this_user.save()
        else:
            this_users_payable = totals_today.filter(user=user).first()
            if this_users_payable.total_earning != total_earning or this_users_payable.payable != payable:
                this_users_payable.total_earning = total_earning
                this_users_payable.payable = payable
                this_users_payable.save()


        final_data.append([user, total_earning, payable])
    my_total = my_total_ref_earning + my_revenue
    context = {'final_data': final_data, 'all_users': all_users, 'my_revenue': my_revenue,
               'my_total_ref_earning': my_total_ref_earning, 'last_day_payable': last_day_totals,
               'totals_today': totals_today, 'my_ref_id': referral_id, 'parent_ref_id': parent_ref_id, 'amt': amt, 'my_revenue_rate': my_revenue_rate,
			   'children_count': children_count, 'total_earning': total_earning, 
			   'my_total': my_total, 'my_payable': my_payable, 'my_childern_list': my_childern_list}
    return render(request, 'dashboard/admin_base.html', context)



def userprofile(request):
	return render(request, 'dashboard/user_profile.html')	
	