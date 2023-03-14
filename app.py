import json
import logging
import re

from khl import Bot, Message
from revChatGPT.V3 import Chatbot

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

ChatGPTConfig = {
    "api_key": config['openai_api_key']
}

if config["openai_engine"] != "":
    ChatGPTConfig["engine"] = config['openai_engine']

# init gpt api
gptApi = Chatbot(**ChatGPTConfig)

# init Bot
bot = Bot(token=config['kook_token'])


@bot.command(name='hi')
async def hello(msg: Message):
    await msg.reply("what's up bro!", use_quote=True)


@bot.command(name='help')
async def help(msg: Message):
    await msg.reply("使用 /ai 命令与ChatGPT聊天，例如：/ai 写一首诗", use_quote=True)


@bot.command(name='ai')
async def go_gpt(msg: Message, content: str):
    prompt = re.sub('(?:\s)<@[^, ]*|(?:^)<@[^, ]*', '', content)
    try:
        response = gptApi.ask(prompt)
    except Exception as e:
        print(e)
        response = "无法从OpenAI获得响应，API服务或者转发服务可能挂了..."

    await msg.reply(response)


if __name__ == "__main__":
    logging.basicConfig(level='INFO')
    bot.run()
