from vkbottle.bot import BotLabeler, Message

help_labeler = BotLabeler()

@help_labeler.message(command="help")
async def help_handler(message: Message):
    text = (
    "Список доступных комманд:\n\n"
    "/new – создать новую очередь (для избранных).\n"
    "/end – встать в конец очереди.\n"
    "/list – текущие очереди.\n"
    "/skip – пропустить 24ч.\n"
    "/drop – сбросить очередь (для избранных).\n"
    "/admins – список избранных." 
    )
    await message.answer(text)
