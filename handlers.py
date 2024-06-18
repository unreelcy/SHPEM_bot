from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
import text
from utils import *
from sql_utils import *


router = Router()


@router.message(Command("start"))  # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message):
    if find_user(str(msg.from_user.id)):
        await msg.answer(text.greet_user % {'username': msg.from_user.username})
    else:
        await msg.answer(text.greet_unknown_user % {'username': msg.from_user.username})


# @router.message(F.document)
# async def file_handler(msg: Message):
#     pass


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Неизвестная команда", )
