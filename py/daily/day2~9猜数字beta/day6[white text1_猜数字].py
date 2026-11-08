#**题目：凭记忆完整重写猜数字游戏**，功能要求：
#1. 每局随机生成 1~10 的答案，玩家反复猜，提示大了/小了，猜中结束本局
#2. 一局游戏封装成一个函数，返回这一局的完整记录
#3. 可以连续玩多局，所有局的记录存进一个总列表
#4. 每局结束后打印全部历史记录，带编号（第1局、第2局……），要求用 `enumerate()`
#5. 退出后打印：总局数、总猜测次数、平均每局次数
#6. 一局都没玩就退出时，程序不能报错


import random
def guess_game():
    key=random.randint(1,10)
    answer=None
    guesses=[]

    while answer!=key:
        answer=int(input("请猜数字："))
        guesses.append(answer)
        if answer>key:
            print("猜大了！")
        elif answer<key:
            print("猜小了！")
    print("恭喜你猜对了！")

    return(key,guesses)


data=[]
guesses_all=0
choose=input("输入“y”开始游戏，否则退出：")
while choose=="y":
    result=guess_game()
    data.append(result)
    guesses_all=guesses_all+len(result[1])
    for n,history in enumerate(data):
        print(f"本局答案为{history[0]}，你猜的答案有{history[1]}")
        print(f"第{n+1}局历史记录：{history}")
    choose=input("输入“y”开始游戏，否则退出：")

print(f"你一共猜了{len(data)}局")
if len(data)>0:
    print(f"总共猜了{guesses_all}次，平均每局猜{guesses_all/len(data)}次")
print("感谢游玩！")



#用时40min完成（20min敲完v1，20min修改两个bug完成）