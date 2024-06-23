import random

def multiplication_quiz():
    while True:  # 使用內部迴圈處理輸入錯誤的情況
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        
        # 計算正確答案
        correct_answer = num1 * num2
        
        try:
            # 提示題目並讀取使用者的回答
            user_answer = int(input(f"{num1} * {num2}是多少? "))
            
            # 檢查答案是否正確
            if user_answer == correct_answer:
                return "恭喜你答對了!\n"
            else:
                return "嗯...再多想想答案吧\n"
                
        except ValueError:
            return "請輸入有效的數字!\n"
