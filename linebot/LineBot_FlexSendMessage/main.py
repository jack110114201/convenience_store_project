from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json
import os
import app_recom
from ALS_to_Mysql import *
from django.core.validators import URLValidator

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('kX5eYU/Jbvk3CAZKloR5IXWlMM0HBp8kDCme1aRuyVYqLwcpCJ0Oq0+aSP4TvTH9rZc2DkK8C4NoFh5sYJ3bmu3Ep5O7zHWEl7ooh0EQWAXnWFgqDmLvLAwcwJ2rXGh+1gLoR8jRpAyXNJrBV6pKDAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b2f507155846a74ee6b71d4e8a85000d')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# handle FlexMessage
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    reply_token = event.reply_token
    message = event.message.text
    user_id = event.source.user_id
    if message == "推薦系統":
        FlexMessage = app_recom.recommend(user_id)
        if FlexMessage is None:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入商品名稱'))
        else:    
            line_bot_api.reply_message(reply_token,FlexSendMessage(alt_text='客製推薦',contents=dict(FlexMessage)))
    elif message == "apple":
        FlexMessage = app_recom.recommendP(message)
        if FlexMessage is None:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='查無相關商品'))
        else:    
            line_bot_api.reply_message(reply_token,FlexSendMessage(alt_text='相關推薦',contents=dict(FlexMessage)))
    else:
        pass


# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345)