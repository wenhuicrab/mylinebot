from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import StickerSendMessage
from linebot.models import ImageSendMessage
from linebot.models import LocationSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
import datetime
import random
def index(request):
    return HttpResponse("hello")

import requests
from bs4 import BeautifulSoup

def getInvoice():
    url = "https://invoice.etax.nat.gov.tw"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    headers = {'User-Agent': user_agent}
    html = requests.get(url, headers=headers)
    # html = requests.get(url)
    html.encoding ='uft-8'
    soup = BeautifulSoup(html.text, 'html.parser')

    period = soup.find("a", class_="etw-on")
    rr = period.text+"\n"

    nums = soup.find_all("p", class_="etw-tbiggest")
    rr += "特別獎：" + nums[0].text + "\n"
    rr += "特獎：" + nums[1].text + "\n"
    rr += "頭獎：" + nums[2].text.strip() +" "+ nums[3].text.strip() +" "+ nums[4].text.strip()

    return rr
def multiplication_quiz(reply_token):
    correct_count = 0
    
    while correct_count < 10:
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        
        correct_answer = num1 * num2
        
        while True:
            try:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f"{num1} * {num2} 是多少？")
                )
                
                user_answer = int(input(f"{num1} * {num2} 是多少？ "))  # 在實際運行中，這裡的 input 需要改成從 Line Bot 接收使用者回答的方式
                
                if user_answer == correct_answer:
                    correct_count += 1
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text="恭喜你答對了！")
                    )
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text=f"已經答對了 {correct_count} 題！")
                    )
                    break
                else:
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text="嗯...再多想想答案吧")
                    )
                    
            except ValueError:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="請輸入有效的數字！")
                )
    
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text="恭喜你成功答對十題，做得很好！")
    )

def getNews(num=10):
    """"擷取中央社新聞"""
    url = "https://www.cna.com.tw/list/aall.aspx"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'}
    html = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(html.text, 'html.parser')
    soup.encoding = 'utf-8'
    
    allnews = soup.find(id="jsMainList")
    nn = allnews.find_all('li')
    
    mm = ""
    for n in nn[:num]:
        mm += n.find('div',class_='date').text +' '
        mm += n.find('h2').text +'\n'
        mm += 'https://www.cna.com.tw/' + n.find('a').get('href') +'\n'
        mm += '-'*30+'\n'
    return mm


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
                        StickerSendMessage(package_id=11537, sticker_id=52002738)
                    )

                elif msg=='你是誰':
                    msg = '我是蔣中正!'
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )

                elif msg== 'guess':
                    num = random.randint(1,10)
                    msg = f"{num}"
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )
                    
                elif msg=='最新消息' or msg=='今日新聞':
                    sms = getNews(6)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=sms)
                    )

                elif msg=='統一發票':
                    msg = getInvoice()
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
                elif msg.startswith('今天誰'):
                    names = ['馮雅嵐','鍾旻蓁','陳玟卉','施芷庭','吉彥安']
                    msg = msg.replace('誰','')+'的是:'+random.choice(names)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )
                 elif msg == ('九九乘法表'):
                    multiplication_quiz(event.reply_token)

                else:
                    tdnow = datetime.datetime.now()
                    msg = tdnow.strftime("%Y/%m/%d, %H:%M:%S") + '\n' + event.message.text
                    # 回傳收到的文字訊息
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
