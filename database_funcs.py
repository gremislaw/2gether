import sqlite3


def add_user_to_base(id, name, institute, course):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'user_info' ('user_id', 'name', 'institute', 'course') VALUES (?, ?, ?, ?);",
        (id, name, institute, course))
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
    return 1
