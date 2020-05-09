import urllib
import os
import json
import threading
import asyncio
from kivy.network.urlrequest import UrlRequest

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
	# call authorize() every 120 seconds
	threading.Timer(120, authorize).start()
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
	print('ERROR')
	print(result)


# API REQUESTS

# takes in endpoint and optional data
def api_call(endpoint, data=None):
	headers = {'Content-Type':'application/json', 'accept':'application/json', 'Authorization':API_KEY}
	req = UrlRequest('https://menstralhealthgameserver.herokuapp.com/api/' + endpoint, on_success=print_results, req_headers=headers, req_body=data)
	print_results(req, result)

# print request results from successful api call
def print_results(req, result):
	print('REQUEST SUCCESFUL')
	print(result)

result = ''

