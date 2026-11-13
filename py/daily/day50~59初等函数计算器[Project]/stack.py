#=========分栈器=========#
"""
分栈器\n
负责将输入的表达式分栈并调用计算包进行计算\n
"""
#=========分栈器=========#
try:
    import pack
    pack.copyer(r"C:\Users\cutes\Desktop\copy\初等函数计算器","stack.txt",(6,12))
except ModuleNotFoundError:pass
#调用打包复制工具(可删,以下为正文)
#=========分栈器=========#
import calculation as c;import transformer as t
class EmptyError(Exception):pass
#初始化声明
def stack(put):
    """该函数用于将输入栈进行分栈计算喵，并返回最终结果喵"""
    num=[];ope=[]#双栈
    constent={"e":c.e(),"π":c.pi(),"pi":c.pi(),"inf":c.inf}#常数
    operator_tuple=("+","-","*","/","//","%","@","^","!","!!")#算符组
    function_tuple=(
                    "sin","cos","tan","cot","sec","csc",#三角函数
                    "arcsin","asin","arccos","acos","arctan","atan",#反三角函数
                    "ln","lg","log","~",#对数函数
                    "sh","sinh","ch","cosh","th","tanh",#双曲函数
                    "arsh","ash","arsinh","asinh","arch","ach","arcosh","acosh","arth","ath","artanh","atanh"#反双曲函数
                    )#函数组
    brackt_pair={")":"(",">":"<"}#括号对
    operator_weight={"+":1,"-":1,"*":2,"/":2,"//":2,"%":2,"@":3,"^":4,"(":0,"<":0}#算符权重
    #初始化声明
    if not put:raise EmptyError
    #非法输入检测
    for i,p in enumerate(put):
    #输入栈循环
        if p in operator_tuple:
        #算符入栈
            if p not in ("!","!!"):
            #基础算符入栈
                if p in ("+","-") and (i==0 or put[i-1] in operator_weight or put[i-1] in function_tuple):
                #一阶算符合并
                    num.append(1 if p=="+" else -1);ope.append("@")
                
                else:
                #高阶算符入栈
                    while ope and (
                                operator_weight[p]<operator_weight[ope[-1]] if p=="^" 
                                else operator_weight[p]<=operator_weight[ope[-1]]
                                ):
                    #栈权判断
                        y=num.pop();x=num.pop();o=ope.pop()
                        num.append(c.basic(x,o,y))
                    ope.append(p)

            else:num.append(c.gamma(num.pop(),"!") if p=="!" else c.gamma(num.pop(),"!!"))
            #伽马函数入栈
        elif p in brackt_pair.values():ope.append(p)
        #括号及绝对值入栈
        elif p in brackt_pair:
        #括号及绝对值出栈
            while ope[-1]!=brackt_pair[p]:
            #出栈循环
                y=num.pop();x=num.pop();o=ope.pop()
                num.append(c.basic(x,o,y))
            ope.pop()

            if p==">":num.append(c.absorlute(num.pop()))
            #绝对值判断
            if i<len(put)-1 and put[i+1] in (*function_tuple,"(","<",*constent,"i"):
            #隐乘法判断
                while ope and operator_weight["*"]<=operator_weight[ope[-1]]:
                #栈权判断
                    y=num.pop();x=num.pop();o=ope.pop()
                    num.append(c.basic(x,o,y))
                ope.append("*")

        else:
        #数字与角度入栈
            if p in ("e","pi","π","i"):num.append(constent[p] if p!="i" else (0,10**t.P))
            #e,π入栈,i以(0,10**P)元组形式分部入栈
            elif p=="°":num.append(c.basic(c.basic(num.pop(),"/","180"),"*",constent["π"]))
            #角度转弧度入栈
            else:num.append(p)
            #数字入栈
            if i<len(put)-1 and put[i+1] in (*function_tuple,"(","<",*constent,"i"):
            #隐乘法判断
                while ope and operator_weight["*"]<=operator_weight[ope[-1]]:
                #栈权判断
                    y=num.pop();x=num.pop();o=ope.pop()
                    num.append(c.basic(x,o,y))
                ope.append("*")

    while ope:
    #清栈
        y=num.pop();x=num.pop();o=ope.pop()
        num.append(c.basic(x,o,y))

    return num[0]#答案