import os
import sys
import json
from datetime import datetime
from fb_api import send_message

import requests
from flask import Flask, request
import flow_0

app = Flask(__name__)
last_message = {}
current_flow = {}


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    #log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    #recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if message_text == "Test":
                        current_flow[sender_id] = "flow_0"
                        flow_0.start(sender_id, last_message)
                    elif sender_id in last_message:
                        if current_flow[sender_id] == "flow_0":
                            flow_0.talk(sender_id, last_message, messaging_event)
                    else:
                        send_message(sender_id, "roger that!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


@app.route('/hello', methods=['GET'])
def say_hello():
    sender_id = '2537414029616995'
    send_message(sender_id, "Hello!")
    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)
