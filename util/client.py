import ssl
import urllib
import os
import json
import threading
from kivy.network.urlrequest import UrlRequest
from util.firebase import firebase
from dotenv import load_dotenv
from util.store import update_admin_state


load_dotenv()
API_KEY = os.getenv('API_KEY')


# API REQUESTS

# takes in endpoint and optional data
def _api_call(endpoint, data=None):
	headers = {'Content-Type':'application/json', 'accept':'application/json', 'X-API-Key':API_KEY}
	req = UrlRequest('https://healthfriendgameserver.herokuapp.com/api/' + endpoint, on_success=on_success, req_headers=headers, req_body=data)
	req.wait(delay=0.5)
	return req.result

# GET API CALL for api/state/user/:user_id
def get_state_from_user_id(id):
	return  _api_call('state/user/' + id)

# POST API CALL for api/state
def post_state(new_state):
	return  _api_call('state', data=new_state)

# PUT API CALL for api/state/user/:user_id
def update_state(id, new_state):
	new_state['user_id'] = id
	json_obj = json.dumps(new_state, indent = 4)
	print("**(STATE)**", json_obj)
	user_state = get_state_from_user_id(id)
	if(not user_state):
		res = post_state(json_obj)
	else:
		res = _api_call('state/user/' + id, json_obj)
	return res

# GET API CALL for api/admin/:admin_id
def get_students_from_admin_id(id):
	return _api_call('users/admin/' + id)

# print request results from successful api call
def on_success(req, result):
	print('request successful', result)

# login
def login(email, password):
	try:
		auth = firebase.auth()
		admin = auth.sign_in_with_email_and_password(email, password)
		users = get_students_from_admin_id(admin['localId'])
		update_admin_state(admin, users)
		return admin
	except Exception as err:
		print("ERROR", err)

# logout
def logout(sm):
	try:
		sm.screens[1].ids.admin = None
		update_admin_state(None, None)
		sm.current = 'login_screen'
	except Exception as err:
		print("ERROR", err)
