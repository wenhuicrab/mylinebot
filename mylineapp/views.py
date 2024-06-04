from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import StickerSendMessage
from linebot.models import ImageSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
import datetime
import random
def index(request):
    return HttpResponse("hello")


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            # 若有訊息事件
            if isinstance(event, MessageEvent):

                msg = event.message.text
                imgurl="https://i.imgur.com/6hVi7dy.gif"

                if msg=='hello' or msg=='hi'or msg=='嗨'or msg=='哈囉':
                    # 回傳貼圖
                    line_bot_api.reply_message(
                        event.reply_token,
                        StickerSendMessage(package_id=789, sticker_id=10856)
                    )

                elif msg=='你是誰':
                    msg = '我是蔣中正!'
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )

                elif msg== '猜數字':
                    num = random.randint(1,100)
                    msg = f"{num}"
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )

                elif msg=='求籤' or msg=='抽籤':
                    num = random.randint(1,100)
                    img = f"https://www.lungshan.org.tw/fortune_sticks/images/{num:03d}.jpg"

                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url=img,
                        preview_image_url=img)
                    )

                else:
                    tdnow = datetime.datetime.now()
                    msg = tdnow.strftime("%Y/%m/%d, %H:%M:%S") + '\n' + event.message.text
                    # 回傳收到的文字訊息
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg),
                        ImageSendMessage(original_content_url=imgurl,
                        preview_image_url=imgurl)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()