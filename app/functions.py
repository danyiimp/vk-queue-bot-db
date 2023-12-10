import os

from vkbottle import Keyboard, Callback, KeyboardButtonColor
from vkbottle.bot import Message
from vkbottle import API

from .db import get_admins, get_queues_names
from dotenv import load_dotenv
from app import PEER_ID_OFFSET

load_dotenv()
token = os.getenv("token")
api = API(token=token)


async def check_admins_answer(message, user_id, group_id):
    user_id = message.from_id
    group_id = message.peer_id - PEER_ID_OFFSET
    admins = get_admins(group_id)
    if admins is None:
        await message.answer("Администраторы не назначены.")
        return False

    if user_id not in admins:
        await message.answer("Недостаточно прав.")
        return False
    return True
    
def get_queues_keyboard(cmd: str, group_id):
    queues_names = get_queues_names(group_id)
    if queues_names is None:
        return None
    keyboard = Keyboard(inline=True)
    for i, queue_name in enumerate(queues_names):
        keyboard.add(Callback(queue_name, {"cmd": cmd, "queue_name": queue_name}), color=KeyboardButtonColor.PRIMARY)
        if i != len(queues_names) - 1:
            keyboard.row()
    return keyboard.get_json()

async def get_name_from_user_id(user_id):
    user = (await api.users.get(user_id=user_id))[0]
    name = f"{user.first_name} {user.last_name}" 
    return name

def get_skip_text(user_id, skips):
    if user_id in skips:
        return " &#128683;"
    return ""