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