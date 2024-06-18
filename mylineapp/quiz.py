import random

def start_quiz(reply_token, line_bot_api):
    """
    啟動九九乘法表測驗，設置全域變量並呼叫第一個問題
    Args:
        reply_token (str): Line Bot 回覆 token
        line_bot_api (LineBotApi): Line Bot API 實例
    """
    global waiting_for_answer, current_question, correct_count
    waiting_for_answer = True
    correct_count = 0
    ask_question(reply_token, line_bot_api)

def ask_question(reply_token, line_bot_api):
    """
    提問下一個九九乘法表問題
    Args:
        reply_token (str): Line Bot 回覆 token
        line_bot_api (LineBotApi): Line Bot API 實例
    """
    global current_question
    
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
        
    correct_answer = num1 * num2
        
    current_question = (num1, num2, correct_answer)
        
    # 使用外部傳入的 line_bot_api 和 reply_token 來回覆訊息
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=f"{num1} * {num2} 是多少？")
    )

def handle_answer(msg, reply_token, line_bot_api):
    """
    處理使用者回答的九九乘法表問題
    Args:
        msg (str): 使用者回答的訊息
        reply_token (str): Line Bot 回覆 token
        line_bot_api (LineBotApi): Line Bot API 實例
    """
    global waiting_for_answer, correct_count
    
    try:
        user_answer = int(msg)
        
        # 取得目前的題目
        num1, num2, correct_answer = current_question
        
        if user_answer == correct_answer:
            correct_count += 1  # 正確答題計數器加一
            
            if correct_count < 10:
                ask_question(reply_token, line_bot_api)
            else:
                end_quiz(reply_token, line_bot_api)
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

def end_quiz(reply_token, line_bot_api):
    """
    結束九九乘法表測驗，重設相關全域變量
    Args:
        reply_token (str): Line Bot 回覆 token
        line_bot_api (LineBotApi): Line Bot API 實例
    """
    global waiting_for_answer, correct_count
    waiting_for_answer = False
    correct_count = 0
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text="恭喜你成功答對十題，做得很好！")
    )

# 在這裡可以添加更多需要的功能或函式
