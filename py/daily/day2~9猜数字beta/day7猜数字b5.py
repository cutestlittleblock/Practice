import random

##########################################################################

def guess_game(num_max):                    #参数：函数定义时预留的接收入口，调用时外部数据由此进入函数，占位名为形式参数（形参），调用那一刻能算出值的任何东西为实际参数（实参）
    guesses=[]
    num=None
    key=random.randint(1,num_max)

    while num!=key:
        num=int(input("请猜数字："))
        guesses.append(num)
        if num<key:
            print("猜小了！")
        elif num>key:
            print("猜大了！")
    print("恭喜你猜对了！")
    return {"答案":key,"猜测":guesses}                  #函数可return字典

##########################################################################

answer=input("是否开始游戏？是为y,输入任意字符为否:")
data=[]                 #data=答案+猜测
guesses_num=0
level_difficulties={1:10,2:100,3:200,4:1000}                    #变量={}为“字典”，字典中冒号前后为一一对应关系，即{键:值}

while answer=="y":                  #开始条件判断
    prompt="请选择难度：难度1为（1~10）难度2为（1~100）难度3为（1~200）难度4为（1~1000）你选择难度："
    level=int(input(prompt))                   #难度判断
    while level not in level_difficulties:                   #校验循环，判断多种变量值时用and（与）或not in（非）
        if level>4:
            print("这太难了！")
            level=int(input(prompt))
        else:
            print("太简单了！")
            level=int(input(prompt))

    num_max=level_difficulties[level]                   #字典[键]→值

    result=guess_game(num_max)                  #调用函数，游戏开始
    data.append(result)

    for n,history in enumerate(data):                   #enumerate=编号（从0开始），元素#history[0]=key,history[1]=guesses
        print(f"第{n+1}局历史记录：{history}")
        print(f"该局猜过的数字有{history["猜测"]}，该局答案为{history["答案"]}！")

    guesses_num=guesses_num+len(result["猜测"])

    answer=input("是否开始游戏？是为y，输入任意字符为否:")

print("感谢游玩！")
print(f"你总共猜了{len(data)}局")
print(f"你总共猜了{guesses_num}次！")
if len(data)>0:
    print(f"平均每局猜{guesses_num/len(data)}次！")