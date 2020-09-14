import pyrebase

config = {
"apiKey": "AIzaSyCJi80zlhnrj8noZtO7uPwOxnMDX-XLmyM",
  "authDomain": "menstrual-health-game.firebaseapp.com",
  "databaseURL": "https://menstrual-health-game.firebaseio.com",
  "projectId": "menstrual-health-game",
  "storageBucket": "menstrual-health-game.appspot.com",
  "messagingSenderId": "763317516525",
  "appId": "1:763317516525:web:1b3e47b1e893223c7834e4"
}

firebase = pyrebase.initialize_app(config)
