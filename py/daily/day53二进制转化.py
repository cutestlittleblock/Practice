while True:
    try:
        p=int(input("输入一个整数喵，其他输入退出喵:"));i=""
        while p:
            m=p%2;p//=2
            if m:i="1"+i
            else:i="0"+i
        print(i)
    except ValueError:break