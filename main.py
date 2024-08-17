import logging

from wxhook import Bot
from wxhook import events
from wxhook.model import Event

import re

pattern = r"二维码赞赏到账(\d+\.\d+)元"

def on_login(bot: Bot, event: Event):
    print("登录成功之后会触发这个函数")


def on_start(bot: Bot):
    print("微信客户端打开之后会触发这个函数")


def on_stop(bot: Bot):
    print("关闭微信客户端之前会触发这个函数")


def on_before_message(bot: Bot, event: Event):
    print("消息事件处理之前")


def on_after_message(bot: Bot, event: Event):
    title = event.content["msg"]["appmsg"]["title"]
    match = re.search(pattern, title)
    if match:
        amount = match.group(1)
        logging.info(f"收款 {amount}")
    # todo


bot = Bot(
    # faked_version="3.9.10.19", # 解除微信低版本限制
    on_login=on_login,
    on_start=on_start,
    on_stop=on_stop,
    on_before_message=on_before_message,
    on_after_message=on_after_message
)


# 消息回调地址
# bot.set_webhook_url("http://127.0.0.1:8000")

@bot.handle(events.TEXT_MESSAGE)
def on_message(bot: Bot, event: Event):
    bot.send_text("filehelper", "hello world!")


bot.run()
