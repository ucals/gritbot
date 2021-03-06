import os
import sys
import json
from datetime import datetime
import requests
import time


def send_message(recipient_id, message_text, last_message={}, message_number=-1):
    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    #last_message[recipient_id] = message_text
    last_message[recipient_id] = message_number
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_quick_replies(recipient_id, message_text, quick_replies, last_message={}, message_number=-1):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
            "quick_replies": quick_replies
        }
    })
    #last_message[recipient_id] = message_text
    last_message[recipient_id] = message_number
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_quick_yes_no(recipient_id, message_text, last_message={}, message_number=-1):
    quick_replies = [{
        "content_type": "text",
        "title": "Yes",
        "payload": "yes"},
        {
            "content_type": "text",
            "title": "No",
            "payload": "no"
        }
    ]
    send_quick_replies(recipient_id, message_text, quick_replies, last_message, message_number)


def send_video(recipient_id, video_id, last_message={}, message_number=-1):
    log("sending video to {recipient}: {text}".format(recipient=recipient_id, text=video_id))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "media",
                    "elements": [
                        {
                            "media_type": "video",
                            "attachment_id": video_id
                        }
                    ]
                }
            }
        }
    })
    #last_message[recipient_id] = video_id
    last_message[recipient_id] = message_number
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_typing(recipient_id, delay=0):
    log("sending typing indicator to {recipient}".format(recipient=recipient_id))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "typing_on"
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    # time.sleep(delay)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def retrieve_profile_name(psid):
    r = requests.get("https://graph.facebook.com/" + psid + "?fields=first_name,last_name&access_token=" +
                      os.environ["PAGE_ACCESS_TOKEN"])
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return "Error"
    else:
        return r.json()['first_name']


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = (msg).format(*args, **kwargs)
        print(u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()
