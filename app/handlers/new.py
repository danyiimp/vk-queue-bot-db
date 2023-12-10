from typing import Tuple
from vkbottle.bot import BotLabeler, Message

from ..db import create_queue
from app import PEER_ID_OFFSET
from app.functions import check_admins_answer

new_labeler = BotLabeler()

@new_labeler.message(command=("new", 1))
async def new_handler(message: Message, args: Tuple[str]):
    user_id = message.from_id
    group_id = message.peer_id - PEER_ID_OFFSET
    if not await check_admins_answer(message, user_id, group_id):
        return
    
    queue_name = args[0]

    status = create_queue(group_id, queue_name)
    if status:
        await message.answer(f"Очередь {queue_name} создана.")
    else:
        await message.answer(f"Очередь {queue_name} уже существует.")
