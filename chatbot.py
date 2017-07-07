from flask import Flask, request
from wit import Wit
import requests
import json
import traceback
import random

import keys

app = Flask(__name__)

witClient = Wit(access_token=keys.witToken)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data)
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
      response = witClient.message(text) # Outgoing Message Text
      payload = {'status': '200 OK', 'recipient': {'id': sender}, 'message': {'text': response}}
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + keys.fbToken, json=payload)
    except Exception as e:
      print(traceback.format_exception())

  elif request.method == 'GET': # For initial verification
    if request.args.get('hub.verify_token') == 'Hello World':
      return request.args.get('hub.challenge')
    return 'Wrong Verify Token'

if __name__ == '__main__':
  app.run(debug=True)
