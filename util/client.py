import ssl
import urllib
import os
import json
import threading
from kivy.network.urlrequest import UrlRequest
from util.firebase import firebase
from dotenv import load_dotenv
from util.store import update_admin_state, clear_game_state, current_state, new_user

load_dotenv()
API_KEY = os.getenv('API_KEY')


# API REQUESTS

# takes in endpoint and optional data
def _api_call(endpoint, data=None):
	headers = {'Content-Type':'application/json', 'accept':'application/json', 'X-API-Key':API_KEY}
	req = UrlRequest('https://healthfriendgameserver.herokuapp.com/api/' + endpoint, on_success=on_success, on_failure=on_failure, req_headers=headers, req_body=data)
	req.wait(delay=0.5)
	return req.result

def _put_api_call(endpoint, data):
	headers = {'Content-Type':'application/json', 'accept':'application/json', 'X-API-Key':API_KEY}
	req = UrlRequest('https://healthfriendgameserver.herokuapp.com/api/' + endpoint, on_success=on_success, on_failure=on_failure, req_headers=headers, req_body=data, method='PUT')
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
	json_obj = json.dumps(new_state)
	print("UPDATE_STATE\n")
	print("**(STATE)**", json_obj)
	user_state = get_state_from_user_id(id)
	if user_state is None:
		res = post_state(json_obj)
	else:
		res = _put_api_call('state/user/' + id, json_obj)
	return res

# GET API CALL for api/admin/:admin_id
def get_students_from_admin_id(id):
	return _api_call('users/admin/' + id)

# print request results from successful api call
def on_success(req, result):
	print('request successful', result)

# print request results from failed api call
def on_failure(req, result):
	print('request failed', result)

def update_local_state(users):
	for user in users:
		state = get_state_from_user_id(user['_id'])
		new_user(user['_id'], state)

def add_local_state_to_backend():
	state = current_state()
	try:
		for user in state:
			game_state = state[user]['game_state']
			for module in range(len(game_state)):
				update_state(user, game_state[module])
		return True
	except Exception as err:
		print("ERROR UPDATING BACKEND WITH LOCAL STATE", err)
		return False

# login
def login(email, password):
		auth = firebase.auth()

		#try to login, and cut function short if unsuccessful
		try:
			auth.sign_in_with_email_and_password(email, password)
		except:
			return False, "login_failure"

		#try to make our backend requests to get the users based on the person who logged in
		try:
			users = get_students_from_admin_id(admin['localId'])
			update_local_state(users)
			update_admin_state(admin, users)
		except:
			return False, "network_failure"

		return True, ""

def clear_state(sm):
	did_upload = add_local_state_to_backend()
	if did_upload:
		clear_game_state()
		update_admin_state(None, None)

# logout
def logout(sm):
	try:
		clear_state(sm)
		sm.current = 'login_screen'
	except Exception as err:
		print("ERROR", err)
