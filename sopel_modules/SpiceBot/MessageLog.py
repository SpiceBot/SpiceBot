# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Message Log system.
"""

import uuid


class MessageLog():

    def __init__(self):
        self.dict = {}
        self.message_display = dict()
        self.used_ids = [0]
        self.error_message_dict = {
                                    "command_inchan_only": "$command must be run in channel.",
                                    "admin_switch_unauth": "The admin switch (-a) is for use by authorized nicks ONLY.",
                                    }

    def messagelog_assign(self):
        unique_id = 0
        while unique_id in self.used_ids:
            unique_id = uuid.uuid4()
        self.used_ids.append(unique_id)
        return unique_id

    def messagelog_start(self, bot, trigger, log_id):

        if not trigger.is_privmsg:
            channelname = None
        else:
            channelname = trigger.sender

        self.message_display[log_id] = {
                                        "trigger": {
                                                "nick": trigger.nick,
                                                "sender": channelname,
                                                },
                                        "bot": {
                                                "nick": bot.nick
                                                },
                                        "messages": [],
                                        }

    def messagelog_error(self, log_id, error_id):

        newloglist = []
        error_exists_prior = False

        for existing_messagedict in self.message_display[log_id]["messages"]:
            if existing_messagedict["type"] == "error":
                if existing_messagedict["error_id"] == error_id:
                    error_exists_prior = True
                    existing_messagedict["count"] += 1
            newloglist.append(existing_messagedict)

        if not error_exists_prior:
            newmessagedict = {"type": "error", "error_id": error_id, "count": 1}
            newloglist.append(newmessagedict)

        self.message_display[log_id]["messages"] = newloglist

    def messagelog(self, log_id, message, recipients=None):

        if not recipients:
            if self.message_display[log_id]["trigger"]["sender"]:
                recipients = self.message_display[log_id]["trigger"]["sender"]
            else:
                recipients = self.message_display[log_id]["trigger"]["nick"]

        messagedict = {"type": "normal", "message": message, "recipients": recipients}

        self.message_display[log_id]["messages"].append(messagedict)

    def messagelog_exit(self, bot, log_id):

        current_messages = []
        current_errors = []

        for messagedict in self.message_display[log_id]["messages"]:

            if messagedict["type"] == "error":
                if messagedict["error_id"] not in self.error_message_dict.keys():
                    message = "Error missing for ID '" + str(messagedict["error_id"]) + "'"
                else:
                    message = self.error_message_dict[messagedict["error_id"]]
                message += " (" + str(messagedict["count"]) + ")"
                message = self.messagelog_fillin(bot, message, log_id)
                current_errors.append(message)
            else:
                if len(current_errors):
                    currenterrordict = {"type": "error", "message": current_errors}
                    current_messages.append(currenterrordict)
                    current_errors = []
                message = messagedict["message"]
                current_messages.append(messagedict)
        if len(current_errors):
            currenterrordict = {"type": "error", "message": current_errors}
            current_messages.append(currenterrordict)
            current_errors = []

        for messagedict in current_messages:
            if messagedict["type"] == 'error':
                bot.osd(messagedict['message'], self.message_display[log_id]["trigger"]["nick"], 'notice')
            else:
                bot.osd(messagedict['message'], messagedict["recipients"], 'say')

        self.messagelog_kill(log_id)

    def messagelog_fillin(self, message, log_id):

        for botval in ["nick"]:
            fullbotval = str("$bot." + botval)
            fullbotvaleval = self.message_display[log_id]["bot"][botval]
            if fullbotval in message:
                message = str(message.replace(fullbotval, fullbotvaleval))

        for triggerval in ["nick", "sender"]:
            fulltriggerval = str("$trigger." + triggerval)
            fulltriggervaleval = self.message_display[log_id]["trigger"][triggerval]
            if fulltriggerval in message:
                if fulltriggervaleval:
                    message = str(message.replace(fulltriggerval, fulltriggervaleval))
                else:
                    if triggerval == "sender":
                        message = str(message.replace("$trigger.sender", 'privmsg'))
                    else:
                        message = str(message.replace(fulltriggerval, str(fulltriggervaleval)))

        return message

    def messagelog_kill(self, log_id):
        if log_id in self.message_display:
            del self.message_display[log_id]


messagelog = MessageLog()
