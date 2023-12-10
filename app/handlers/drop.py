from icecream import ic
from vkbottle import GroupEventType, GroupTypes
from vkbottle.bot import BotLabeler, Message

from ..filters import EventDataRule
from ..db import drop_queue, get_admins
from app import PEER_ID_OFFSET
from app.functions import check_admins_answer, get_queues_keyboard

drop_labeler = BotLabeler()
drop_labeler.custom_rules["event_data"] = EventDataRule

drop_message_id = None

@drop_labeler.message(command="drops")
async def drop_handler(message: Message):
    global drop_message_id
    user_id = message.from_id
    group_id = message.peer_id - PEER_ID_OFFSET
    if not await check_admins_answer(message, user_id, group_id):
        return
    
    keyboard = get_queues_keyboard("drop", group_id)
    if keyboard is None:
        await message.answer("Очереди не созданы. Используйте /new <имя_очереди>")
        return

    drop_message = message.answer("Удалить очередь:", keyboard=keyboard)
    drop_message_id = (await drop_message).conversation_message_id

@drop_labeler.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent, event_data="drop")
async def drop_callback_handler(event: GroupTypes.MessageEvent):
    global drop_message_id
    group_id = event.object.peer_id - PEER_ID_OFFSET
    user_id = event.object.user_id
    queue_name = event.object.payload.get("queue_name")

    admins = get_admins(group_id)
    if admins is None:
        await event.ctx_api.messages.send(
            peer_id=event.object.peer_id,
            message="Администраторы не назначены.",
            random_id=0
        )
        return

    if user_id not in admins:
        await event.ctx_api.messages.send(
            peer_id=event.object.peer_id,
            message="Недостаточно прав.",
            random_id=0
        )
        return
        
    await event.ctx_api.messages.delete(
        peer_id=event.object.peer_id,
        cmids=drop_message_id,
        delete_for_all=1
    )

    if drop_queue(group_id, queue_name):
        await event.ctx_api.messages.send(
            peer_id=event.object.peer_id,
            message=f"Очередь {queue_name} была удалена.",
            random_id=0
        )
    else:
        await event.ctx_api.messages.send(
            peer_id=event.object.peer_id,
            message=f"Очередь {queue_name} уже удалена.",
            random_id=0
        )

    await event.ctx_api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        peer_id=event.object.peer_id,
        user_id=event.object.user_id
    )