from vkbottle import GroupEventType, GroupTypes
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from ..db import get_admins
from app import PEER_ID_OFFSET

class AdminsRule(ABCRule):
    async def check(self, message: Message) -> bool:
        user_id = message.from_id
        group_id = message.peer_id - PEER_ID_OFFSET
        admins = get_admins(group_id)
        if user_id in admins:
            return True
        return False

