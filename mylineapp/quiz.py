import random

current_question = None
correct_count = 0

def start_quiz():
    global current_question, correct_count
    correct_count = 0
    multiplication_quiz()

def handle_answer(msg):
    global correct_count
    
    try:
        user_answer = int(msg)
        
        # 取得目前的題目
        num1, num2, correct_answer = current_question
        
        if user_answer == correct_answer:
            correct_count += 1
            if correct_count < 10:
                multiplication_quiz()
            else:
                end_quiz()
        else:
            print("嗯...再多想想答案吧")
        
    except ValueError:
        print("請輸入有效的數字！")

def multiplication_quiz():
    global current_question
    
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    
    correct_answer = num1 * num2
    
    current_question = (num1, num2, correct_answer)
    
    print(f"{num1} * {num2} 是多少？")

def end_quiz():
    global correct_count
    correct_count = 0
    print("測驗結束")
