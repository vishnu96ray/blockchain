# from accounts.models import *


# def calculateProfit(id):
#     user = UserProfile.objects.filter(id=id)
#     if user.exists():
#         profit = []
#         referral_code = user[0].referral_code
#         print(referral_code,99999)
#         for i in range(0, 5):
#             if(referral_code is not None):
#                 referredBy = UserProfile.objects.filter(user_referral=referral_code)
#                 percentage = 5/2**i
#                 profitAmount = float(user[0].joining_amt)*percentage/100
#                 profit.append((referredBy[0], percentage, profitAmount))
#                 referral_code = referredBy[0].referral_code
#             else:
#                 break
#         print(profit,545445)
#     return "User not found"