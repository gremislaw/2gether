import sqlite3
from database_funcs import *
from queue import Queue



def get_queue():
    lunch_queue = [244, 432, 123, 544, 853]
    return lunch_queue


def do_search_status(id):
    #поставить галочку то что он ищет чела
    pass


def have_a_person():
    lunch_queue = get_queue()
    if len(lunch_queue) >= 2:
        return 1
    return 0



def share_username():
    lunch_queue = get_queue()
    person = lunch_queue.get()
    #убрать галочку в базе данных то что он ищет чела
    return person



def search_for_lunch(user_id):
    if not have_a_person():
        do_search_status(user_id)
    else:
        user2_id = share_username()
        #первому юзеру надо дать второго а второму первого
    


