import logging

import requests
from wxhook import Bot
from wxhook import events
from wxhook.model import Event

from apscheduler.schedulers.background import BackgroundScheduler

import re
import time
import hashlib

host = "xxx"
key = "xxx"

pattern = r"二维码赞赏到账(\d+\.\d+)元"

def calc_sign(data):
    md5_hash = hashlib.md5()
    md5_hash.update((data + key).encode('utf-8'))
    md5_hex = md5_hash.hexdigest()
    return md5_hex

def heartbeat():
    t = time.time()
    url = f"http://{host}/appHeart?t={t}&sign={calc_sign(t)}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            logging.info(f"心跳包发送成功 {r.content}")
    except Exception as e:
        logging.error("请检查地址是否配置正确")
        logging.error(f"当前地址 {host} 密钥 {key}")
        logging.error(e)

def cash(amount):
    t = time.time()
    sign = calc_sign(f"1{amount}{t}")
    url = f"http://{host}/appPush?t=${t}&type=1&price={amount}&sign={sign}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            logging.info(f"回调成功 {r.content}")
    except Exception as e:
        logging.error("回调失败")
        logging.error(e)

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
        cash(amount)


bot = Bot(
    faked_version="3.9.10.19", # 解除微信低版本限制
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

scheduler = BackgroundScheduler()
scheduler.add_job(heartbeat, 'interval', minutes=5)
scheduler.start()

bot.run()
