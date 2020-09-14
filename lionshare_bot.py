#!/usr/bin/env python3
#find me at t.me/Sakib0194 if you are looking to create a bot
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
        print(send)
        print(send.json)
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
        print(send.json())
        return send 
    
    def send_document(self, chat_id, document):
        fieldss = {'chat_id':chat_id, 'document':document}
        function = 'sendDocument'
        send = requests.post(self.api_url + function, fieldss)
        print(send.json())
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

current_lang = 'English'
texts = {}
buttons = {}
all_te = grab_data.lang('English', cur)
all_bu = grab_data.buttons('English', cur)
for i in range(len(all_te)):
    texts[str(i)] = all_te[i]
for i in range(len(all_bu)):
    buttons[str(i)] = all_bu[i]
special = ['@', '=', '.', '>', '-', '(', ')','!']

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
                print(current_updates)
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
    global current_lang
    try:
        if callback == True:
            print(callback_data)
            if callback_data == 'Nothing' or callback_data == 'Zoom Video' or callback_data == 'Promotion Video' or callback_data == 'Introduction':
                bot.get_updates(offset = update_id+1)

            if callback_data == 'English' or callback_data == 'Hindi' or callback_data == 'Spanish':
                all_texts = grab_data.lang(callback_data, cur)
                all_buttons = grab_data.buttons(callback_data, cur)
                for i in range(len(all_texts)):
                    texts[str(i)] = all_texts[i]
                for i in range(len(all_buttons)):
                    buttons[str(i)] = all_buttons[i]
                current_lang = callback_data
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
            
            elif callback_data == 'PC Regi':
                button1 = buttons['8']
                button2 = buttons['9']
                bot.edit_message_two(group_id, message_id, (texts['1']), [[{'text':f'{button1}', 'callback_data':'Tronlink'}],
                                                                        [{'text':f'{button2}', 'callback_data':'Manual'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'No Wallet':
                message = texts['5']
                button1 = buttons['11']
                button2 = buttons['12']
                button3 = buttons['13']
                photo = grab_data.links('photo 1', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Create Tron':
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

            elif callback_data == 'Topping Up':
                message = texts['4']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['11']
                button2 = buttons['12']
                button3 = buttons['13']
                video = grab_data.links('video 1', cur)
                bot.send_video(sender_id, video)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Complete Regi':
                message = texts['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['14']
                photo = grab_data.links('photo 2', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Complete Regi PC':
                message = texts['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['14']
                photo = grab_data.links('photo 4', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Finalize':
                bot.edit_message(group_id, message_id, (texts['7']))
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Have Wallet':
                message = texts['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['14']
                photo = grab_data.links('photo 2', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Manual':
                message = texts['8']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                bot.edit_message(group_id, message_id, message)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Tronlink':
                button1 = buttons['15']
                button2 = buttons['16']
                button3 = buttons['13']
                photo = grab_data.links('photo 3', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, (texts['5']), [[{'text':f'{button1}', 'callback_data':'Create Tronlink'}],
                                                                [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                                [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Create Tronlink':
                message = texts['9']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons['15']
                button2 = buttons['16']
                button3 = buttons['13']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tronlink'}],
                                                                [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                                [{'text':f'{button3}', 'callback_data':'Complete Regi PC'}]])
                bot.get_updates(offset = update_id+1)


            if callback_data == 'Page 1':
                message = texts['12']
                button1 = buttons['22']
                button2 = buttons['23']
                button3 = buttons['24']
                button4 = buttons['25']
                button5 = buttons['26']
                button6 = buttons['27']
                button7 = buttons['28']
                button8 = buttons['29']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Answer 13'}],
                                                                [{'text':f'{button2}', 'callback_data':'Answer 14'}],
                                                                [{'text':f'{button3}', 'callback_data':'Answer 15'}],
                                                                [{'text':f'{button4}', 'callback_data':'Answer 16'}],
                                                                [{'text':f'{button5}', 'callback_data':'Answer 17'}],
                                                                [{'text':f'{button6}', 'callback_data':'Answer 18'}],
                                                                [{'text':f'{button7}', 'callback_data':'Answer 19'}],
                                                                [{'text':f'{button8}', 'callback_data':'Answer 20'}],
                                                                [{'text':'<', 'callback_data':'Page 3'}, {'text':'Page 1', 'callback_data':'Nothing'}, {'text':'>', 'callback_data':'Page 2'}],
                                                                [{'text':'Back', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Page 2':
                message = texts['12']
                button1 = buttons['30']
                button2 = buttons['31']
                button3 = buttons['32']
                button4 = buttons['33']
                button5 = buttons['34']
                button6 = buttons['35']
                button7 = buttons['36']
                button8 = buttons['37']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Answer 21'}],
                                                                [{'text':f'{button2}', 'callback_data':'Answer 22'}],
                                                                [{'text':f'{button3}', 'callback_data':'Answer 23'}],
                                                                [{'text':f'{button4}', 'callback_data':'Answer 24'}],
                                                                [{'text':f'{button5}', 'callback_data':'Answer 25'}],
                                                                [{'text':f'{button6}', 'callback_data':'Answer 26'}],
                                                                [{'text':f'{button7}', 'callback_data':'Answer 27'}],
                                                                [{'text':f'{button8}', 'callback_data':'Answer 28'}],
                                                                [{'text':'<', 'callback_data':'Page 1'}, {'text':'Page 2', 'callback_data':'Nothing'}, {'text':'>', 'callback_data':'Page 3'}],
                                                                [{'text':'Back', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Page 3':
                message = texts['12']
                button1 = buttons['38']
                button2 = buttons['39']
                button3 = buttons['40']
                button4 = buttons['41']
                button5 = buttons['42']
                button6 = buttons['43']
                button7 = buttons['44']
                button8 = buttons['45']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Answer 29'}],
                                                                [{'text':f'{button2}', 'callback_data':'Answer 30'}],
                                                                [{'text':f'{button3}', 'callback_data':'Answer 31'}],
                                                                [{'text':f'{button4}', 'callback_data':'Answer 32'}],
                                                                [{'text':f'{button5}', 'callback_data':'Answer 33'}],
                                                                [{'text':f'{button6}', 'callback_data':'Answer 34'}],
                                                                [{'text':f'{button7}', 'callback_data':'Answer 35'}],
                                                                [{'text':f'{button8}', 'callback_data':'Answer 36'}],
                                                                [{'text':'<', 'callback_data':'Page 2'}, {'text':'Page 3', 'callback_data':'Nothing'}, {'text':'>', 'callback_data':'Page 1'}],
                                                                [{'text':'Back', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Back':
                button1 = buttons['10']
                button2 = buttons['17']
                button3 = buttons['18']
                button4 = buttons['19']
                button5 = buttons['20']
                button6 = buttons['21']
                button7 = buttons['46']
                bot.edit_message_two(group_id, message_id, texts['11'], [[{'text':f'{button7}', 'callback_data':'Intro Video'}],
                                                                [{'text':f'{button2}', 'callback_data':'Introduction'}],
                                                                [{'text':f'{button3}', 'callback_data':'Zoom Video'}],
                                                                [{'text':f'{button4}', 'callback_data':'Promotion Video'}],
                                                                [{'text':f'{button5}', 'callback_data':'Page 1'}],
                                                                [{'text':f'{button6}', 'callback_data':'Nothing'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Intro Video':
                video = grab_data.links('video 2', cur)
                bot.send_video(sender_id, video)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Zoom Video':
                link1 = grab_data.links('video zoom', cur)
                link2 = grab_data.links('video zoom 2', cur)
                bot.send_video(sender_id, link1)
                bot.send_video(sender_id, link2)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Introduction':
                button1 = buttons['47']
                button2 = buttons['48']
                bot.edit_message_two(group_id, message_id, texts['38'], [[{'text':f'{button1}', 'callback_data':'Intro Eng'}],
                                                                        [{'text':f'{button2}', 'callback_data':'Intro Afr'}],
                                                                        [{'text':'Back', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Promotion Video':
                button1 = buttons['49']
                button2 = buttons['50']
                button3 = buttons['51']
                bot.edit_message_two(group_id, message_id, texts['39'], [[{'text':f'{button1}', 'callback_data':'Promo Vid'}],
                                                                        [{'text':f'{button2}', 'callback_data':'Promo Pic'}],
                                                                        [{'text':f'{button3}', 'callback_data':'Stickers'}],
                                                                        [{'text':'Back', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Promo Vid':
                all_links = []
                for i in range(3,11):
                    video = grab_data.links(f'video {i}', cur)
                    all_links.append(video[0])
                print(all_links)
                for i in all_links:
                    bot.send_video(sender_id, i)

                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Promo Pic':
                #video = grab_data.links('video 3', cur)
                #bot.send_video(sender_id, video)
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Stickers':
                #video = grab_data.links('video 3', cur)
                #bot.send_video(sender_id, video)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Intro Eng':
                document = grab_data.links('document 1', cur)
                bot.send_document(sender_id, document)
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Intro Afr':
                document = grab_data.links('document 2', cur)
                bot.send_document(sender_id, document)
                bot.get_updates(offset = update_id+1)

            if callback_data.startswith('Answer'):
                number = callback_data.split(' ')[1]
                reply = grab_data.faq(number, current_lang, cur)
                for i in special:
                    reply = reply.replace(i, f'\\{i}')
                bot.edit_message_two(group_id, message_id, reply, [[{'text':'Back', 'callback_data':'Page 1'}]])
                bot.get_updates(offset = update_id+1)
        else:
            text = current_updates['message']['text']
            print(text)
            if text == '/start' or text == 'start':
                bot.send_message_four(sender_id, 'Select a Language', [[{'text':'English', 'callback_data':'English'}],
                                                                    [{'text':'Hindi', 'callback_data':'Hindi'}],
                                                                    [{'text':'Spanish', 'callback_data':'Spanish'}]])
                bot.get_updates(offset = update_id+1)

            if text == buttons['10']:
                bot.send_message_two(sender_id, texts['0'], [[(buttons['0'])], [(buttons['1'])], [(buttons['3'])], [(buttons['2'])]])
                bot.get_updates(offset = update_id+1)

            if text == buttons['0']:
                button1 = buttons['4']
                button2 = buttons['5']
                button3 = buttons['10']
                bot.send_message_two(sender_id, (texts['2']), [[button3]])
                bot.send_message_four(sender_id, (texts['1']), [[{'text':f'{button1}', 'callback_data':'Mobile Regi'}],
                                                            [{'text':f'{button2}', 'callback_data':'PC Regi'}]])
                bot.get_updates(offset = update_id+1)

            elif text == buttons['1']:
                button1 = buttons['10']
                button2 = buttons['17']
                button3 = buttons['18']
                button4 = buttons['19']
                button5 = buttons['20']
                button6 = buttons['21']
                button7 = buttons['46']
                bot.send_message_two(sender_id, texts['10'], [[button1]])
                bot.send_message_four(sender_id, texts['11'], [[{'text':f'{button7}', 'callback_data':'Intro Video'}],
                                                                [{'text':f'{button2}', 'callback_data':'Introduction'}],
                                                                [{'text':f'{button3}', 'callback_data':'Zoom Video'}],
                                                                [{'text':f'{button4}', 'callback_data':'Promotion Video'}],
                                                                [{'text':f'{button5}', 'callback_data':'Page 1'}],
                                                                [{'text':f'{button6}', 'callback_data':'Nothing'}]])
                bot.get_updates(offset = update_id+1)

            elif text == buttons['2']:
                bot.send_message_three(sender_id, 'Change Language', remove_keyboard=True)
                bot.send_message_four(sender_id, 'Select a Language', [[{'text':'English', 'callback_data':'English'}],
                                                                    [{'text':'Hindi', 'callback_data':'Hindi'}],
                                                                    [{'text':'Spanish', 'callback_data':'Spanish'}]])
                bot.get_updates(offset = update_id+1)

            elif text == buttons['3']:
                bot.send_message
                bot.send_message_four(sender_id, texts['37'], [[{'text':'Telegram', 'url':'https://www.google.com/'}],
                                                                [{'text':'YouTube', 'url':'https://www.google.com/'}]])
                bot.get_updates(offset = update_id+1)

    
    except Exception as e:
        print(e)
        bot.get_updates(offset = update_id+1)
        pass

starter()
