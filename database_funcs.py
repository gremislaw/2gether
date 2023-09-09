import sqlite3


def add_user_to_base(id, name, institute, course, nick):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'user_info' ('user_id', 'name', 'institute', 'course', 'nick') VALUES (?, ?, ?, ?, ?);",
        (id, name, institute, course, nick))
    con.commit()
    con.close()


# надо добавить таблицу для ланча

def add_user_to_lunch(id):
    pass


def add_subject(id, subject):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'subjects' ('user_id', 'subject') VALUES (?, ?);",
        (id, subject))
    con.commit()
    con.close()


def find_common_subjects(subject):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    haveid = cur.execute("Select user_id from 'subjects' where subject = ?", (subject,)).fetchall()
    con.close()
    return haveid


def find_common_hobbyes(hobby):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    haveid = cur.execute("Select user_id from 'hobbyes' where hobby = ?", (hobby,)).fetchall()
    con.close()
    return haveid


def get_profile(user_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    haveid = cur.execute("SELECT name, course, institute, nick FROM 'user_info' WHERE user_id = ?", (user_id,)).fetchall()
    con.close()
    return haveid


def check_if_user_in_base(user_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    haveid = cur.execute("Select user_id from 'user_info' where user_id = ?", (user_id,)).fetchone()
    con.close()
    return haveid

