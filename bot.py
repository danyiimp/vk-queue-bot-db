import os
import logging

from vkbottle.bot import Bot, BotLabeler, rules
from dotenv import load_dotenv
from app.handlers import labelers

load_dotenv()
token = os.getenv("token")

def main():
    #TODO: Добавить default админов и возможность добавлять их через команду
    logging.getLogger("vkbottle").setLevel(logging.INFO)

    global_labeler = BotLabeler()
    global_labeler.auto_rules = [rules.PeerRule(from_chat=True)]
    
    for labeler in labelers:
        global_labeler.load(labeler)

    bot = Bot(token=token, labeler=global_labeler)
    bot.run_forever()

if __name__ == "__main__":
    main()
