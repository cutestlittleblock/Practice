def play_game():
    guesses=[]
    num=None
    while num!=7:
        num=int(input("请猜数字："))
        guesses.append(num)
        if num!=7:
            print("猜错了！")

    print("恭喜你猜对了！")
    return guesses

result=play_game()
print(f"你猜的数字有{result}")
