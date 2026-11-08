def play_game():
    guesses=[]
    num=None
    while num!=7:
        num=int(input("请猜数字："))
        guesses.append(num)
        if num<7:
            print("猜小了！")
        elif num>7:
            print("猜大了！")
    print("恭喜你才对了！")
    return guesses

answer=input("是否开始游戏？是为y否为n:")

while answer=="y":
    result=play_game()
    print(f"你猜错的数字有{result}！")
    answer=input("是否开始游戏？是为y否为n:")

print("感谢游玩！")