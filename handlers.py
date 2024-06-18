from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
import text
from utils import *


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):

    await msg.answer(text.greet_unknown_user % {'username': msg.from_user.username})


# @router.message(F.document)
# async def file_handler(msg: Message):
#     pass


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Неизвестная команда", )
