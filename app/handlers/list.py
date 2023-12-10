import json

from icecream import ic
from vkbottle import GroupEventType, GroupTypes
from vkbottle.bot import BotLabeler, Message

from ..filters import EventDataRule
from ..db import get_queue, get_skips
from app import PEER_ID_OFFSET
from app.functions import get_queues_keyboard, get_name_from_user_id, get_skip_text

list_labeler = BotLabeler()
list_labeler.custom_rules["event_data"] = EventDataRule

@list_labeler.message(command="lists")
async def list_handler(message: Message):
    group_id = message.peer_id - PEER_ID_OFFSET

    keyboard = get_queues_keyboard("list", group_id)
    if keyboard is None:
        await message.answer("Очереди не созданы. Используйте /new <имя_очереди>")
        return
    
    await message.answer("Посмотреть список:", keyboard=keyboard)

@list_labeler.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent, event_data="list")
async def list_callback_handler(event: GroupTypes.MessageEvent):
    group_id = event.object.peer_id - PEER_ID_OFFSET
    queue_name = event.object.payload.get("queue_name")

    queue = get_queue(group_id, queue_name)

    if queue is None:
        await event.ctx_api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({"type": "show_snackbar", "text": f"Очереди {queue_name} больше не существует."})
        )
        return
        
    if len(queue) == 0:
        answer = f"Очередь {queue_name} несформирована.\nИспользуйте /end чтобы встать в очередь."
    else:
        skips = get_skips(group_id, queue_name)
        names = [await get_name_from_user_id(user_id) for user_id in queue]
        skips_text = [get_skip_text(user_id, skips) for user_id in queue]

        title = f"Список очереди {queue_name}:\n"
        text = "\n".join([f"{i+1}. {names[i]} {skips_text[i]}" for i in range(len(names))])
        answer = title + text
    
    await event.ctx_api.messages.send(
        peer_id=event.object.peer_id,
        message=answer,
        random_id=0
    )

    await event.ctx_api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        peer_id=event.object.peer_id,
        user_id=event.object.user_id,
    )
