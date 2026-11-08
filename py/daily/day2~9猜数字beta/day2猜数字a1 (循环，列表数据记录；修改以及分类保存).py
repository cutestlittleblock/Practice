answer=None
num=0             
guesses_more=[]
guesses_less=[]                 #变量

while answer!=7:
    answer=int(input("请猜数字："))                 #循环

    if answer<7:                #判断
        print("猜小了！")
        guesses_less.append(answer)         #记录1    
        num=num+1               #计数1
    elif answer>7:
        print("猜大了！")
        guesses_more.append(answer)                 #记录2
        num=num+1               #计数2
    
print(f"猜对了！恭喜你！你猜错{num}次！")  
print(f"你猜大的数字有{guesses_more}")
print(f"你猜小的数字有{guesses_less}")                  #输出