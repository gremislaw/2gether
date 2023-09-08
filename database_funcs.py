import sqlite3
import random
import re


class Special:
    def get_sol_by_task(task_num, task_id):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        task = str(task_num) + "_solution"
        q2 = "SELECT [" + task + "] FROM tasks WHERE id = " + str(task_id)
        res = cur.execute(q2).fetchone()[0]
        con.close()
        return res


def get_task_by_num(tasknum):
    if tasknum.isdigit():
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        num = int(tasknum)
        if 0 < num < 28:
            task = str(num) + "_task"
            task = re.sub(" ", "", task)
            q = "SELECT COUNT([" + task + "]) FROM tasks"
            task_id = cur.execute(q).fetchall()[0]
            task_id = task_id[0]
            task_id = random.randint(0, task_id - 1)
            q2 = "SELECT [" + task + "] FROM tasks WHERE id = " + str(task_id)
            res = cur.execute(q2).fetchone()[0]
            if num == 1:
                hash = cur.execute("SELECT [1_taskinf] FROM tasks WHERE id = ?", (task_id,)).fetchone()[0]
                res = res + "\n" + decode(hash)
            elif num in [3, 9, 10, 13, 17, 18, 24, 26, 27]:
                link = get_link(tasknum, task_id)
                res = res + " \n" + link
            answer = dict(num=task_id, text=res)
            con.close()
            return answer
        else:
            con.close()
            return "Error"
    else:
        return "Error"


def decode(text):
    t = text[:4]
    if t == "tabl":
        input_string = text[3:]
        i = 0
        main_string = ""
        input_string = re.sub(" ", "..", input_string)
        input_string = input_string.split(":")
        while i != len(input_string):
            if input_string[i] == "tr":
                main_string = main_string + "\n"
            if input_string[i] == "td":
                try:
                    t = int(input_string[i + 1])
                    if t > 9:
                        main_string = main_string + "..|" + input_string[i + 1] + "|"
                    else:
                        main_string = main_string + "..|" + input_string[i + 1] + "|.."
                except Exception:
                    main_string = main_string + "..|" + input_string[i + 1] + "|.."
            i = i + 1
    res = main_string
    return res


def get_link(task_num, task_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    column_name = task_num + "_file_links"
    q = "SELECT [" + column_name + "] FROM tasks WHERE id = " + str(task_id)
    link = cur.execute(q).fetchone()[0]
    con.close()
    return link


def add_user_to_base(id, name, institute, course):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'user_info' ('user_id', 'name', 'institute', 'course') VALUES (?, ?, ?, ?);",
        (id, name, institute, course))
    con.commit()
    con.close()


def check_if_user_in_base(user_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    haveid = cur.execute("Select user_id from 'user_info' where user_id = ?", (user_id,)).fetchone()
    con.close()
    return haveid


def get_user_nick(user_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    name = cur.execute("select user_name from 'user_info' WHERE user_id = ?", (user_id,)).fetchone()[0]
    con.close()
    return name


def update_user_last_asked_task(task_num, task_id, user_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    cur.execute("UPDATE user_info SET [asked_task_id] = ? WHERE user_id = ?", (task_id, user_id))
    cur.execute("UPDATE user_info SET [asked_task_num] = ? WHERE user_id = ?", (task_num, user_id))
    con.commit()
    con.close()


def get_solution_to_user(user_id):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()

    sol_num = cur.execute("SELECT [asked_task_num] FROM user_info WHERE user_id = ?",
                          (user_id,)).fetchone()[0]
    sol_id = cur.execute("SELECT [asked_task_id] FROM user_info WHERE user_id = ?",
                         (user_id,)).fetchone()[0]
    if sol_num is not None and sol_id is not None:
        res = Special.get_sol_by_task(sol_num, sol_id)
        con.close()
        return res
    else:
        con.close()
        return "Ты ничего не спрашивал"


def get_ege_theory(task_num):
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    query = "SELECT [" + task_num + "_theory" + "] FROM theory"
    res = cur.execute(query).fetchone()
    con.close()
    return res


def get_random_joke():
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()
    number_of_jokes = cur.execute("SELECT COUNT() [jokes] FROM jokes").fetchone()[0]
    joke_num = random.randint(0, number_of_jokes - 1)
    joke = cur.execute("SELECT [jokes] FROM jokes WHERE id = ?", (joke_num,)).fetchone()[0]
    con.close()
    return joke
