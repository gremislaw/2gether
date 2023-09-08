# from telegram import ReplyKeyboardMarkup
# from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import database_funcs
from secret import TOKEN

#
# state = 0
# reply_keyboard_main = [['Study buddy'], ['Чувак чтоб вместе пообедать'], ['Товарищ по интересам'], ['Земляк'], ['На другом языке']]
# reply_keyboard_ege = [['Кто я', 'Задание'], ['Теория', 'Анекдот'], ['Команды', 'На главную']]
# markup_main = ReplyKeyboardMarkup(reply_keyboard_main, one_time_keyboard=False)
# markup_ege = ReplyKeyboardMarkup(reply_keyboard_ege, one_time_keyboard=False)
# messages = dict(initial="Я могу помочь тебе с поиском друзей "
#                         "Выбери, кого ты хочешь найти",
#                 unclear_num="Я не понимаю, какой номер ты имел в виду... Попробуй еще раз")
#
#
# def main():
#     updater = Updater(TOKEN, use_context=True)
#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler('start', start))
#     dp.add_handler(MessageHandler(Filters.text, text))
#     updater.start_polling()
#     updater.idle()
#
#
# def start(update, context):
#     global id, markup_main
#
#
#
#     id = update.message.from_user.id
#     if database_funcs.check_if_user_in_base(id) is None:
#         update.message.reply_text('Привет! Круто, что ты поступил в МИСИС. Я могу помочь тебе освоиться')
#         update.message.reply_text('Заполни, пожалуйства, небольшую анкету, она нужна, чтобы лучше помочь тебе')
#         name(update)
#
#
#         update.message.reply_text('Приятно познакомиться!\nНа каком ты курсе?')
#         course = update.message.text
#         update.message.reply_text('Отлично\nВ каком институте ты учишься?')
#         institute = update.message.text
#         database_funcs.add_user_to_base(id, name, institute, course)
#     update.message.reply_text(messages['initial'], reply_markup=markup_main)
#
#
# def name(update):
#     global state
#     update.message.reply_text('Твое имя?')
#     name = update.message.text
#     state = name
#
#
# def text(update, context):
#     global state, markup_ege
#     req = update.message.text.lower()
#     if state == name:
#         update.message.reply_text('Идём дальше', reply_markup=markup_ege)
#     if req == 'подготовка к егэ':
#         start_ege(update, context)
#     elif req == 'вопросы собеседования по сетям':
#         net_question(update, context)
#
#     elif req == 'выйти':
#         update.message.reply_text('Идём дальше', reply_markup=markup_ege)
#     else:
#         update.message.reply_text('Я тебя не понимаю. Напиши "команды", чтобы узнать список доступных функций.')
#
#
# if __name__ == '__main__':
#     main()


# !/usr/bin/env python
# pylint: disable=unused-argument, import-error
# This program is dedicated to the public domain under the CC0 license.

from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

CHOOSING_PROFILE, TYPING_REPLY, TYPING_CHOICE, CHOOSING_DIRECTION = range(4)

reply_keyboard_profile = [['Имя'], ['Курс'], ['Институт'], ['Закончить']]
markup_profile = ReplyKeyboardMarkup(reply_keyboard_profile, one_time_keyboard=True)
keyboard_go = [['Вперёд!']]
markup_go = ReplyKeyboardMarkup(keyboard_go, one_time_keyboard=True)

def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key.capitalize()} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def profile(update, context):
    id = update.message.from_user.id
    if database_funcs.check_if_user_in_base(id) is None:
        await update.message.reply_text(
            "Привет! Круто, что ты поступил в МИСИС. Я могу помочь тебе освоиться. "
            "Заполни, пожалуйства, небольшую анкету, она нужна, чтобы лучше помочь тебе",
            reply_markup=markup_profile)
        return CHOOSING_PROFILE
    else:
        await update.message.reply_text(
            "Информацию о тебе я уже знаю. "
            "Можем приступать",
            reply_markup=markup_go,
        )
        return CHOOSING_DIRECTION


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    if text == 'институт':
        await update.message.reply_text(f"В каком институте ты учишься?",  reply_markup=markup_inst)

    return TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


async def direction(update, context):
    user_data = context.user_data
    text = update.message.text

    await update.message.reply_text(
        "Круто!",
        reply_markup=markup_profile,
    )
    return CHOOSING_PROFILE


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]
    await update.message.reply_text(
        f"Теперь я знаю эти факты о тебе: {facts_to_str(user_data)}\nМожем начинать искать друзей!",
        reply_markup=markup_go)
    id = update.message.from_user.id
    if database_funcs.check_if_user_in_base(id) is None:
        name = institute = course = ''
        if 'имя' in user_data.keys():
            name = user_data['имя']
        if 'курс' in user_data.keys():
            course = user_data['курс']
        if 'институт' in user_data.keys():
            institute = user_data['институт']
        database_funcs.add_user_to_base(id, name, course, institute)
    user_data.clear()
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
                    filters.Regex("^(Вперёд!)$"), direction
                )
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
