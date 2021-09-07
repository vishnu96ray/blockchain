from django.shortcuts import render, redirect
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
    my_total_ref_earning = 0
    amt = current_user.joining_amt
    my_payable = Payable.objects.filter(user=current_user, is_activated=True).order_by('-date').first()

    my_payable = 0.0 if my_payable is None else float(my_payable.payable)

    joining_date = current_user.user.date_joined.date()

    my_re = Reinvestment.objects.filter(profile=current_user).order_by('date')

    final_d = []
    if len(my_re) != 0:
        for x in my_re:
            if len(final_d) != 0:
                amt = final_d[len(final_d)-1][1]
            re_date = x.date.date()
            diff = (re_date - joining_date).days
            rev = diff * (0.75/100) * float(amt)
            left_of_initial_amount = float(amt) - rev
            final_d.append([left_of_initial_amount, (left_of_initial_amount + float(x.amount))])

    if len(final_d) != 0:
        amt = final_d[len(final_d)-1][1]

    final_amount = float(amt)

    my_revenue_rate = float(final_amount) * (0.75 / 100)

    date_difference = (today - joining_date).days
    if date_difference < 266:
        delta = date_difference
    else:
        delta = 266

    for i in range(delta+1):
        day = joining_date + timedelta(days=i)
        is_holiday = Holidays.objects.filter(date__date=day).first()
        if day.weekday() == 5 or day.weekday() == 6 or is_holiday:
            pass
        else:
            my_revenue += my_revenue_rate

    final_data = []
    for user in all_users:
        total_ref_earning = 0

        children_list = []

        children = user.get_all_children()

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

                    children_list.append(t)

                    calculated_commission = float(t.joining_amt) * (commission / 100)
                    total_ref_earning += calculated_commission
        else:
            total_ref_earning = 0

        if user == current_user:
            my_total_ref_earning = total_ref_earning

        final_data.append([user])
    my_total = my_total_ref_earning + my_revenue

    # pagination logic
    paginator = Paginator(final_data, 20) # change this number to how many rows you want to show
    pg_no = request.GET.get('page', 1)
    page = paginator.get_page(pg_no)

    prev_url = ''
    next_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'

    context = {'page': page, 'nexturl': next_url, 'prevurl': prev_url, 'final_data': page.object_list, 'all_users': all_users, 'my_revenue': my_revenue,
               'my_total_ref_earning': my_total_ref_earning, 'last_day_payable': last_day_totals,
               'totals_today': totals_today, 'my_ref_id': referral_id, 'parent_ref_id': parent_ref_id, 'amt': current_user.joining_amt, 'my_revenue_rate': my_revenue_rate,
               'my_total': my_total, 'my_payable': my_payable, 'my_childern_list': my_childern_list}
    return render(request, 'dashboard/admin_base.html', context)


def userprofile(request):
    return render(request, 'dashboard/user_profile.html')


def reinvest(request):
    profile = request.user.userdetail
    if request.method == 'POST':
        re_amount = request.POST.get('re_amount')
        reinvestment = Reinvestment(amount=re_amount, profile=profile)
        reinvestment.save()
        return redirect('insite')
    return render(request, 'accounts/reinvest.html')


def payable(request):
    payables = Payable.objects.filter(payable__gte=100).order_by('-date')
    context = {'payables': payables}
    return render(request, 'dashboard/payables.html', context)


def activate_payable(request, pk):
    payable = Payable.objects.get(id=pk)
    payable.is_activated = True
    payable.save()
    return redirect('payable')