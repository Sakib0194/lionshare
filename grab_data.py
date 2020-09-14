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
