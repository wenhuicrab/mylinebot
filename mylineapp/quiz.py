import random

def start_quiz():
    global waiting_for_answer, current_question, correct_count
    waiting_for_answer = True
    correct_count = 0
    ask_question()

def ask_question(reply_token=None):
    global current_question
    
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
        
    correct_answer = num1 * num2
        
    current_question = (num1, num2, correct_answer)
        
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=f"{num1} * {num2} 是多少？")
    )

def handle_answer(msg, reply_token):
    global waiting_for_answer, correct_count
    
    try:
        user_answer = int(msg)
        
        # 取得目前的題目
        num1, num2, correct_answer = current_question
        
        if user_answer == correct_answer:
            correct_count += 1  # 正確答題計數器加一
            
            if correct_count < 10:
                ask_question(reply_token)
            else:
                end_quiz(reply_token)
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

def end_quiz(reply_token):
    global waiting_for_answer, correct_count
    waiting_for_answer = False
    correct_count = 0
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text="恭喜你成功答對十題，做得很好！")
    )
