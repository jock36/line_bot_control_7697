import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

led_status = '0'


channel_secret = 'cae3f7bc69b39097ed1e4a1a573d8d60'
channel_access_token = '5eWbZ8CVW0UQPJbQs6bBGS9IZS29mj8p9GZa9EhF9so3O25MreKhSqVIh8+s3kFlIT79ep1TpnIolf71haF7byeBeLWwqRgt8kbUDoNuhWxs7n1EjhR8L7rmf8Qh7jZGxv9S8RK9LUR54s3txuFuxwdB04t89/1O/w1cDnyilFU='

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/")
def control_led():
    global led_status
    return led_status

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    global led_status
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
    print event.message.text

    in_w = event.message.text[0]
    
    if ('開' == in_w.encode('utf-8')):
        led_status = '1'
    elif('關' == in_w.encode('utf-8')):
        led_status = '0'
    print "led狀態:" + led_status

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
