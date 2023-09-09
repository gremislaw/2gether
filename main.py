from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters)
import database_funcs
from secret import TOKEN

CHOOSING_PROFILE, TYPING_REPLY, TYPING_CHOICE, CHOOSING_DIRECTION, FIX_SUBJECT, FIX_HOBBY = range(6)
reply_keyboard_profile = [['Имя', 'Курс'], ['Институт'], ['Закончить']]
markup_profile = ReplyKeyboardMarkup(reply_keyboard_profile, one_time_keyboard=True)
keyboard_go = [['Вперёд!']]
markup_go = ReplyKeyboardMarkup(keyboard_go, one_time_keyboard=True)


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
    await update.message.reply_text(
        f"Теперь я знаю эти факты о тебе: {facts_to_str(user_data)}\nМожем начинать искать друзей!",
        reply_markup=markup_go)
    id = update.message.from_user.id
    nick = update.message.from_user.username
    if database_funcs.check_if_user_in_base(id) is None:
        name = institute = course = ''
        if 'имя' in user_data.keys():
            name = user_data['имя']
        if 'курс' in user_data.keys():
            course = user_data['курс']
        if 'институт' in user_data.keys():
            institute = user_data['институт']
        database_funcs.add_user_to_base(id, name, course, institute, nick)
    user_data.clear()
    return CHOOSING_DIRECTION


async def direction(update, context):
    reply_keyboard_dir = [['Study Buddy'], ['Сообедник'], ['Товарищ по увлечениям'], ['Земляк'], ['Чел с языком']]
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
        res += f'Имя: {inf[0]}\nИнститут: {inf[1]}\nКурс: {inf[2]}\nКонтакт: @{inf[3]}\n\n'

    await update.message.reply_text(res)

    database_funcs.add_subject(id, subj)
    return FIX_SUBJECT


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
        res += f'Имя: {inf[0]}\nИнститут: {inf[1]}\nКурс: {inf[2]}\nКонтакт: @{inf[3]}\n\n'

    await update.message.reply_text(res)

    database_funcs.add_subject(id, hobby)
    return FIX_HOBBY


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
                MessageHandler(filters.Regex("^Товарищ по увлечениям$"), hobby)

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
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Закончить$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Закончить$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Закончить$"), done)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
