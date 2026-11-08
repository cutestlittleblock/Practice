import random

##########################################################################

def guess_game(num_min,num_max):                    #游戏主体函数
    guesses=[]
    num=None
    key=random.randint(num_min,num_max)

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


##########################################################################

def history_print(data):                    #历史打印函数
    for n,history in enumerate(data):                   #enumerate=编号（从0开始），元素
        print(f"第{n+1}局历史记录：{history}")                  #history["答案"]=key,history["猜测"]=guesses
        print(f"该局猜过的数字有{history["猜测"]}，该局答案为{history["答案"]}！")

##########################################################################


##########################################################################

def game_stats(data):                   #值型收官函数
    guesses_num=0

    for game_result_g_s in data:
        guesses_num_list=game_result_g_s["猜测"]
        guesses_num=guesses_num+len(guesses_num_list)
        
    if len(data)==0:
        guesses_average=0
    else:
        guesses_average=guesses_num/len(data)
    
    return{"局数":len(data),"总次数":guesses_num,"平均":guesses_average}

##########################################################################

start="是否开始游戏？是为y,输入任意字符为否:"
answer=input(start)
data=[]                 #data=列表:[字典{"答案":...,"猜测":...}]
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
    num_min=1

    game_result=guess_game(num_min,num_max)                  #调用函数，游戏开始
    data.append(game_result)

    history_print(data)

    answer=input(start)

stats=game_stats(data)

print("感谢游玩！")
print(f"你总共猜了{stats["局数"]}局,你总共猜了{stats["总次数"]}次！平均每局猜{stats["平均"]}次！")