import sqlite3
import database_funcs
from queue import Queue



def share_username(user_id, status):
    lunch_person_id = database_funcs.get_a_lunch_person(user_id)[0]

    database_funcs.swap_lunch_status(lunch_person_id, status)
    return lunch_person_id



def search_for_lunch(user_id):
    database_funcs.add_user_to_lunch(user_id)
    status = database_funcs.get_lunch_status(user_id)
    if database_funcs.get_a_lunch_person(user_id) == None:
        database_funcs.swap_lunch_status(user_id, status)
        return ('wait', -1)
    else:
        user2_id = share_username(user_id, status)
        user2_profile = database_funcs.get_profile(user2_id)
        return (user2_profile, user2_id)

    


