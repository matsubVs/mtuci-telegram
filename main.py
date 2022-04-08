import os
import telebot
from telebot import types

from dotenv import load_dotenv
import time

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "/roll_the_dice", "/learn_googling", "/test", "/help")
    bot.send_message(
        message.chat.id,
        "Привет! Хочешь узнать свежую информацию о МТУСИ?",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["help"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Описание команд:\n"
        "Хочу - ссылка на официальный сайт МТУСИ\n"
        "/roll_the_dice - кинуть кости\n"
        "/learn_googling - если твой друг не умеет гуглить\n",
        "/test - пройти тест"
    )


@bot.message_handler(commands=["roll_the_dice"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Что же тебе выпало?\n"
    )

    dice = bot.send_dice(
        message.chat.id,
    )

    send_dice_answer(dice)

def send_dice_answer(dice_message):
    time.sleep(2)
    bot.send_message(
        dice_message.chat.id,
        f"Тебе выпало {dice_message.dice.value}!",
    )


@bot.message_handler(commands=["learn_googling"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Твой друг не умееть гуглить, и ты хочешь ему помочь?\n"
        "Этот сервис поможет - https://pogugli.com/"
    )


@bot.message_handler(commands=["test"])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="Учусь", callback_data="studying"))
    markup.add(telebot.types.InlineKeyboardButton(text="Работаю", callback_data="working"))
    markup.add(telebot.types.InlineKeyboardButton(text="Сплю", callback_data="sleeping"))
    bot.send_message(
        message.chat.id,
        text="Чем занимаешься?",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text="Спасибо за ответ!")
    reply = ""
    if call.data == "studying":
        reply = "Супер! Не забываю отдыхать"
    elif call.data == "working":
        reply = "Отлично! Опыть всегда пригодится"
    elif call.data == "sleeping":
        reply = "Это дело святое"
    bot.send_message(call.message.chat.id, reply)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(
            message.chat.id,
            "Хочешь попасть на оффициальный сайт МТУСИ?\n"
            "Тогда тебе сюда - https://mtuci.ru/",
        )


bot.infinity_polling()
