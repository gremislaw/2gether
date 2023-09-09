from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters)
import database_funcs
from regions import regions
from secret import TOKEN
import have_a_break

CHOOSING_PROFILE, TYPING_REPLY, TYPING_CHOICE, CHOOSING_DIRECTION, FIX_SUBJECT, FIX_HOBBY, FIX_LANG, FIND_REGION, FIND_LUNCH, SUCCESS_REGION = \
    range(10)
reply_keyboard_profile = [['Имя', 'Курс'], ['Институт'], ['Закончить регистрацию']]
markup_profile = ReplyKeyboardMarkup(reply_keyboard_profile, one_time_keyboard=True)
keyboard_go = [['Вперёд!']]
markup_go = ReplyKeyboardMarkup(keyboard_go, one_time_keyboard=True, resize_keyboard=True)



def facts_to_str(user_data):
    facts = [f"{key.capitalize()} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def profile(update, context):
    id = update.message.from_user.id
    if database_funcs.check_if_user_in_base(id) is None:
        await update.message.reply_text(
            "Привет! Круто, что ты поступил в МИСИС. Я могу помочь тебе освоиться. "
            "Заполни, пожалуйста, небольшую анкету, она нужна, чтобы помочь тебе",
            reply_markup=markup_profile)
        return CHOOSING_PROFILE
    else:
        await update.message.reply_text(
            "Информацию о тебе я уже знаю. "
            "Можем приступать",
            reply_markup=markup_go,
        )
        return CHOOSING_DIRECTION


async def regular_choice(update, context):
    text = update.message.text.lower()
    context.user_data["choice"] = text
    keyboard_course = [['1', '2'], ['3', '4'], ['5', '6']]
    markup_course = ReplyKeyboardMarkup(keyboard_course, one_time_keyboard=True)
    keyboard_inst = [['ИКН'], ['ИНМиН'], ['ЭУПП'], ['ИТ'], ['Горный']]
    markup_inst = ReplyKeyboardMarkup(keyboard_inst, one_time_keyboard=True)
    if text == 'имя':
        await update.message.reply_text(f"Как тебя зовут?")
    elif text == 'курс':
        await update.message.reply_text(f"На каком курсе ты учишься?", reply_markup=markup_course)
    elif text == 'институт':
        await update.message.reply_text(f"В каком институте ты учишься?", reply_markup=markup_inst)

    return TYPING_REPLY


async def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Круто! Вот, что я уже знаю о тебе:\n"
        f"{facts_to_str(user_data)}\nТы можешь изменить какие-то данные, если хочешь",
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
        name = institute = course = ''
        if len(user_data.keys()) == 3:
            database_funcs.add_user_to_base(id, name, course, institute, nick)
        else:
            await update.message.reply_text('Сначала заполни все данные', reply_markup=markup_profile)
            return CHOOSING_PROFILE
    await update.message.reply_text(
        f"Теперь я знаю эти факты о тебе: {facts_to_str(user_data)}\nМожем начинать искать друзей!",
        reply_markup=markup_go)
    user_data.clear()
    return CHOOSING_DIRECTION


async def direction(update, context):
    reply_keyboard_dir = [['Study Buddy'], ['Сообедник'], ['Товарищ по увлечениям'], ['Земляк'],
                          ['Носитель другого языка']]
    markup_dir = ReplyKeyboardMarkup(reply_keyboard_dir, one_time_keyboard=True)
    await update.message.reply_text(
        "Кого ты хочешь найти?",
        reply_markup=markup_dir,
    )
    return CHOOSING_DIRECTION


async def study(update, context):
    reply_keyboard_subjects = [['Математика'], ['Физика'], ['ВычМаш'], ['Английский']]
    markup_subjects = ReplyKeyboardMarkup(reply_keyboard_subjects, one_time_keyboard=True)
    await update.message.reply_text(
        "Каким предметом ты хочешь заниматься?",
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
    res = 'Смотри, эти ребята тоже хотят заниматься этим предметом\nСвяжись с кем-нибудь из них\n'
    for user in a:
        inf = user[0]
        res += f'\nИмя: {inf[0]}\nИнститут: {inf[1]}\nКурс: {inf[2]}\nКонтакт: @{inf[3]}\n\n'

    await update.message.reply_text(res, reply_markup=markup_go)

    database_funcs.add_subject(id, subj)
    return CHOOSING_DIRECTION


async def hobby(update, context):
    reply_keyboard_hobbyes = [['Футбол', 'Волейбол'], ['Танцы', 'Вокал'], ['Гейм-дизайн', 'Спорт-программирование'],
                              ['Шахматы', 'Походы']]
    markup = ReplyKeyboardMarkup(reply_keyboard_hobbyes, one_time_keyboard=True)
    await update.message.reply_text(
        "Чем ты увлекаешься?",
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
    res = 'Смотри, эти ребята увлекаются тем же, что и ты\nСвяжись с кем-нибудь из них\n'
    for user in a:
        inf = user[0]
        res += f'\nИмя: {inf[0]}\nИнститут: {inf[1]}\nКурс: {inf[2]}\nКонтакт: @{inf[3]}\n\n'

    await update.message.reply_text(res, reply_markup=markup_go)

    database_funcs.add_hobby(id, hobby)
    return CHOOSING_DIRECTION


async def lunch(update, context):
    partner = have_a_break.search_for_lunch(update.message.from_user.id)[0]
    if partner != 'wait':
        await update.message.reply_text(
            "Вот с кем ты можешь пообедать: " + f'\nИмя: {partner[0]}\nИнститут: {partner[1]}\nКурс: {partner[2]}\nКонтакт: @{partner[3]}\n\n',
        
        )
    else:
        await update.message.reply_text(
            'Подожди, скоро найдем кого-нибудь',
        
        )

    return CHOOSING_DIRECTION


async def lang(update, context):
    reply_keyboard_lang = [['Английский', 'Французский'], ['Испанский', 'Немецкий'], ['Китайский']]
    markup = ReplyKeyboardMarkup(reply_keyboard_lang, one_time_keyboard=True)
    await update.message.reply_text(
        "C носителем какого языка ты хочешь познакомиться?",
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
    res = 'Вот кого мне удалось найти\nСвяжись с кем-нибудь из них\n'
    for user in a:
        inf = user[0]
        res += f'\nИмя: {inf[0]}\nИнститут: {inf[1]}\nКурс: {inf[2]}\nКонтакт: @{inf[3]}\n\n'

    await update.message.reply_text(res, reply_markup=markup_go)

    database_funcs.add_lang(id, lang)

    return CHOOSING_DIRECTION


async def region(update, context):
    global reg
    await update.message.reply_text(
        "Напиши название своего региона")

    return FIND_REGION


async def find_region(update, context):
    global reg
    text = update.message.text
    reply_keyboard_reg = [['Здорово']]
    markup = ReplyKeyboardMarkup(reply_keyboard_reg, one_time_keyboard=True)
    for x in regions:
        if x[:6] in text:
            reg = x
            await update.message.reply_text(
                f"Я определил для тебя регион {x}", reply_markup=markup)
            return SUCCESS_REGION
    else:
        await update.message.reply_text(
            f"Попробуй ввести регион еще раз")
        return FIND_REGION


async def success_region(update, context):
    global reg, id

    database_funcs.find_common_regions(reg)
    list_id = database_funcs.find_common_regions(reg)
    a = []
    for user_id in list_id:
        if id != user_id[0]:
            a.append(database_funcs.get_profile(user_id[0]))
    res = f'Я добавил тебя в список людей из этого региона - {reg}:'
    for user in a:
        inf = user[0]
        res += f'\nИмя: {inf[0]}\nИнститут: {inf[1]}\nКурс: {inf[2]}\nКонтакт: @{inf[3]}\n\n'
    await update.message.reply_text(
        res, reply_markup=markup_go
    )
    return CHOOSING_DIRECTION


async def fix_lang(update, context):
    lang = update.message.text
    id = update.message.from_user.id
    list_id = database_funcs.find_common_lang(lang)
    a = []
    for user_id in list_id:
        if id != user_id[0]:
            a.append(database_funcs.get_profile(user_id[0]))
    res = 'Вот кого мне удалось найти\nСвяжись с кем-нибудь из них\n'
    for user in a:
        inf = user[0]
        res += f'\nИмя: {inf[0]}\nИнститут: {inf[1]}\nКурс: {inf[2]}\nКонтакт: @{inf[3]}\n\n'

    await update.message.reply_text(res, reply_markup=markup_go)

    database_funcs.add_lang(id, lang)

    return CHOOSING_DIRECTION

def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", profile)],
        states={
            CHOOSING_PROFILE: [
                MessageHandler(
                    filters.Regex("^(Имя|Курс|Институт)$"), regular_choice
                )
            ],
            CHOOSING_DIRECTION: [
                MessageHandler(
                    filters.Regex("^Вперёд!$"), direction),
                MessageHandler(filters.Regex("^Study Buddy$"), study),
                MessageHandler(filters.Regex("^Товарищ по увлечениям$"), hobby),
                MessageHandler(filters.Regex("^Земляк$"), region),
                MessageHandler(filters.Regex("^Носитель другого языка$"), lang),
                MessageHandler(filters.Regex("^Сообедник$"), lunch)


            ],
            FIND_REGION: [
                MessageHandler(
                    filters.ALL, find_region)
            ],
            FIX_HOBBY: [
                MessageHandler(
                    filters.Regex("^(Футбол|Волейбол|Танцы|Вокал|Гейм-дизайн|Спорт-программирование|Шахматы|Походы)$"),
                    fix_hobby),

            ],
            FIX_SUBJECT: [
                MessageHandler(
                    filters.Regex("^(Математика|Физика|ВычМаш|Английский)$"), fix_subject),

            ],
            FIX_LANG: [
                MessageHandler(
                    filters.Regex("^(Английский|Французский|Испанский|Немецкий|Китайский)$"), fix_lang),

            ],
            SUCCESS_REGION: [
                MessageHandler(
                    filters.ALL, success_region),

            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Закончить регистрацию$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Закончить регистрацию$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Закончить регистрацию$"), done)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
