score=int(input("请输入成绩："))                #类型转换

if score>100:
    print("成绩无效")
elif score>=90:
    print("优秀")
elif score>=80:
    print("良好")
elif score>=60:
    print("及格")
elif score>=0:
    print("不及格")
elif score>=-1:
    print("试卷丢失")
else:
    print("作弊")               #判断