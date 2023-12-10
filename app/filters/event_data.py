from vkbottle import GroupEventType, GroupTypes
from vkbottle.dispatch.rules import ABCRule

class EventDataRule(ABCRule):
    def __init__(self, cmd: str):
        self._cmd = cmd

    async def check(self, event: GroupTypes.MessageEvent) -> bool:
        return event.object.payload.get("cmd") == self._cmd
