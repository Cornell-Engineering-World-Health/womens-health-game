import urllib
import os
import json
import threading
from kivy.network.urlrequest import UrlRequest
from util.firebase import firebase
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')


# API REQUESTS

# takes in endpoint and optional data
def _api_call(endpoint, data=None):
	headers = {'Content-Type':'application/json', 'accept':'application/json', 'X-API-Key':API_KEY}
	req = UrlRequest('https://menstralhealthgameserver.herokuapp.com/api/' + endpoint, on_success=on_success, req_headers=headers, req_body=data)
	req.wait(delay=0.5)
	return req.result

def get_students_from_admin_id(id):
	return _api_call('users/admin/' + id)

# print request results from successful api call
def on_success(req, result):
	print('REQUEST SUCCESFUL', result)

# login
def login(email, password):
	try:
		auth = firebase.auth()
		user = auth.sign_in_with_email_and_password(email, password)
		return user
	except Exception as err:
		print("ERROR", err)

# logout
def logout(sm):
	try:
		sm.screens[0].ids.users = None
		sm.screens[0].ids.admin = None
		sm.current = 'login_screen'
	except Exception as err:
		print("ERROR", err)
