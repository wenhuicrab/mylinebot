import random

def multiplication_quiz():

        # 計算正確答案
        correct_answer = num1 * num2
        
        while True:  # 使用內部迴圈處理輸入錯誤的情況
            try:
                # 提示題目並讀取使用者的回答
                user_answer = int(input(f"{num1} * {num2}是多少? "))
                
                # 檢查答案是否正確
                if user_answer == correct_answer:
                    return f"恭喜你答對了! 已經答對了 {correct_count} 題！\n"
                else:
                    return "嗯...再多想想答案吧\n"
                    
            except ValueError:
                return "請輸入有效的數字!\n"
    
    # 當答對十題時，顯示鼓勵訊息
    return "恭喜你成功答對十題，做得很好！"
