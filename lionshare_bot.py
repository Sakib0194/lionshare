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

    def edit_message_two (self, chat_id, message_id, text, reply_markup, disable_web_page_preview=True, parse_mode='MarkdownV2'):
        reply_markup = json.dumps({'inline_keyboard': reply_markup})
        fieldss = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'parse_mode':parse_mode, 'reply_markup':reply_markup, 'disable_web_page_preview':disable_web_page_preview}
        function = 'editMessageText'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send

details = sys.argv[1:]
conn = mysql.connector.connect(host=details[0],user=details[1],database=details[2],password=details[3], autocommit=True)
cur = conn.cursor()

token = grab_data.api(cur)
offset = 0

cu_lang = {}
texts = {}
buttons = {}
all_lang = ['English', 'Hindi', 'Spanish']
for h in all_lang:
    te = {}
    bu = {}
    all_te = grab_data.lang(h, cur)
    all_bu = grab_data.buttons(h, cur)
    for t in range(len(all_te)):
        te[str(t)] = all_te[t]
    for i in range(len(all_bu)):
        bu[str(i)] = all_bu[i]
    texts[h] = te
    buttons[h] = bu
special = ['@', '=', '.', '>', '-', '(', ')','!']
send_feedback = []

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
            pending_reply = grab_data.feedback_sent(cur)
            if pending_reply == []:
                pass
            else:
                for i in pending_reply:
                    data = grab_data.sent_reply(i, cur)
                    message = data[1]
                    for u in special:
                        message = message.replace(u, f'\\{u}')
                    bot.send_message(data[0], f'Reply to Feedback: {message}')
                    grab_data.update_sent(i, cur)
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
    global cu_lang
    print(send_feedback)
    try:
        if callback == True:
            print(callback_data)
            if callback_data == 'Nothing':
                bot.get_updates(offset = update_id+1)

            if callback_data == 'English' or callback_data == 'Hindi' or callback_data == 'Spanish':
                cu_lang[sender_id] = callback_data
                bot.send_message_two(sender_id, texts[cu_lang[sender_id]]['0'], [[(buttons[cu_lang[sender_id]]['0'])], [(buttons[cu_lang[sender_id]]['1'])], [(buttons[cu_lang[sender_id]]['3']), (buttons[cu_lang[sender_id]]['2'])]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Promotion Video':
                button4 = buttons[cu_lang[sender_id]]['53']
                button1 = buttons[cu_lang[sender_id]]['49']
                button2 = buttons[cu_lang[sender_id]]['50']
                button3 = buttons[cu_lang[sender_id]]['51']
                bot.edit_message_two(group_id, message_id, texts[cu_lang[sender_id]]['39'], [[{'text':f'{button1}', 'callback_data':'Promo Vid'}],
                                                                        [{'text':f'{button2}', 'callback_data':'Promo Pic'}],
                                                                        [{'text':f'{button3}', 'callback_data':'Stickers'}],
                                                                        [{'text':f'{button4}', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Promo Vid':
                all_links = []
                for i in range(3,12):
                    video = grab_data.links(f'video {i}', cur)
                    all_links.append(video[0])
                for i in all_links:
                    bot.send_video(sender_id, i)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Promo Pic':
                all_links = []
                for i in range(1,10):
                    photo = grab_data.links(f'photo promo {i}', cur)
                    all_links.append(photo[0])
                for i in all_links:
                    bot.send_photo(sender_id, i)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Stickers':
                all_links = []
                link = grab_data.links('sticker 1', cur)
                all_links.append(link[0])
                for i in all_links:
                    bot.send_sticker(sender_id, i)
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Mobile Regi':
                button1 = buttons[cu_lang[sender_id]]['6']
                button2 = buttons[cu_lang[sender_id]]['7']
                button3 = buttons[cu_lang[sender_id]]['9']
                bot.edit_message_two(group_id, message_id, (texts[cu_lang[sender_id]]['1']), [[{'text':f'{button1}', 'callback_data':'Have Wallet'}],
                                                                        [{'text':f'{button2}', 'callback_data':'No Wallet'}],
                                                                        [{'text':f'{button3}', 'callback_data':'Manual'}]])
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'PC Regi':
                button1 = buttons[cu_lang[sender_id]]['8']
                button2 = buttons[cu_lang[sender_id]]['9']
                bot.edit_message_two(group_id, message_id, (texts[cu_lang[sender_id]]['1']), [[{'text':f'{button1}', 'callback_data':'Tronlink'}],
                                                                        [{'text':f'{button2}', 'callback_data':'Manual'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'No Wallet':
                message = texts[cu_lang[sender_id]]['5']
                button1 = buttons[cu_lang[sender_id]]['11']
                button2 = buttons[cu_lang[sender_id]]['12']
                button3 = buttons[cu_lang[sender_id]]['13']
                photo = grab_data.links('photo 1', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Create Tron':
                message = texts[cu_lang[sender_id]]['3']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['11']
                button2 = buttons[cu_lang[sender_id]]['12']
                button3 = buttons[cu_lang[sender_id]]['13']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Topping Up':
                message = texts[cu_lang[sender_id]]['4']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['11']
                button2 = buttons[cu_lang[sender_id]]['12']
                button3 = buttons[cu_lang[sender_id]]['13']
                video = grab_data.links('video 1', cur)
                bot.send_video(sender_id, video)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tron'}],
                                                            [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                            [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Complete Regi':
                message = texts[cu_lang[sender_id]]['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['14']
                photo = grab_data.links('photo 2', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Complete Regi PC':
                message = texts[cu_lang[sender_id]]['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['14']
                photo = grab_data.links('photo 4', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Finalize':
                bot.edit_message(group_id, message_id, (texts[cu_lang[sender_id]]['7']))
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Have Wallet':
                message = texts[cu_lang[sender_id]]['6']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['14']
                photo = grab_data.links('photo 2', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Finalize'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Manual':
                message = texts[cu_lang[sender_id]]['8']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                bot.edit_message(group_id, message_id, message)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Tronlink':
                button1 = buttons[cu_lang[sender_id]]['15']
                button2 = buttons[cu_lang[sender_id]]['16']
                button3 = buttons[cu_lang[sender_id]]['13']
                photo = grab_data.links('photo 3', cur)
                bot.send_photo(sender_id, photo)
                bot.send_message_four(sender_id, (texts[cu_lang[sender_id]]['5']), [[{'text':f'{button1}', 'callback_data':'Create Tronlink'}],
                                                                [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                                [{'text':f'{button3}', 'callback_data':'Complete Regi'}]])
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Create Tronlink':
                message = texts[cu_lang[sender_id]]['9']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['15']
                button2 = buttons[cu_lang[sender_id]]['16']
                button3 = buttons[cu_lang[sender_id]]['13']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Create Tronlink'}],
                                                                [{'text':f'{button2}', 'callback_data':'Topping Up'}],
                                                                [{'text':f'{button3}', 'callback_data':'Complete Regi PC'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Introduction':
                button1 = buttons[cu_lang[sender_id]]['47']
                button2 = buttons[cu_lang[sender_id]]['48']
                button3 = buttons[cu_lang[sender_id]]['52']
                button4 = buttons[cu_lang[sender_id]]['53']
                button5 = buttons[cu_lang[sender_id]]['54']
                button6 = buttons[cu_lang[sender_id]]['55']
                bot.edit_message_two(group_id, message_id, texts[cu_lang[sender_id]]['38'], [[{'text':f'{button1}', 'callback_data':'Intro Eng'}],
                                                                        [{'text':f'{button2}', 'callback_data':'Intro Afr'}],
                                                                        [{'text':f'{button3}', 'callback_data':'Intro Span'}],
                                                                        [{'text':f'{button5}', 'callback_data':'Intro Turk'}],
                                                                        [{'text':f'{button6}', 'callback_data':'Intro Hind'}],
                                                                        [{'text':f'{button4}', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Intro Eng':
                document = grab_data.links('document 1', cur)
                bot.send_document(sender_id, document)
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Intro Afr':
                document = grab_data.links('document 2', cur)
                bot.send_document(sender_id, document)
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Intro Span':
                document = grab_data.links('document 3', cur)
                bot.send_document(sender_id, document)
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Intro Turk':
                document = grab_data.links('document 4', cur)
                bot.send_document(sender_id, document)
                bot.get_updates(offset = update_id+1)
            
            elif callback_data == 'Intro Hind':
                document = grab_data.links('document 5', cur)
                bot.send_document(sender_id, document)
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Intro Video':
                video = grab_data.links('video 2', cur)
                bot.send_video(sender_id, video)
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Zoom Video':
                link1 = grab_data.links('video zoom', cur)
                link2 = grab_data.links('video zoom 2', cur)
                bot.send_video(sender_id, link1)
                bot.send_video(sender_id, link2)
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Send Feedback':
                message = texts[cu_lang[sender_id]]['40']
                for i in special:
                    message = message.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['53']
                send_feedback.append(sender_id)
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Page 1':
                message = texts[cu_lang[sender_id]]['12']
                button1 = buttons[cu_lang[sender_id]]['22']
                button2 = buttons[cu_lang[sender_id]]['23']
                button3 = buttons[cu_lang[sender_id]]['24']
                button4 = buttons[cu_lang[sender_id]]['25']
                button5 = buttons[cu_lang[sender_id]]['26']
                button6 = buttons[cu_lang[sender_id]]['27']
                button7 = buttons[cu_lang[sender_id]]['28']
                button8 = buttons[cu_lang[sender_id]]['29']
                button9 = buttons[cu_lang[sender_id]]['53']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Answer 13'}],
                                                                [{'text':f'{button2}', 'callback_data':'Answer 14'}],
                                                                [{'text':f'{button3}', 'callback_data':'Answer 15'}],
                                                                [{'text':f'{button4}', 'callback_data':'Answer 16'}],
                                                                [{'text':f'{button5}', 'callback_data':'Answer 17'}],
                                                                [{'text':f'{button6}', 'callback_data':'Answer 18'}],
                                                                [{'text':f'{button7}', 'callback_data':'Answer 19'}],
                                                                [{'text':f'{button8}', 'callback_data':'Answer 20'}],
                                                                [{'text':'<', 'callback_data':'Page 3'}, {'text':'Page 1', 'callback_data':'Nothing'}, {'text':'>', 'callback_data':'Page 2'}],
                                                                [{'text':f'{button9}', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Page 2':
                message = texts[cu_lang[sender_id]]['12']
                button1 = buttons[cu_lang[sender_id]]['30']
                button2 = buttons[cu_lang[sender_id]]['31']
                button3 = buttons[cu_lang[sender_id]]['32']
                button4 = buttons[cu_lang[sender_id]]['33']
                button5 = buttons[cu_lang[sender_id]]['34']
                button6 = buttons[cu_lang[sender_id]]['35']
                button7 = buttons[cu_lang[sender_id]]['36']
                button8 = buttons[cu_lang[sender_id]]['37']
                button9 = buttons[cu_lang[sender_id]]['53']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Answer 21'}],
                                                                [{'text':f'{button2}', 'callback_data':'Answer 22'}],
                                                                [{'text':f'{button3}', 'callback_data':'Answer 23'}],
                                                                [{'text':f'{button4}', 'callback_data':'Answer 24'}],
                                                                [{'text':f'{button5}', 'callback_data':'Answer 25'}],
                                                                [{'text':f'{button6}', 'callback_data':'Answer 26'}],
                                                                [{'text':f'{button7}', 'callback_data':'Answer 27'}],
                                                                [{'text':f'{button8}', 'callback_data':'Answer 28'}],
                                                                [{'text':'<', 'callback_data':'Page 1'}, {'text':'Page 2', 'callback_data':'Nothing'}, {'text':'>', 'callback_data':'Page 3'}],
                                                                [{'text':f'{button9}', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            elif callback_data == 'Page 3':
                message = texts[cu_lang[sender_id]]['12']
                button1 = buttons[cu_lang[sender_id]]['38']
                button2 = buttons[cu_lang[sender_id]]['39']
                button3 = buttons[cu_lang[sender_id]]['40']
                button4 = buttons[cu_lang[sender_id]]['41']
                button5 = buttons[cu_lang[sender_id]]['42']
                button6 = buttons[cu_lang[sender_id]]['43']
                button7 = buttons[cu_lang[sender_id]]['44']
                button8 = buttons[cu_lang[sender_id]]['45']
                button9 = buttons[cu_lang[sender_id]]['53']
                bot.edit_message_two(group_id, message_id, message, [[{'text':f'{button1}', 'callback_data':'Answer 29'}],
                                                                [{'text':f'{button2}', 'callback_data':'Answer 30'}],
                                                                [{'text':f'{button3}', 'callback_data':'Answer 31'}],
                                                                [{'text':f'{button4}', 'callback_data':'Answer 32'}],
                                                                [{'text':f'{button5}', 'callback_data':'Answer 33'}],
                                                                [{'text':f'{button6}', 'callback_data':'Answer 34'}],
                                                                [{'text':f'{button7}', 'callback_data':'Answer 35'}],
                                                                [{'text':f'{button8}', 'callback_data':'Answer 36'}],
                                                                [{'text':'<', 'callback_data':'Page 2'}, {'text':'Page 3', 'callback_data':'Nothing'}, {'text':'>', 'callback_data':'Page 1'}],
                                                                [{'text':f'{button9}', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Back':
                if sender_id in send_feedback:
                    send_feedback.remove(sender_id)
                button1 = buttons[cu_lang[sender_id]]['10']
                button2 = buttons[cu_lang[sender_id]]['17']
                button3 = buttons[cu_lang[sender_id]]['18']
                button4 = buttons[cu_lang[sender_id]]['19']
                button5 = buttons[cu_lang[sender_id]]['20']
                button6 = buttons[cu_lang[sender_id]]['21']
                button7 = buttons[cu_lang[sender_id]]['46']
                bot.edit_message_two(group_id, message_id, texts[cu_lang[sender_id]]['11'], [[{'text':f'{button7}', 'callback_data':'Intro Video'}],
                                                                [{'text':f'{button2}', 'callback_data':'Introduction'}],
                                                                [{'text':f'{button3}', 'callback_data':'Zoom Video'}],
                                                                [{'text':f'{button4}', 'callback_data':'Promotion Video'}],
                                                                [{'text':f'{button5}', 'callback_data':'Page 1'}],
                                                                [{'text':f'{button6}', 'callback_data':'Send Feedback'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data.startswith('Answer'):
                number = callback_data.split(' ')[1]
                reply = grab_data.faq(number, cu_lang[sender_id], cur)
                if callback_data == 'Answer 20':
                    pass
                else:
                    for i in special:
                        reply = reply.replace(i, f'\\{i}')
                button1 = buttons[cu_lang[sender_id]]['53']
                if callback_data == 'Answer 20':
                    bot.edit_message_two(group_id, message_id, reply, [[{'text':f'{button1}', 'callback_data':'Page 1'}]], parse_mode='HTML')
                else:
                    bot.edit_message_two(group_id, message_id, reply, [[{'text':f'{button1}', 'callback_data':'Page 1'}]])
                bot.get_updates(offset = update_id+1)
        else:
            text = current_updates['message']['text']
            print(text)
            if text == '/start' or text == 'start':
                cu_lang[sender_id] = 'English'
                bot.send_message_four(sender_id, 'Please choose your language⤵️', [[{'text':'ENGLISH🇬🇧', 'callback_data':'English'}],
                                                                    [{'text':'हिन्दी🇮🇳', 'callback_data':'Hindi'}],
                                                                    [{'text':'ESPAÑOL🇪🇸', 'callback_data':'Spanish'}]])
                users = grab_data.all_users(cur)
                if sender_id not in users:
                    grab_data.add_users(sender_id, cur)
                bot.get_updates(offset = update_id+1)

            if sender_id not in cu_lang:
                cu_lang[sender_id] = 'English'
                bot.send_message_four(sender_id, 'Please choose your language⤵️', [[{'text':'ENGLISH🇬🇧', 'callback_data':'English'}],
                                                                    [{'text':'हिन्दी🇮🇳', 'callback_data':'Hindi'}],
                                                                    [{'text':'ESPAÑOL🇪🇸', 'callback_data':'Spanish'}]])
                users = grab_data.all_users(cur)
                bot.get_updates(offset = update_id+1)

            if text.startswith(grab_data.mass_message(cur)):
                message = text.split(' ')[1:]
                full_text = ''
                for i in message:
                    full_text += f'{i} '
                for i in special:
                    full_text = full_text.replace(i, f'\\{i}')
                all_user = grab_data.all_users(cur)
                for i in all_user:
                    bot.send_message(i, full_text)
                bot.get_updates(offset = update_id+1)

            if text == buttons[cu_lang[sender_id]]['10']:
                if sender_id in send_feedback:
                    send_feedback.remove(sender_id)
                bot.send_message_two(sender_id, texts[cu_lang[sender_id]]['0'], [[(buttons[cu_lang[sender_id]]['0'])], [(buttons[cu_lang[sender_id]]['1'])], [(buttons[cu_lang[sender_id]]['3']), (buttons[cu_lang[sender_id]]['2'])]])
                bot.get_updates(offset = update_id+1)

            elif sender_id in send_feedback:
                if sender_id in send_feedback:
                    send_feedback.remove(sender_id)
                grab_data.add_feedback(sender_id, text, cur)
                message = texts[cu_lang[sender_id]]['41']
                button1 = buttons[cu_lang[sender_id]]['53']
                bot.send_message_four(sender_id, message, [[{'text':f'{button1}', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            if text == buttons[cu_lang[sender_id]]['0']:
                button1 = buttons[cu_lang[sender_id]]['4']
                button2 = buttons[cu_lang[sender_id]]['5']
                button3 = buttons[cu_lang[sender_id]]['10']
                bot.send_message_two(sender_id, (texts[cu_lang[sender_id]]['2']), [[button3]])
                bot.send_message_four(sender_id, (texts[cu_lang[sender_id]]['1']), [[{'text':f'{button1}', 'callback_data':'Mobile Regi'}],
                                                            [{'text':f'{button2}', 'callback_data':'PC Regi'}]])
                bot.get_updates(offset = update_id+1)

            elif text == buttons[cu_lang[sender_id]]['1']:
                button1 = buttons[cu_lang[sender_id]]['10']
                button2 = buttons[cu_lang[sender_id]]['17']
                button3 = buttons[cu_lang[sender_id]]['18']
                button4 = buttons[cu_lang[sender_id]]['19']
                button5 = buttons[cu_lang[sender_id]]['20']
                button6 = buttons[cu_lang[sender_id]]['21']
                button7 = buttons[cu_lang[sender_id]]['46']
                bot.send_message_two(sender_id, texts[cu_lang[sender_id]]['10'], [[button1]])
                bot.send_message_four(sender_id, texts[cu_lang[sender_id]]['11'], [[{'text':f'{button7}', 'callback_data':'Intro Video'}],
                                                                [{'text':f'{button2}', 'callback_data':'Introduction'}],
                                                                [{'text':f'{button3}', 'callback_data':'Zoom Video'}],
                                                                [{'text':f'{button4}', 'callback_data':'Promotion Video'}],
                                                                [{'text':f'{button5}', 'callback_data':'Page 1'}],
                                                                [{'text':f'{button6}', 'callback_data':'Send Feedback'}]])
                bot.get_updates(offset = update_id+1)

            elif text == buttons[cu_lang[sender_id]]['2']:
                bot.send_message_three(sender_id, 'Change Language', remove_keyboard=True)
                bot.send_message_four(sender_id, 'Select a Language', [[{'text':'ENGLISH🇬🇧', 'callback_data':'English'}],
                                                                    [{'text':'हिन्दी🇮🇳', 'callback_data':'Hindi'}],
                                                                    [{'text':'ESPAÑOL🇪🇸', 'callback_data':'Spanish'}]])
                bot.get_updates(offset = update_id+1)

            elif text == buttons[cu_lang[sender_id]]['3']:
                bot.send_message_four(sender_id, texts[cu_lang[sender_id]]['37'], [[{'text':'TELEGRAM CHAT 👤', 'url':'https://t.me/lionssharetron_official'}],
                                                                [{'text':'TELEGRAM CHANNEL 📢', 'url':'https://t.me/lionsharetron_official'}]])
                bot.get_updates(offset = update_id+1)
    except Exception as e:
        print(e)
        bot.get_updates(offset = update_id+1)
        pass

starter()
