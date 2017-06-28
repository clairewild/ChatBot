from flask import Flask, request
import requests
import json
import traceback
import random

app = Flask(__name__)

token = "EAAMKk8tUJe4BAKheQjTq9Cs1vdXq0LNZC19cR2ZBnt0vZBnW1dsbu43yI5i2bUhZBmSuXV6P6gb1LWLurbFZBopPKZAStZCvx1HSr0KnKgfz1mT79sLiZClfTZBZBvoR1AKYRBHmgBPArH99xHSTsq2JZCrLYj4zUMDxjaNZAqif7koEYgZDZD"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data)
      text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      payload = {'recipient': {'id': sender}, 'message': {'text': "Hello World"}} # We're going to send this back
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
    except Exception as e:
      print(traceback.format_exception()) # something went wrong

  elif request.method == 'GET': # For the initial verification
    if request.args.get('hub.verify_token') == 'Hello World':
      return request.args.get('hub.challenge')
    return "Wrong Verify Token"
    
  return "Hello World"

if __name__ == '__main__':
  app.run(debug=True)
