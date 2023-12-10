from icecream import ic
from vkbottle import GroupEventType, GroupTypes
from vkbottle.bot import BotLabeler, Message

from ..filters import EventDataRule
from app import PEER_ID_OFFSET
from app.functions import get_admins, get_name_from_user_id, check_admins_answer

admins_labeler = BotLabeler()

@admins_labeler.message(command="admins")
async def admins_handler(message: Message):
    group_id = message.peer_id - PEER_ID_OFFSET    
    admins_id = get_admins(group_id)

    if admins_id is None:
        await message.answer("Администраторы не назначены.")
        return

    admins_names = [await get_name_from_user_id(admin_id) for admin_id in admins_id]

    title = "Список администраторов:\n"
    text = "\n".join([f"{i+1}. {admin}" for i, admin in enumerate(admins_names)])
    answer = title + text
    
    await message.answer(answer)