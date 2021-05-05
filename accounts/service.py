import requests
import json
import random
import datetime
from twilio.rest import Client


def referral():
	rr = random.randint(11111,99999)
	plus = 'SabziCartb2c'
	x = (plus + str(rr))
	return x


def usesrpass():
    pp = random.randint(1111111,9999999)
    plus = 'sabzi'
    u = (plus + str(pp))
    return u    

	
account_sid = 'ACdcf64a7c9a50f5be4a56754c02238076'
auth_token = '4c0abbe370cf9bc84b2c4d4db94102b6'
def userauthsend(mobile,user,username,password):
    
    client = Client(account_sid, auth_token)
    customer_num='+91'+str(mobile)
    message = client.messages.create(
                                body='Welcome,\nYour username:'+str(username)+'\npassword:'+str(password)+'\nvisit:https://www/sabzicart.in',
                                from_='+12517665621',
                                to=customer_num
                            )
    return