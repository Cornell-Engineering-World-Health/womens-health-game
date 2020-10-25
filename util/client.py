import urllib
import os
import json
import threading
from kivy.network.urlrequest import UrlRequest
from util.firebase import firebase


API_KEY = ' '

# KEY REQUEST

# read and parse key.json
def get_options():
	util = os.path.dirname(os.path.abspath(__file__))
	key_json = os.path.join(util, 'key.json')
	with open(key_json) as o:
		data = json.load(o)
	return data

# main authorize function
def authorize():
	options = get_options()
	body = json.dumps(options['body'])
	req = UrlRequest(options['url'], on_success=get_key, on_failure=error_msg, req_headers=options['headers'], req_body=body)

# acquire key from successful authorize response
def get_key(req, result):
	print('API_KEY ACQUIRED')
	global API_KEY
	API_KEY = result['token_type'] + ' ' + result['access_token']

# print error msg from failed authorize response
def error_msg(req, result):
	print('ERROR', result)


# API REQUESTS

# takes in endpoint and optional data
def _api_call(endpoint, data=None):
	headers = {'Content-Type':'application/json', 'accept':'application/json', 'Authorization':API_KEY}
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
