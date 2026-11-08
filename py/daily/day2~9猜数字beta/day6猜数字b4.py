import random
def play_game():
    guesses=[]
    num=None
    key=random.randint(1,10)
    while num!=key:
        num=int(input("请猜数字："))
        guesses.append(num)
        if num<key:
            print("猜小了！")
        elif num>key:
            print("猜大了！")
    print("恭喜你猜对了！")
    return [key,guesses,]

answer=input("是否开始游戏？是为y,输入任意字符为否:")
data=[]                 #data=[[key_1,guesses_1],...,[key_n,guesses_n]]
guesses_num=0

while answer=="y":
    result=play_game()
    data.append(result)
    for n,history in enumerate(data):                   #enumerate=编号（从0开始），元素#history[0]=key,history[1]=guesses
        print(f"第{n+1}局历史记录：{history}")
        print(f"该局猜过的数字有{history[1]}，该局答案为{history[0]}！")
    guesses_num=guesses_num+len(result[1])

    answer=input("是否开始游戏？是为y，输入任意字符为否:")

print("感谢游玩！")
print(f"你总共猜了{len(data)}局")
print(f"你总共猜了{guesses_num}次！")
if len(data)>0:
    print(f"平均每局猜{guesses_num/len(data)}次！")