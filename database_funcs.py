import sqlite3


def add_user_to_base(id, name, institute, course, nick):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'user_info' ('user_id', 'name', 'institute', 'course', 'nick') VALUES (?, ?, ?, ?, ?);",
        (id, name, institute, course, nick))
    con.commit()
    con.close()


def add_user_to_lunch(id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'have_a_break' ('user_id', 'status') VALUES (?, ?);",
        (id, 0))
    con.commit()
    con.close()


def add_subject(id, subject):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'subjects' ('user_id', 'subject') VALUES (?, ?);",
        (id, subject))
    con.commit()
    con.close()


def add_hobby(id, hobby):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'hobbyes' ('user_id', 'hobby') VALUES (?, ?);",
        (id, hobby))
    con.commit()
    con.close()


def add_lang(id, lang):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'languages' ('user_id', 'language') VALUES (?, ?);",
        (id, lang))
    con.commit()
    con.close()


def add_reg(id, reg):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'regions' ('user_id', 'region') VALUES (?, ?);",
        (id, reg))
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


def find_common_lang(lang):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    haveid = cur.execute("Select user_id from 'languages' where language = ?", (lang,)).fetchall()
    con.close()
    return haveid


def find_common_regions(reg):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    haveid = cur.execute("Select user_id from 'regions' where region = ?", (reg,)).fetchall()
    con.close()
    return haveid


def get_lunch_status(user_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    status = cur.execute("SELECT status FROM 'have_a_break' WHERE user_id = ?", (user_id,)).fetchone()
    con.close()
    return int(status[0])


def swap_lunch_status(user_id, status):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(f"UPDATE have_a_break SET status = {(status + 1) % 2} WHERE user_id = {user_id}")
    con.commit()
    con.close()


def get_a_lunch_person(id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    have_a_guy = cur.execute(f"SELECT user_id FROM 'have_a_break' WHERE status = 1 and user_id != {id}").fetchone()
    con.close()
    return have_a_guy


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


def update_profile(id, name, course, institute):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(f'UPDATE user_info SET name = "{name}", course = "{course}", institute = "{institute}" WHERE user_id = {id}')
    con.commit()
    con.close()

