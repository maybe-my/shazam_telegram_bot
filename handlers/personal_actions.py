from aiogram import types
from dispatcher import dp
import config
from aiogram.types import ContentType
from bot import BotDB
from dispatcher import bot 
from shazam import shazam_voice
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import datetime


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Знакомство с ботом `/start`
    """

    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id, message.from_user.username)
    opts = { "hey" : ('Привет', 'Здравствуйте', 'Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи')}

    now = datetime.datetime.now()
    if now.hour > 4 and now.hour <= 12 :
        greet = opts["hey"][2]
    if now.hour > 12 and now.hour <= 16 :
        greet = opts["hey"][3]
    if now.hour > 16 and now.hour <= 24 :
        greet = opts["hey"][4]
    if now.hour >= 0 and now.hour <= 4 :
        greet = opts["hey"][5]

    await message.answer(f"{greet}, Отправь мне голосовое сообщение с песней (мин 3 секунды) 🔍")


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    voice = await bot.get_file(message.voice.file_id)
    sound = shazam_voice(voice.file_path)

    if sound['result'] is None:
        await message.reply(f"{message.chat.first_name}, мне не удалось найти ")
    else:
        if(BotDB.user_exists(message.from_user.id)):
            spotify_btn = InlineKeyboardButton('Spotify 💚', url=sound['result']['spotify']['external_urls']['spotify'])
            # apple_btn = InlineKeyboardButton('Apple Music 🖤', url=sound['result']['apple_music']['previews']['url'])
            inline_kb1 = InlineKeyboardMarkup().add(spotify_btn)
            
            await message.answer(
                f""" \
                {sound['result']['title'].strip()} by #{sound['result']['artist'].replace(' ', '_').strip().replace(',', '')}
                """, reply_markup=inline_kb1)
        else:
            await message.answer(
                f"Вы не зарегистрировались! Нажмите /start для регистрации", reply_markup=None)
