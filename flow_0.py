from dateutil import parser
from fb_api import *


def start(sender_id, last_message):
    send_message(sender_id, "Hi Carlos! Welcome to week 7!")
    send_typing(sender_id)
    send_message(sender_id, "Your goal this week will be planning the semester, week-by-week "
                            "progress, and the intermediate milestones that you’ll use to get "
                            "feedback from your classmates and mentor as you go along.")
    send_typing(sender_id)
    send_message(sender_id, "Your key deliverables for this week are:")
    send_typing(sender_id)
    send_message(sender_id, "1) Project Proposal")
    send_typing(sender_id)
    send_message(sender_id, "2) Peer reviews on Qualifier Question")
    send_typing(sender_id)
    send_message(sender_id, "To deliver great work, it's important to plan in advance.")
    send_typing(sender_id)
    send_message(sender_id, "First, let's plan the project proposal. It's expected 3-5 hours to "
                            "complete it.")
    send_typing(sender_id)
    send_message(sender_id, "Which days are you planning to work on the project proposal?", last_message, 0)


def talk(sender_id, last_message, messaging_event):
    message_text = messaging_event["message"]["text"]

    if last_message[sender_id] == 0:
        entities = messaging_event["message"]["nlp"]["entities"]
        if "datetime" in entities:
            msg = ""
            last_dt = None
            for item in entities["datetime"]:
                dt = parser.parse(item["value"])
                if dt != last_dt:
                    msg += dt.strftime("%A, %B %d") + " and "
                last_dt = dt

            msg = msg[0:len(msg) - 5]
            send_quick_yes_no(sender_id, "Do you want me to remind you on " + msg + "?", last_message, 1)
        else:
            send_message(sender_id, "I didn't understand. Please repeat. You can say Thursday, Saturday, next Monday, "
                                    "Fri, etc.")
            send_message(sender_id, "Which days are you planning to work on the project proposal?", last_message, 0)

    #elif last_message[sender_id][0:30] == "Do you want me to remind you o":
    elif last_message[sender_id] == 1:
        if message_text not in ["Yes", "No"]:
            send_message(sender_id, "I didn't understand.")
            send_quick_yes_no(sender_id, "Do you want me to remind you on these dates?", last_message, 1)
        else:
            if message_text == "Yes":
                send_message(sender_id, "Ok, will do it!")
            elif message_text == "No":
                send_message(sender_id, "No worries!")

            send_message(sender_id, "Now, let's plan peer reviews. It's expected 1-2 hours to complete it.")

            quick_replies = [{"content_type": "text", "title": "Before Thursday", "payload": "before_thursday"},
                             {"content_type": "text", "title": "Before Sunday", "payload": "before_sunday"},
                             {"content_type": "text", "title": "After 7 days", "payload": "after_7_days"}]
            send_quick_replies(sender_id, "When do you plan to finish all peer reviews?", quick_replies, last_message,
                               2)

    elif last_message[sender_id] == 2:
        if message_text not in ["Before Thursday", "Before Sunday", "After 7 days"]:
            send_message(sender_id, "I didn't understand.")
            quick_replies = [{"content_type": "text", "title": "Before Thursday", "payload": "before_thursday"},
                             {"content_type": "text", "title": "Before Sunday", "payload": "before_sunday"},
                             {"content_type": "text", "title": "After 7 days", "payload": "after_7_days"}]
            send_quick_replies(sender_id, "When do you plan to finish all peer reviews?", quick_replies, last_message,
                               2)
        elif message_text == "After 7 days":
            send_quick_yes_no(sender_id, "That's really not ideal for your peers and you. Are you sure?", last_message,
                              3)
        else:
            if message_text == "Before Thursday":
                send_message(sender_id, "That's great: you will help your peers and earn all possible points!")
            elif message_text == "Before Sunday":
                send_message(sender_id, "Well, that's not ideal, but I'm sure you will do your best to finish earlier.")

            send_quick_yes_no(sender_id, "Do you want me to remind you to work on it?", last_message, 4)

    elif last_message[sender_id] == 3:
        if message_text not in ["Yes", "No"]:
            send_message(sender_id, "I didn't understand.")
            send_quick_yes_no(sender_id, "That's really not ideal for your peers and you. Are you sure?", last_message,
                              3)
        else:
            if message_text == "Yes":
                send_quick_yes_no(sender_id, "Do you want me to remind you to work on it?", last_message, 4)
            elif message_text == "No":
                send_message(sender_id, "Great that you changed your mind! Let me ask you again.")
                quick_replies = [{"content_type": "text", "title": "Before Thursday", "payload": "before_thursday"},
                                 {"content_type": "text", "title": "Before Sunday", "payload": "before_sunday"},
                                 {"content_type": "text", "title": "After 7 days", "payload": "after_7_days"}]
                send_quick_replies(sender_id, "When do you plan to finish all peer reviews?", quick_replies,
                                   last_message, 2)

    elif last_message[sender_id] == 4:
        if message_text not in ["Yes", "No"]:
            send_message(sender_id, "I didn't understand.")
            send_quick_yes_no(sender_id, "Do you want me to remind you to work on it?", last_message, 4)
        else:
            if message_text == "Yes":
                send_message(sender_id, "Ok, will do it!")
            elif message_text == "No":
                send_message(sender_id, "No worries!")

            send_message(sender_id, "Now, to end our interaction today, check the 2min video below about "
                                    "Neuroplasticity and how your brain works:")
            send_video(sender_id, "2266022390306094")
            send_quick_yes_no(sender_id, "Did you like the video?", last_message, 5)

    elif last_message[sender_id] == 5:
        if message_text not in ["Yes", "No"]:
            send_message(sender_id, "I didn't understand.")
            send_quick_yes_no(sender_id, "Did you like the video?", last_message, 5)
        else:
            if message_text == "Yes":
                send_message(sender_id, "Great to hear!")
                send_message(sender_id, "Can you tell me in few words what did you learn about how your brain works?",
                             last_message, 6)
            elif message_text == "No":
                send_message(sender_id, "Sorry to hear that.")
                send_message(sender_id, "Can you tell me in one sentence why didn't you like it and what did you "
                                        "learn?", last_message, 6)

    elif last_message[sender_id] == 6:
        send_message(sender_id, "Understood!")
        send_quick_yes_no(sender_id, "Do you want me to post that into Piazza's Friday Reflections thread?",
                          last_message, 7)

    elif last_message[sender_id] == 7:
        if message_text not in ["Yes", "No"]:
            send_message(sender_id, "I didn't understand.")
            send_quick_yes_no(sender_id, "Do you want me to post that into Piazza's Friday Reflections thread?",
                              last_message, 7)
        else:
            if message_text == "Yes":
                send_message(sender_id, "Done!")
            elif message_text == "No":
                send_message(sender_id, "No worries!")

            send_message(sender_id, "Carlos, thanks for the interaction! We will catch up tomorrow.")
            send_message(sender_id, "Have a great day!")

            last_message.pop(sender_id)     # resets the flow

    else:
        send_message(sender_id, "Hi! I didn't understand your input. Please type 'Test' to experiment Flow 0")
