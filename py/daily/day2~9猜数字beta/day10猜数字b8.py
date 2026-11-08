import random

##########################################################################

def ask_int():                  #值型判断函数
    while True:
        try:
            return int(input(""))
        except ValueError:
            print("至少输个整数吧宝宝。。。")

##########################################################################

def guess_game(num_min,num_max,chest):                    #游戏主体函数
    guesses=[]
    num=None
    if chest=="TRUE":
        key=num
    else:
        key=random.randint(num_min,num_max)

    while num!=key:
        print("请猜数字")
        num=ask_int()
        guesses.append(num)
        if num<key:
            print("猜小了！")
        elif num>key:
            print("猜大了！")

    print("恭喜你猜对了！")

    return {"答案":key,"猜测":guesses}                  #函数可return字典

##########################################################################

##########################################################################

def choose_level(level_difficulties):                   #难度选择函数
    for dif_key in level_difficulties:
        dif_max=level_difficulties[dif_key]
        print(f"难度{dif_key}为（1~{dif_max}）")

    print("请选择难度：")

    level_chose=ask_int()                   #难度判断

    while level_chose not in level_difficulties:                   #校验循环，判断多种变量值时用and（与）或not in（非）
        if level_chose==274380:   
            print("littleblock is watching YOU...")
            print("how did you get that number?!")
            print("...and you win...?")
            break
        elif level_chose<min(level_difficulties):
            print("宝宝这太简单了。。。")
        elif level_chose>max(level_difficulties):
            print("宝宝这太难了吧。。。")
        else:
            print("唔嘿~这个还没做~")
        level_chose=ask_int()
    return level_chose

##########################################################################

def history_print(data):                    #历史打印函数
    for n,history in enumerate(data):                   #enumerate=编号（从0开始），元素
        print(f"第{n+1}局历史记录：{history}")                  #history["答案"]=key,history["猜测"]=guesses
        print(f"该局猜过的数字有{history["猜测"]}，该局答案为{history["答案"]}！")

##########################################################################

def game_stats(data):                   #值型收官函数
    if len(data)==0:
        return{"局数":0,"总次数":0,"平均":0}
              
    guesses_num=0

    for game_result_g_s in data:
        guesses_num=guesses_num+len(game_result_g_s["猜测"])

    return{"局数":len(data),"总次数":guesses_num,"平均":guesses_num/len(data)}

##########################################################################

start="是否开始游戏？是为y,输入任意字符为否:"
answer=input(start)
data=[]                 #data=列表:[字典{"答案":...,"猜测":...}]
level_difficulties={1:10,2:100,3:200,4:1000,9:5000}                    #变量={}为“字典”，字典中冒号前后为一一对应关系，即{键:值}

while answer=="y":                  #开始条件判断
    level=choose_level(level_difficulties)

    if level==274380:
        chest="TRUE"
        num_max=None
        num_min=None
    else:
        chest="false"
        num_max=level_difficulties[level]                   #字典[键]→值
        num_min=1

    game_result=guess_game(num_min,num_max,chest)                  #调用函数，游戏开始
    data.append(game_result)

    history_print(data)

    answer=input(start)

stats=game_stats(data)

print("感谢游玩！")
print(f"你总共猜了{stats["局数"]}局,你总共猜了{stats["总次数"]}次！平均每局猜{stats["平均"]}次！")