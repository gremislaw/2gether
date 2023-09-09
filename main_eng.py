from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters)
import database_funcs
from secret import TOKEN_EN
import have_a_break

CHOOSING_PROFILE, TYPING_REPLY, TYPING_CHOICE, CHOOSING_DIRECTION, FIX_SUBJECT, FIX_HOBBY, FIX_LANG, FIND_REGION, FIND_LUNCH, SUCCESS_REGION = \
    range(10)
reply_keyboard_profile = [['Name', 'Year'], ['Faculty'], ['Finish registration']]
markup_profile = ReplyKeyboardMarkup(reply_keyboard_profile, one_time_keyboard=True)
keyboard_go = [["Let's go!"], ['Edit profile']]
markup_go = ReplyKeyboardMarkup(keyboard_go, one_time_keyboard=True, resize_keyboard=True)


def facts_to_str(user_data):
    facts = [f"{key.capitalize()} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def profile(update, context):
    id = update.message.from_user.id
    if database_funcs.check_if_user_in_base(id) is None:
        await update.message.reply_text(
            "Hey! We're glad to see you among the students of MISIS. "
            "Please, fill this questionnnaire out",
            reply_markup=markup_profile)
        return CHOOSING_PROFILE
    else:
        await update.message.reply_text(
            "I know info about you. "
            "We can start",
            reply_markup=markup_go,
        )
        return CHOOSING_DIRECTION


async def regular_choice(update, context):
    text = update.message.text.lower()
    context.user_data["choice"] = text
    keyboard_course = [['1', '2'], ['3', '4'], ['5', '6']]
    markup_course = ReplyKeyboardMarkup(keyboard_course, one_time_keyboard=True)
    keyboard_inst = [['Institute of computer science'], ['Institute of new materials'],
                     ['Institute of economics and management'], ['Institute of technologies'], ['Mining institute']]
    markup_inst = ReplyKeyboardMarkup(keyboard_inst, one_time_keyboard=True)
    if text == 'name':
        await update.message.reply_text(f"What's your name?")
    elif text == 'year':
        await update.message.reply_text(f"What year are you studying?", reply_markup=markup_course)
    elif text == 'faculty':
        await update.message.reply_text(f"What is your faculty?", reply_markup=markup_inst)

    return TYPING_REPLY


async def edit_profile(update, context):
    id = update.message.from_user.id
    facts = database_funcs.get_profile(id)[0][:4]
    print(facts)
    res = f'\n\nName: {facts[0]}\nFaculty: {facts[1]}\nYear: {facts[2]}\n'
    context.user_data['name'] = facts[0]
    context.user_data['faculty'] = facts[1]
    context.user_data['year'] = facts[2]
    await update.message.reply_text(
        f"\nI know following about you: {res}\nYou can change something",
        reply_markup=markup_profile)
    return CHOOSING_PROFILE


async def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Nice! That's what i know about you:\n"
        f"{facts_to_str(user_data)}\nYou can change something if you want",
        reply_markup=markup_profile,
    )
    return CHOOSING_PROFILE


async def done(update, context):
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    id = update.message.from_user.id
    nick = update.message.from_user.username
    if database_funcs.check_if_user_in_base(id) is None:

        if len(user_data.keys()) == 3:
            name = user_data['name']
            course = user_data['year']
            institute = user_data['faculty']
            database_funcs.add_user_to_base(id, name, course, institute, nick)
        else:
            await update.message.reply_text('You have to fill everything out', reply_markup=markup_profile)
            return CHOOSING_PROFILE
    await update.message.reply_text(
        f"I know following about you:  {facts_to_str(user_data)}\nWe can start finding new friends!",
        reply_markup=markup_go)
    user_data.clear()
    return CHOOSING_DIRECTION


async def direction(update, context):
    reply_keyboard_dir = [['Study Buddy'], ['Companion for lunch'], ['Hobby fellow'],
                          ['Native speaker']]
    markup_dir = ReplyKeyboardMarkup(reply_keyboard_dir, one_time_keyboard=True)
    await update.message.reply_text(
        "Who would you like to find?",
        reply_markup=markup_dir,
    )
    return CHOOSING_DIRECTION


async def study(update, context):
    reply_keyboard_subjects = [['Math'], ['Physics'], ['Chemistry'], ['Russian']]
    markup_subjects = ReplyKeyboardMarkup(reply_keyboard_subjects, one_time_keyboard=True)
    await update.message.reply_text(
        "What subject would you like to study?",
        reply_markup=markup_subjects,
    )
    return FIX_SUBJECT


async def fix_subject(update, context):
    subj = update.message.text
    id = update.message.from_user.id
    list_id = database_funcs.find_common_subjects(subj)
    a = []
    for user_id in list_id:
        if id != user_id[0]:
            a.append(database_funcs.get_profile(user_id[0]))
    res = 'Look, this guys also want to study it\nContact them\n'
    for user in a:
        inf = user[0]
        res += f'\nName: {inf[0]}\nFaculty: {inf[1]}\nYear: {inf[2]}\nContact: @{inf[3]}\n\n'

    await update.message.reply_text(res, reply_markup=markup_go)

    database_funcs.add_subject(id, subj)
    return CHOOSING_DIRECTION


async def hobby(update, context):
    reply_keyboard_hobbyes = [['Football', 'Volleyball'], ['Dancing', 'Vocals'], ['Game dev', 'Sport programming'],
                              ['Chess', 'Tourism']]
    markup = ReplyKeyboardMarkup(reply_keyboard_hobbyes, one_time_keyboard=True)
    await update.message.reply_text(
        "What is your hobby?",
        reply_markup=markup,
    )
    return FIX_HOBBY


async def fix_hobby(update, context):
    hobby = update.message.text
    id = update.message.from_user.id
    list_id = database_funcs.find_common_hobbyes(hobby)
    a = []
    for user_id in list_id:
        if id != user_id[0]:
            a.append(database_funcs.get_profile(user_id[0]))
    res = 'Look, this guys also love to do it\nContact them\n'
    for user in a:
        inf = user[0]
        res += f'\nName: {inf[0]}\nFaculty: {inf[1]}\nYear: {inf[2]}\nContact: @{inf[3]}\n\n'

    await update.message.reply_text(res, reply_markup=markup_go)

    database_funcs.add_hobby(id, hobby)
    return CHOOSING_DIRECTION


async def lunch(update, context):
    partner_profile, partner_id = have_a_break.search_for_lunch(update.message.from_user.id)
    cur_profile = database_funcs.get_profile(update.message.from_user.id)[0]
    if partner_profile != 'wait':
        partner_profile = partner_profile[0]
        await update.message.reply_text(
            "Here's the person you can have lunch with: " + f'\nName: {partner_profile[0]}\nFaculty: {partner_profile[1]}\nYear: '
                                                            f'{partner_profile[2]}\nContact: @{partner_profile[3]}\n\n',
            reply_markup=markup_go
        )
        await context.bot.send_message(chat_id=partner_id,
                                       text=f"Here's the person you can have lunch with: " + f'\nName: '
                                                                                             f'{cur_profile[0]}\n'
                                                                                             f'Faculty: '
                                                                                             f'{cur_profile[1]}\nYear: '
                                                                                             f'{cur_profile[2]}\n'
                                                                                             f'Contact: '
                                                                                             f'@{cur_profile[3]}\n\n',
                                       )
        database_funcs.swap_lunch_status(partner_id, 1)
    else:
        await update.message.reply_text(
            "Wait, we'll find somebody", reply_markup=markup_go

        )

    return CHOOSING_DIRECTION


async def lang(update, context):
    reply_keyboard_lang = [['English', 'French'], ['Spanish', 'German'], ['Chinese']]
    markup = ReplyKeyboardMarkup(reply_keyboard_lang, one_time_keyboard=True)
    await update.message.reply_text(
        "What native speaker would you like to meet?",
        reply_markup=markup,
    )
    return FIX_LANG


async def fix_lang(update, context):
    lang = update.message.text
    id = update.message.from_user.id
    list_id = database_funcs.find_common_lang(lang)
    a = []
    for user_id in list_id:
        if id != user_id[0]:
            a.append(database_funcs.get_profile(user_id[0]))
    res = "Here's people I could find for you\nContact somebody of them\n"
    for user in a:
        inf = user[0]
        res += f'\nName: {inf[0]}\nFaculty: {inf[1]}\nYear: {inf[2]}\nContact: @{inf[3]}\n\n'

    await update.message.reply_text(res, reply_markup=markup_go)

    database_funcs.add_lang(id, lang)

    return CHOOSING_DIRECTION



def main():
    application = Application.builder().token(TOKEN_EN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", profile)],
        states={
            CHOOSING_PROFILE: [
                MessageHandler(
                    filters.Regex("^(Name|Year|Faculty)$"), regular_choice
                )
            ],
            CHOOSING_DIRECTION: [
                MessageHandler(
                    filters.Regex("^Let's go!$"), direction),
                MessageHandler(filters.Regex("^Edit profile$"), edit_profile),
                MessageHandler(filters.Regex("^Study Buddy$"), study),
                MessageHandler(filters.Regex("^Hobby fellow$"), hobby),
                MessageHandler(filters.Regex("^Native speaker$"), lang),
                MessageHandler(filters.Regex("^Companion for lunch$"), lunch)


            ],
            FIX_HOBBY: [
                MessageHandler(
                    filters.Regex("^(Football|Volleyball|Dancing|Vocals|Game dev|Sport programming|Chess|Tourism)$"),
                    fix_hobby),

            ],
            FIX_SUBJECT: [
                MessageHandler(
                    filters.Regex("^(Math|Physics|Chemistry|Russian)$"), fix_subject),

            ],
            FIX_LANG: [
                MessageHandler(
                    filters.Regex("^(English|French|Spanish|German|Chinese)$"), fix_lang),

            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Finish registration$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Finish registration$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Finish registration$"), done)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
