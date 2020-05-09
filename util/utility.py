from util.client import api_call, authorize
import json

class Utility(object):
    def __init__(self):
        self.username = ''
        self.password = ''

        # authorize / acuire key on startup
        authorize()



