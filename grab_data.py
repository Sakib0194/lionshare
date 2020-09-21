def lang(lang, cur):
    cur.execute(f"SELECT {lang} FROM texts_lang")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def buttons(lang, cur):
    cur.execute(f"SELECT {lang} FROM button_lang")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def api(cur):
    cur.execute(f"SELECT Details FROM specials where code = 'API'")
    rows = cur.fetchall()
    return rows[0][0]

def api_two(cur):
    cur.execute(f"SELECT Details FROM specials where code = 'API 2'")
    rows = cur.fetchall()
    return rows[0][0]

def faq(number, lang, cur):
    cur.execute(f"SELECT {lang} FROM texts_lang WHERE Message_ID = '{int(number)+1}'")
    rows = cur.fetchall()
    full_texts = ''
    for i in rows:
        full_texts = i[0]
    return full_texts

def links(code, cur):
    cur.execute(f"SELECT Details FROM specials where code = '{code}'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def all_users(cur):
    cur.execute(f"SELECT Telegram_ID FROM users")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def add_users(id_num, cur):
    sql = f"INSERT INTO users(Telegram_ID) VALUES('{id_num}')"
    cur.execute(sql)

def feed_pass(tele_id, cur):
    cur.execute(f"SELECT Password FROM users where Telegram_ID = '{tele_id}'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        if i[0] == None:
            pass
        else:
            unique.append(i[0])
    if unique == []:
        return 'Nothing'
    else:
        return unique[0]

def pending_feed(cur):
    cur.execute(f"SELECT Message_ID FROM feedbacks where Pending_Reply = 'Yes'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def add_feedback(id_num, message, cur):
    sql = f"INSERT INTO feedbacks(Telegram_ID, Feedback) VALUES('{id_num}', '{message}')"
    cur.execute(sql)

def feed_details(message, cur):
    cur.execute(f"SELECT Telegram_ID, Feedback, Message_ID FROM feedbacks where Message_ID = '{message}'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i)
    return unique[0]

def feedback_reply(message_id, message, cur):
    sql = f"""UPDATE feedbacks SET Reply_Message = "{message}" WHERE Message_ID = {message_id}"""
    cur.execute(sql)
    sql = f"UPDATE feedbacks SET Feedback_Sent = 'Yes' WHERE Message_ID = {message_id}"
    cur.execute(sql)
    sql = f"UPDATE feedbacks SET Pending_Reply = 'No' WHERE Message_ID = {message_id}"
    cur.execute(sql)

def feedback_sent(cur):
    cur.execute(f"SELECT Message_ID FROM feedbacks where Feedback_Sent = 'Yes'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def sent_reply(message_id,cur):
    cur.execute(f"SELECT Telegram_ID, Reply_Message FROM feedbacks where Message_ID = '{message_id}'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i)
    return unique[0]

def update_sent(message_id, cur):
    sql = f"UPDATE feedbacks SET Feedback_Sent = 'Done' WHERE Message_ID = {message_id}"
    cur.execute(sql)

def all_admins(cur):
    cur.execute(f"SELECT Telegram_ID FROM users where Admin = 'Yes'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def pending_seen(cur):
    cur.execute(f"SELECT Message_ID FROM feedbacks where Feedback_Seen = 'No'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def seen_reply(message_id, cur):
    cur.execute(f"SELECT Feedback FROM feedbacks where Message_ID = '{message_id}'")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique[0]

def update_seen(message_id, cur):
    sql = f"UPDATE feedbacks SET Feedback_Seen = 'Done' WHERE Message_ID = {message_id}"
    cur.execute(sql)

def mass_message(cur):
    cur.execute(f"SELECT Details FROM specials where code = 'mass message'")
    rows = cur.fetchall()
    return rows[0][0]