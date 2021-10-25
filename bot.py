import logging
from aiogram.types import ContentType
import config
from shazam import shazam_voice
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Знакомство с ботом `/start`
    """
    await message.reply("Хелоу 🙈 \nНайду песню по звуковом сообщение 🔍")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    помощ юзеру `/help`
    """
    await message.answer("""Отправь мне голосовое сообщение с песней (мин 3 секунды) 🔍""")


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    voice = await bot.get_file(message.voice.file_id)
    sound = shazam_voice(voice.file_path)

    if sound['result'] is None:
        await message.reply(f"{message.chat.first_name}, мне не удалось найти ")
    else:
        spotify_btn = InlineKeyboardButton('Spotify 💚', url=sound['result']['spotify']['external_urls']['spotify'])
        inline_kb1 = InlineKeyboardMarkup().add(spotify_btn)
        await message.answer(
            f""" \
            {sound['result']['title'].strip()} от #{sound['result']['artist'].replace(' ', '_').strip()}
            """, reply_markup=inline_kb1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
