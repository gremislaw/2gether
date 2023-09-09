import sqlite3
import database_funcs
from queue import Queue



def share_username():
    lunch_person_id = database_funcs.get_a_lunch_person()[0]
    database_funcs.swap_lunch_status(lunch_person_id)
    return lunch_person_id



def search_for_lunch(user_id):
    database_funcs.add_user_to_lunch(user_id)
    status = database_funcs.get_lunch_status(user_id)
    if len(database_funcs.get_a_lunch_person()) == 0:
        database_funcs.swap_lunch_status(user_id, status)
        while len(database_funcs.get_a_lunch_person()) == 1:
            pass        
    user2_id = share_username()
    user2_name = database_funcs.get_profile(user2_id)
    return user2_name
    


