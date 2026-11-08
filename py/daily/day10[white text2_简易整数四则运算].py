#随笔自测：整数四则运算计算程序




##########################################################################

def int_text():
    while True:
        try:
            int_num=int(input("请输入整数:"))
            return int_num
        except ValueError:
            print("这不是一个整数")

##########################################################################

def operator_text(operator_list):
    operator=input("请输入四则运算符或=:")

    while operator not in operator_list:
        print("这不是一个四则运算符")
        operator=input("请输入四则运算符或=:")

    return operator

##########################################################################

def calculation(operator,num_a,num_b):
    if operator=="+":
        result=num_a+num_b
    elif operator=="-":
        result=num_a-num_b
    elif operator=="*":
        result=num_a*num_b
    elif operator=="/":                 #选择elif而非else是为了方便以后加入其他可能的运算
        while num_b==0:
            print("除数不能为0，请重新输入")
            num_b=int_text()
        result=num_a/num_b
    return result

##########################################################################

operator_list=["+","-","*","/","="]                 #初始化变量

num_a=int_text()
operator=operator_text(operator_list)                   #初始化函数

while operator!="=":
    num_b=int_text()
    num_a=calculation(operator,num_a,num_b)
    operator=operator_text(operator_list)
    
print("最终结果",num_a)



#用时1h