import json
import asyncio

from icecream import ic
from vkbottle import GroupEventType, GroupTypes
from vkbottle.bot import BotLabeler, Message

from ..filters import EventDataRule
from ..db import  get_skips, update_skips, remove_skip
from app import PEER_ID_OFFSET
from app.functions import get_queues_keyboard, get_name_from_user_id


skip_labeler = BotLabeler()
skip_labeler.custom_rules["event_data"] = EventDataRule

@skip_labeler.message(command="skip")
async def skip_handler(message: Message):
    group_id = message.peer_id - PEER_ID_OFFSET

    keyboard = get_queues_keyboard("skip", group_id)
    if keyboard is None:
        await message.answer("Очереди не созданы. Используйте /new <имя_очереди>")
        return
    
    await message.answer("Пропустить 24 часа в очереди:", keyboard=keyboard)

@skip_labeler.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent, event_data="skip")
async def skip_callback_handler(event: GroupTypes.MessageEvent):
    group_id = event.object.peer_id - PEER_ID_OFFSET
    queue_name = event.object.payload.get("queue_name")
    user_id = event.object.user_id
    

    skips = get_skips(group_id, queue_name)
    if skips is None:
        await event.ctx_api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({"type": "show_snackbar", "text": f"Очереди {queue_name} больше не существует."})
        )
        return

    if user_id in skips:
        await event.ctx_api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({"type": "show_snackbar", "text": f"Вы уже пропускаете 24 часа в очереди c названием {queue_name}."})
        )
        return
    else:
        update_skips(group_id, queue_name, user_id)

    await event.ctx_api.messages.send(
        peer_id=event.object.peer_id,
        message=f"{await get_name_from_user_id(user_id)} пропускает 24 часа в очереди с названием {queue_name}.",
        random_id=0
    )

    await event.ctx_api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        peer_id=event.object.peer_id,
        user_id=event.object.user_id,
        event_data=json.dumps({"type": "show_snackbar", "text": f"Вы пропускаете 24 часа в очереди c названием {queue_name}."})
    )

    skip_in_sec = 60 * 60 * 24
    await asyncio.sleep(skip_in_sec)
    remove_skip(group_id, queue_name, user_id)