#!/usr/bin/env python3
import requests, json, random, string, time, datetime, requests, mysql.connector, sys
import grab_data

class BoilerPlate:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=10000):         #FOR GETTING UPDATES
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
        print(send.json)
        return send.json()

    def send_photo(self, chat_id, photo):
        fieldss = {'chat_id':chat_id, 'photo':photo}
        function = 'sendPhoto'
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
        print(send.json())
        return send

details = sys.argv[1:]
conn = mysql.connector.connect(host=details[0],user=details[1],database=details[2],password=details[3], autocommit=True)
cur = conn.cursor()

token = grab_data.api(cur)
offset = 0

texts = {}
buttons = {}
all_te = grab_data.lang('English', cur)
all_bu = grab_data.buttons('English', cur)
for i in range(len(all_te)):
    texts[str(i)] = all_te[i]
for i in range(len(all_bu)):
    buttons[str(i)] = all_bu[i]
special = ['@', '=', '.', '>', '-', '(', ')']

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
            if callback_data == 'English' or callback_data == 'Hindi' or callback_data == 'Spanish':
                all_texts = grab_data.lang(callback_data, cur)
                all_buttons = grab_data.buttons(callback_data, cur)
                for i in range(len(all_texts)):
                    texts[str(i)] = all_texts[i]
                for i in range(len(all_buttons)):
                    buttons[str(i)] = all_buttons[i]
                bot.send_message_two(sender_id, texts['0'], [[(buttons['0'])], [(buttons['1'])], [(buttons['3'])], [(buttons['2'])]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Mobile Regi':
                button1 = buttons['6']
                button2 = buttons['7']
                button3 = buttons['9']
                bot.edit_message_two(group_id, message_id, (texts['1']), [[{'text':f'{button1}', 'callback_data':'Have Wallet'}],
                                                                        [{'text':f'{button2}', 'callback_data':'No Wallet'}],
                                                                        [{'text':f'{button3}', 'callback_data':'Manual'}]])
                bot.get_updates(offset = update_id+1)
            
            if callback_data == 'PC Regi':
                button1 = buttons['8']
                button2 = buttons['9']
                bot.edit_message_two(group_id, message_id, (texts['1']), [[{'text':f'{button1}', 'callback_data':'Tronlink'}],
                                                                        [{'text':f'{button2}', 'callback_data':'Manual'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'No Wallet':
                message = texts['5']
                button1 = buttons['11']
                button2 = buttons['12']
                button3 = buttons['13']
                bot.send_message(sender_id, 'Photo here')
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Create Tron':
                message = texts['3']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['11']
                button2 = buttons['12']
                button3 = buttons['13']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Topping Up':
                message = texts['4']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['11']
                button2 = buttons['12']
                button3 = buttons['13']
                bot.send_message(sender_id, 'Video here')
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Complete Regi':
                message = texts['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['14']
                bot.send_message(sender_id, 'Photo here')
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)
            
            if callback_data == 'Finalize':
                bot.edit_message(group_id, message_id, (texts['7']))
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Have Wallet':
                message = texts['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['14']
                bot.send_message(sender_id, 'Photo here')
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Manual':
                message = texts['8']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                bot.edit_message(group_id, message_id, message)
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Tronlink':
                button1 = buttons['15']
                button2 = buttons['16']
                button3 = buttons['13']
                bot.send_message(sender_id, 'Photo here')
                bot.send_message_four(sender_id, (texts['5']), [[{'text':f'{button1}', 'callback_data':'Create Tronlink'}],
                                                                [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                                [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)
            
            if callback_data == 'Create Tronlink':
                message = texts['9']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['15']
                button2 = buttons['16']
                button3 = buttons['13']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tronlink'}],
                                                                [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                                [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

        else:
            text = current_updates['message']['text']
            print(text)
            if text == '/start' or text == 'start':
                bot.send_message_four(sender_id, 'Select a Language', [[{'text':'English', 'callback_data':'English'}],
                                                                    [{'text':'Hindi', 'callback_data':'Hindi'}],
                                                                    [{'text':'Spanish', 'callback_data':'Spanish'}]])
                bot.get_updates(offset = update_id+1)

            if text == buttons['0']:
                button1 = buttons['4']
                button2 = buttons['5']
                button3 = buttons['10']
                bot.send_message_two(sender_id, (texts['2']), [[button3]])
                bot.send_message_four(sender_id, (texts['1']), [[{'text':f'{button1}', 'callback_data':'Mobile Regi'}],
                                                            [{'text':f'{button2}', 'callback_data':'PC Regi'}]])
                bot.get_updates(offset = update_id+1)

            if text == buttons['10']:
                bot.send_message_two(sender_id, texts['0'], [[(buttons['0'])], [(buttons['1'])], [(buttons['3'])], [(buttons['2'])]])
                bot.get_updates(offset = update_id+1)

    except Exception as e:
        print(e)
        bot.get_updates(offset = update_id+1)
        pass

starter()