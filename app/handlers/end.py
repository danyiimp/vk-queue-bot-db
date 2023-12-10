import json

from icecream import ic
from vkbottle import GroupEventType, GroupTypes
from vkbottle.bot import BotLabeler, Message

from ..filters import EventDataRule
from ..db import update_queue
from app import PEER_ID_OFFSET
from app.functions import get_queues_keyboard, get_name_from_user_id

end_labeler = BotLabeler()
end_labeler.custom_rules["event_data"] = EventDataRule

@end_labeler.message(command="end")
async def end_handler(message: Message):
    group_id = message.peer_id - PEER_ID_OFFSET

    keyboard = get_queues_keyboard("end", group_id)
    if keyboard is None:
        await message.answer("Очереди не созданы. Используйте /new <имя_очереди>")
        return
    
    await message.answer("Встать в конец очереди:", keyboard=keyboard)

@end_labeler.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent, event_data="end")
async def end_callback_handler(event: GroupTypes.MessageEvent):
    group_id = event.object.peer_id - PEER_ID_OFFSET
    queue_name = event.object.payload.get("queue_name")
    user_id = event.object.user_id
    
    position = update_queue(group_id, queue_name, user_id)

    if position is None:
        await event.ctx_api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({"type": "show_snackbar", "text": f"Очереди {queue_name} больше не существует."})
        )
        return

    await event.ctx_api.messages.send(
        peer_id=event.object.peer_id,
        message=f"{await get_name_from_user_id(user_id)} занимает очередь с названием {queue_name}.",
        random_id=0
    )

    await event.ctx_api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        peer_id=event.object.peer_id,
        user_id=event.object.user_id,
        event_data=json.dumps({"type": "show_snackbar", "text": f"Вы встали в конец очереди c названием {queue_name} на {position} место."})
    )