from aiogram import executor
from dispatcher import dp
import handlers

from database.db import BotDB

BotDB = BotDB('users.db')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
