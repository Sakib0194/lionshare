#!/usr/bin/env python3
#find me at t.me/Sakib0194 if you are looking to create a bot
import requests, json, random, string, time, datetime, requests, mysql.connector, sys
import grab_data

class BoilerPlate:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=2):         #FOR GETTING UPDATES
        function = 'getUpdates'
        fieldss = {'timeout' : timeout, 'offset': offset}
        send = requests.get(self.api_url + function, fieldss)
        #print(send.json())
        result_json = send.json()['result']
        return result_json

    def send_message(self, chat_id, text, disable_web_page_preview=False):                  #FOR SENDING NORMAL MESSAGE
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'disable_web_page_preview':disable_web_page_preview}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send
    def send_message_two(self, chat_id, text, reply_markup, one_time_keyboard=False, resize_keyboard=True, disable_web_page_preview=True):         #FOR SENDING MESSAGE WITH KEYBOARD INCLUDED
        reply_markup = json.dumps({'keyboard': reply_markup, 'one_time_keyboard': one_time_keyboard, 'resize_keyboard': resize_keyboard, 'disable_web_page_preview':disable_web_page_preview})
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'reply_markup': reply_markup}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss).json()
        #print(send)
        return send

    def send_message_three(self, chat_id, text, remove_keyboard):               #FOR SENDING MESSAGES AND TO REMOVE KEYBOARD
        reply_markup = json.dumps({'remove_keyboard': remove_keyboard})
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'reply_markup': reply_markup}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss).json()
        return send   

    def send_message_four(self, chat_id, text, reply_markup, disable_web_page_preview=True):               #FOR SENDING MESSAGES WITH INLINE KEYBOARD
        reply_markup = json.dumps({'inline_keyboard': reply_markup})
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'reply_markup': reply_markup, 'disable_web_page_preview':disable_web_page_preview}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss)
        #print(send)
        #print(send.json)
        return send.json()

    def send_photo(self, chat_id, photo):
        fieldss = {'chat_id':chat_id, 'photo':photo}
        function = 'sendPhoto'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 

    def send_video(self, chat_id, video):
        fieldss = {'chat_id':chat_id, 'video':video}
        function = 'sendVideo'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 
    
    def send_document(self, chat_id, document):
        fieldss = {'chat_id':chat_id, 'document':document}
        function = 'sendDocument'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 

    def send_sticker(self, chat_id, sticker):
        fieldss = {'chat_id':chat_id, 'sticker':sticker}
        function = 'sendSticker'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 
    
    def InLineAnswer(self, inline_query_id, results):                   #FOR MANAGING INLINE REPLIES
        fieldss = {"inline_query_id": inline_query_id, "results" : results}
        function = 'answerInlineQuery'
        send = requests.post(self.api_url + function, fieldss)
        return send   

    def deleteWebhook(self):                #FOR DELETING WEBHOOK
        function = 'deleteWebhook'
        send = requests.post(self.api_url + function)
        return send

    def delete_message(self, group_id, message_id):         #FOR DELETING MESSAGES FROM GROUP
        fieldss = {'chat_id': group_id, 'message_id': message_id}
        function = 'deleteMessage'
        send = requests.post(self.api_url + function, fieldss)
        return send

    def get_admins(self, chat_id):              #ADMIN LIST IN A GROUP
        function = 'getChatAdministrators'
        fieldss = {'chat_id':chat_id}
        send = requests.get(self.api_url + function, fieldss)
        return send.json()['result']

    def edit_message (self, chat_id, message_id, text):
        fieldss = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'parse_mode':'MarkdownV2'}
        function = 'editMessageText'
        send = requests.post(self.api_url + function, fieldss)
        return send

    def edit_message_two (self, chat_id, message_id, text, reply_markup, disable_web_page_preview=True):
        reply_markup = json.dumps({'inline_keyboard': reply_markup})
        fieldss = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'parse_mode':'MarkdownV2', 'reply_markup':reply_markup, 'disable_web_page_preview':disable_web_page_preview}
        function = 'editMessageText'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send

details = sys.argv[1:]
conn = mysql.connector.connect(host=details[0],user=details[1],database=details[2],password=details[3], autocommit=True)
cur = conn.cursor()

token = grab_data.api_two(cur)
offset = 0

logged_in = []
special = ['[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

bot = BoilerPlate(token)

def starter():
    global offset, conn, cur
    while True:
        try:
            if conn.is_connected() == True:
                pass
            else:
                conn = mysql.connector.connect(host=details[0],user=details[1],database=details[2],password=details[3], autocommit=True)
                cur = conn.cursor()

            seen = grab_data.pending_seen(cur)
            if seen == []:
                pass
            else:
                all_admins = grab_data.all_admins(cur)
                for i in seen:
                    reply = grab_data.seen_reply(i, cur)
                    for a in all_admins:
                        message = reply
                        for u in special:
                            message = message.replace(u, f'\\{u}')
                        bot.send_message(a, f'Got Feedback: {message}')
                        grab_data.update_seen(i, cur)
            all_updates = bot.get_updates(offset)
            for current_updates in all_updates:
                #print(current_updates)
                update_id = current_updates['update_id']
                #bot.get_updates(offset = update_id+1)
                try:
                    if 'callback_query' in current_updates:
                        #print('inline keyboard detected')
                        sender_id = current_updates['callback_query']['from']['id']
                        group_id = current_updates['callback_query']['message']['chat']['id']
                        message_id = current_updates['callback_query']['message']['message_id']
                        callback_data = current_updates['callback_query']['data']
                        bot_message_handler(current_updates, update_id, message_id, sender_id, group_id, 0, cur, callback_data=callback_data, callback=True)
                    else:
                        group_id = current_updates['message']['chat']['id']
                        sender_id = current_updates['message']['from']['id']
                        message_id = current_updates['message']['message_id']
                        dict_checker = []
                        for keys in current_updates.get('message'):
                            dict_checker.append(keys)
                        if sender_id == group_id:
                            bot_message_handler(current_updates, update_id, message_id, sender_id, group_id, dict_checker, cur)
                except:
                    bot.get_updates(offset = update_id+1)
        except Exception as e:
            print(e)
            print('got an error')
            pass

def bot_message_handler(current_updates, update_id, message_id, sender_id, group_id, dict_checker, cur, callback_data=0, callback=False):
    try:
        if callback == True:
            print(callback_data)
            if callback_data == 'Nothing':
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Feedbacks' and sender_id in logged_in:
                pendings = grab_data.pending_feed(cur)
                if pendings == []:
                    bot.edit_message_two(group_id, message_id, 'No Feedback is Pending for a Reply', [[{'text':'Back', 'callback_data':'Back'}]])
                    bot.get_updates(offset = update_id+1)
                else:
                    full_text = f'Total Reply Pending : {len(pendings)}\n\nPending Message ID: '
                    for i in pendings:
                        full_text += f'{i}, '
                    full_text += '\n\nTo get Details of a Feedback send a message in the following manner\n\nfeedback messageid\nfeedback 1\nfeedback 28\nfeedback 15'
                    bot.edit_message_two(group_id, message_id, full_text, [[{'text':'Back', 'callback_data':'Back'}]])
                    bot.get_updates(offset = update_id+1)
            
            if callback_data == 'Back' and sender_id in logged_in:
                users = grab_data.all_users(cur)
                bot.edit_message_two(group_id, message_id, 'Admin Panel', [[{'text':f'Total User: {len(users)}', 'callback_data':'Nothing'}],
                                                                    [{'text':'Feedbacks', 'callback_data':'Feedbacks'}]])
                bot.get_updates(offset = update_id+1)

            if sender_id not in logged_in:
                bot.send_message(sender_id, 'Enter Your Password')
                bot.get_updates(offset = update_id+1)
        else:
            text = current_updates['message']['text']
            print(text)

            if text == '/start' and sender_id not in logged_in:
                bot.send_message(sender_id, 'Enter your Password')
                bot.get_updates(offset = update_id+1)
            
            elif text == '/start' and sender_id in logged_in:
                users = grab_data.all_users(cur)
                bot.send_message_four(sender_id, 'Admin Panel', [[{'text':f'Total User: {len(users)}', 'callback_data':'Nothing'}],
                                                                [{'text':'Feedbacks', 'callback_data':'Feedbacks'}]])
                bot.get_updates(offset = update_id+1)

            elif text == grab_data.feed_pass(sender_id, cur) and sender_id not in logged_in:
                bot.delete_message(sender_id, message_id)
                bot.send_message(sender_id, 'Access Granted')
                users = grab_data.all_users(cur)
                bot.send_message_four(sender_id, 'Admin Panel', [[{'text':f'Total User: {len(users)}', 'callback_data':'Nothing'}],
                                                                [{'text':'Feedbacks', 'callback_data':'Feedbacks'}]])
                logged_in.append(sender_id)
                bot.get_updates(offset = update_id+1)

            elif sender_id not in logged_in and text != grab_data.feed_pass(sender_id, cur):
                bot.send_message(sender_id, 'Access Failed')
                bot.get_updates(offset = update_id+1)

            if text.startswith('feedback') and sender_id in logged_in:
                mess = text.split(' ')[1]
                data = grab_data.feed_details(mess, cur)
                if data == []:
                    bot.send_message(sender_id, 'Invalid Message ID')
                    bot.get_updates(offset = update_id+1)
                else:
                    message = data[1]
                    for i in special:
                        message = message.replace(i, f'\\{i}')
                    bot.send_message(sender_id, f'Telegram ID: {data[0]}\nFeedback Message: {message}\nMessage ID: {data[2]}\n\nTo send a reply to this Feedback type\nMessageID Message\nExample\n\1 what you want to send')
                    bot.get_updates(offset = update_id+1)

            if text.split(' ')[0].isnumeric():
                message_id = text.split(' ')[0]
                message = text.split(' ')[1:]
                full_text = ""
                for i in message:
                    full_text += f"{i} "
                for i in special:
                    full_text = full_text.replace(i, f'\\{i}')
                grab_data.feedback_reply(message_id, full_text, cur)
                bot.send_message(sender_id, 'Feedback Reply Sent')
                bot.get_updates(offset = update_id+1)

    except Exception as e:
        print(e)
        bot.get_updates(offset = update_id+1)
        pass

starter()