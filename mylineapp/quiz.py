import random
from linebot.models import TextSendMessage

def start_quiz(reply_token, line_bot_api):
    global waiting_for_answer, current_question, correct_count
    waiting_for_answer = True
    correct_count = 0  # 初始化正確答題計數器
    multiplication_quiz(reply_token, line_bot_api)

def handle_answer(msg, reply_token, line_bot_api):
    global waiting_for_answer, correct_count
    
    try:
        user_answer = int(msg)
        
        # 取得目前的題目
        num1, num2, correct_answer = current_question
        
        if user_answer == correct_answer:
            print("恭喜你答對了！")
            correct_count += 1  # 正確答題計數器加一
            
            if correct_count < 10:
                multiplication_quiz(reply_token, line_bot_api)
            else:
                end_quiz()
        else:
            print("嗯...再多想想答案吧")
        
    except ValueError:
        print("請輸入有效的數字！")

def multiplication_quiz(reply_token, line_bot_api):
    global current_question
    
    while correct_count < 10:
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        
        correct_answer = num1 * num2
        
        current_question = (num1, num2, correct_answer)
        
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=f"{num1} * {num2} 是多少？")
        )
        
        # 等待使用者回答，這裡示範等待使用者回答的方式
        return

    print("恭喜你成功答對十題，做得很好！")

def end_quiz():
    global waiting_for_answer, correct_count
    waiting_for_answer = False
    correct_count = 0
    print("測驗結束")

# 在這裡可以添加更多需要的功能或函式
