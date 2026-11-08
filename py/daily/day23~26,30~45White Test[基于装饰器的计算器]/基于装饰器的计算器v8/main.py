try:
    import pack
    pack.copyer(r"C:\Users\cutes\Desktop\copy\计算器v8","main.txt",0)
except ModuleNotFoundError:pass
#调用打包复制工具(可删,以下为正文)
#=========fileblock=========#
import time,re,json,functools,os

#——————classblock——————#

class Main():

    #---defblock---#

    def __init__(self):
        self.token=re.compile(
                              r"""
                              \d+\.?\d*|e|pi|π|i|°|#数字和角度
                              //|[+\-*/^=%\(\)\[\]\{\}]|<|>|#基础算符
                              !!|!|#模块算符(阶乘)
                              sh|sinh|ch|cosh|th|tanh|#模块算符(双曲函数)
                              ash|asinh|ach|acosh|ath|atanh|#模块算符(反双曲函数)
                              ln|lg|log|~|#模块算符(对数函数)
                              sin|cos|tan|cot|sec|csc|#模块算符(三角函数)
                              arcsin|asin|arccos|acos|arctan|atan#模块算符(反三角函数)
                              """,re.VERBOSE
                              )#分词器
        self.e=constant("e");self.pi=constant("pi");self.inf=1e301#e,π,∞初始化定义
        self.basic_operator_set={"+","-","*","/","//","%","&","^"}#基础算符集
        self.trigono_set={
                          "sin","cos","tan","cot","sec","csc",
                          "arcsin","asin","arccos","acos","arctan","atan"
                          }#三角函数集
        self.hyperbolic_set={
                             "sh","sinh","ch","cosh","th","tanh",
                             "ash","asinh","ach","acosh","ath","atanh"
                             }#双曲函数集
        self.modular_operator_set={"!","!!",*self.hyperbolic_set,"ln","lg","log","~",*self.trigono_set}#模块算符组
        self.behpara_operator_set={*self.hyperbolic_set,"ln","lg","log","~",*self.trigono_set}#后参算符集
        self.operator_weight_dict={
                                   "+":1,"-":1,"*":2,"/":2,"//":2,"%":2,"&":3,"^":4,
                                   "(":0,"[":0,"{":0,"<":0
                                   }#算符权重
        self.brackets_dict={")":"(","]":"[","}":"{",">":"<"}#括号对
        self.implicit_times_set={"e","pi","π",*self.brackets_dict.values(),*self.behpara_operator_set}-{"~"}#隐乘集
        self.error="别乱输喵omo"#错误信息
        self.put_stack=[]#输入栈
        self.num_stack=[]#数字栈
        self.operator_stack=[]#算符栈
        self.precision=range(1,17)#精度范围
        self.answer=None#答案
        self.t=0#运行时间
        self.calculation=self.timer(self.calculation)#装饰化计时
        self.data=loader()#读档

    #---defblock---#

    def main_run(self):
        #主运行流程方法
        switch=True;serial=1
        self.data.append([])
        while switch:
            answer=None;self.t=0;self.precision=17
            question=input("我需要算什么喵：")
            self.put_stack=self.token.findall(question)
            try:
                if not self.calculation():continue
                while self.precision not in range(1,17):
                    try:
                        self.precision=int(input("你需要小数点后几位喵(最高只有16位喵)："))
                    except (TypeError,ValueError):
                        print(self.error)

                if isinstance(self.answer,complex):
                    if abs(float(f"{self.answer.imag:.{self.precision}f}"))!=1:
                        answer=(f"{self.answer.real:.{self.precision}f}{self.answer.imag:+.{self.precision}f}i"
                                if abs(self.answer.real)>1e-12 else f"{self.answer.imag:.{self.precision}f}i")
                    else:
                        answer=((f"{self.answer.real:.{self.precision}f}+i"if abs(self.answer.real)>1e-12 else "i")
                                if self.answer.imag>0 else 
                                (f"{self.answer.real:.{self.precision}f}-i"if abs(self.answer.real)>1e-12 else "-i"))

                else:answer=f"{self.answer:.{self.precision}f}"

                print(f"答案是{answer}喵,计算用时约{self.t*1000:.4f}ms喵")
            except ZeroDivisionError:
                print("分母不能为0喵omo");answer=None
            except OverflowError:
                print("太大了喵~受不了了喵~算不出来喵~");answer="太大了喵，你就当是∞"

            self.data[-1].append({"问题":question,"答案":answer,"序号":serial});serial+=1
            saver(self.data)

            switch=input("还要不要算喵，输入H查看历史记录喵，其他任意继续喵，直接回车歇逼了喵：")
            while switch.upper()=="H":
                while True:
                    try:
                        s=int(input("你想看上几次使用记录喵（给自然数喵，看这次就输0喵）："))+1
                        if s<1 or s>len(self.data):
                            print("根本没有这种使用记录喵omo给我重输喵omo")
                            continue
                        break
                    except (TypeError,ValueError):
                        print("我服了你听不懂喵话喵omo给我重输喵omo")
                if not history(self.data[-s]):self.data[-s]=[];saver(self.data)

                switch=input("还要不要算喵，输入H查看历史记录喵，其他任意继续喵，直接回车歇逼了喵：")
        print("感谢使用喵~下班下班~")


    #---defblock---#

    def timer(self,func):
        #计时器
        def wrapper(*args,**kwargs):
            t0=time.perf_counter()
            result=func(*args,**kwargs)
            self.t+=time.perf_counter()-t0
            return result
        return wrapper

    #---defblock---#

    def stack_poper(self):
        #出栈处理器
        y=self.num_stack.pop();x=self.num_stack.pop();o=self.operator_stack.pop()
        if o in self.basic_operator_set:return basic_math(x,y,o)

    #---defblock---#

    def pop_judger(self,operator,top):
        #栈权判断器
        if operator=="^":return self.operator_weight_dict[operator]<self.operator_weight_dict[top]
        return self.operator_weight_dict[operator]<=self.operator_weight_dict[top]

    #---defblock---#

    def behpara_poper(self):
        #后参处理器
        x=self.num_stack.pop();o=self.operator_stack.pop()
        if o in self.trigono_set:
        #三角函数计算
            x=(trigono(x,o) if o in ("sin","cos","tan","cot","sec","csc") else antrigono(x,o))

        elif o in self.hyperbolic_set:
        #双曲函数计算
            x=(hyperbolic(x,o) if o in ("sh","sinh","ch","cosh","th","tanh") else anhyperbolic(x,o))

        elif o in ("ln","lg","log","~"):
        #对数函数计算
            if o in ("ln","lg"):x=logarithm(x,o)
            #自然常用对数运算
            elif o=="~":
            #底真数合并运算
                y=self.num_stack.pop()#x为真数,y为底数
                lnx=logarithm(x,"ln");lny=logarithm(y,"ln")
                x=basic_math(lnx,lny,"/")

            else:pass#log符号跳过,仅用于判断隐乘

        return x

    #---defblock---#

    def calculation(self):
        #计算流程方法
        self.num_stack=[];self.operator_stack=[]
        #双栈初始化
        try:
            if len(self.put_stack)==0:print("这根本没东西可算喵omo");return False
            elif self.put_stack[-1]=="=":self.put_stack.pop()
            #初始化判断
            for i in range(len(self.put_stack)): 
            #输入栈循环
                if self.put_stack[i] is None:continue
                #空值判断
                elif self.put_stack[i] in self.basic_operator_set:
                #基础算符入栈判断
                    if self.put_stack[i] in ("+","-"):
                    #一阶算符的入栈判断与合并
                        if i==0 or self.put_stack[i-1] in self.basic_operator_set or self.put_stack[i-1] in self.brackets_dict.values():
                        #多算符与顶算符合并
                            j=1
                            while self.put_stack[i+j] in ("+","-"):
                                if self.put_stack[i+j]=="+":self.put_stack[i+j]=None
                                else:self.put_stack[i]=("+" if self.put_stack[i]=="-" else "-");self.put_stack[i+j]=None
                                j+=1

                            self.num_stack.append(1 if self.put_stack[i]=="+" else -1);self.operator_stack.append("&")

                        else:
                        #单算符入栈
                            while self.operator_stack and self.pop_judger(operator=self.put_stack[i],top=self.operator_stack[-1]):
                                self.num_stack.append(self.stack_poper(o=self.operator_stack.pop()))

                            self.operator_stack.append(self.put_stack[i])

                    else:
                    #高阶算符入栈判断
                        while self.operator_stack and self.pop_judger(operator=self.put_stack[i],top=self.operator_stack[-1]):
                            self.num_stack.append(self.stack_poper())

                        self.operator_stack.append(self.put_stack[i])

                elif self.put_stack[i] in self.modular_operator_set:
                #模块算符入栈
                    if self.put_stack[i] in ("!","!!"):
                    #(双)阶乘运算
                        self.num_stack.append(factorial(self.num_stack.pop()) if self.put_stack[i]=="!" else defactor(self.num_stack.pop()))
                        if self.put_stack is not None and i<len(self.put_stack)-1 and self.put_stack[i+1] in self.implicit_times_set:
                        #隐乘法判断
                            while self.operator_stack and self.pop_judger(operator="*",top=self.operator_stack[-1]):
                                self.num_stack.append(self.stack_poper())

                            self.operator_stack.append("*")

                    elif self.put_stack[i] in self.behpara_operator_set:self.operator_stack.append(self.put_stack[i])
                    #后参算符入栈(由于其栈位在数字之前,故命名后参算符,在数字入栈/括号收官类计算)

                elif self.put_stack[i] in self.brackets_dict.values():self.operator_stack.append(self.put_stack[i])
                #括号及绝对值入栈判断
                elif self.put_stack[i] in self.brackets_dict:
                #反括号及绝对值入栈,括号及绝对值收官
                    while self.operator_stack[-1]!=self.brackets_dict[self.put_stack[i]]:
                        self.num_stack.append(self.stack_poper())

                    self.operator_stack.pop()
                    if self.put_stack[i]==">":self.num_stack.append(absolute(self.num_stack.pop()))
                    #绝对值判断
                    if i<len(self.put_stack)-1 and self.put_stack[i+1]=="°":pass
                    #角度跳过,弧度化后进行后续计算
                    if self.operator_stack and self.operator_stack[-1] in self.behpara_operator_set:
                    #后参判断
                        self.num_stack.append(self.behpara_poper())

                    if self.put_stack is not None and i<len(self.put_stack)-1 and self.put_stack[i+1] in self.implicit_times_set:
                    #隐乘法判断
                        while self.operator_stack and self.pop_judger(operator="*",top=self.operator_stack[-1]):
                            self.num_stack.append(self.stack_poper())

                        self.operator_stack.append("*")

                else:
                #角度及数字入栈
                    if self.put_stack[i]=="°":
                    #角度转弧度入栈
                        if self.put_stack[i-1] in self.brackets_dict or float(self.put_stack[i-1]) or float(self.put_stack[i-1])==0:
                            self.num_stack.append(basic_math(basic_math(self.num_stack.pop(),180,"/"),self.pi,"*"))

                        else:raise ModularError

                    else:
                    #数字入栈
                            if self.put_stack[i] in ("e","pi","π","i"):
                            #常用无理数e,π及虚数单位i入栈
                                if self.put_stack[i]=="e":self.num_stack.append(self.e)
                                elif self.put_stack[i] in ("pi","π"):self.num_stack.append(self.pi)
                                else:self.num_stack.append(1j)

                            else:self.num_stack.append(float(self.put_stack[i]))
                            #有理数入栈

                    if self.operator_stack and self.operator_stack[-1] in self.behpara_operator_set:
                    #后参判断
                        self.num_stack.append(self.behpara_poper())

                    if i<len(self.put_stack)-1 and self.put_stack[i+1] in self.implicit_times_set:
                    #隐乘法判断
                        while self.operator_stack and self.pop_judger(operator="*",top=self.operator_stack[-1]):
                            self.num_stack.append(self.stack_poper())

                        self.operator_stack.append("*")

        except (IndexError,ValueError,TypeError,ModularError):print(self.error);return False

        try:
        #答案收官
            while self.operator_stack:
                if self.operator_stack[-1] in self.brackets_dict.values():print(self.error);return False
                self.num_stack.append(self.stack_poper())
        except IndexError:print(self.error);return False
        if len(self.num_stack)!=1:print(self.error);return False
        self.answer=self.num_stack[0]

        return True

#——————classblock——————#

class ModularError(Exception):pass

#——————classblock———————#

#---defblock---#

def constant(C):
    #e,π常数初始化
    n=0;R=1;e=0
    while absolute(R)>basic_math(10,-17,"^"):
    #e初始化
        R=basic_math(1,factorial(n),"/")
        e+=R;n+=1
    
    n=0;R=basic_math(10,32,"^");pi=0
    while absolute(R)>1:
    #π初始化
        R0=basic_math(basic_math(2,n,"*"),1,"+")
        R1=basic_math(
                      basic_math(basic_math(16,basic_math(10,32,"^"),"*"),basic_math(R0,basic_math(5,R0,"^"),"*"),"//"[0:2]),
                      basic_math(-1,n,"^"),
                      "*"
                      )
        R2=basic_math(
                      basic_math(basic_math(4,basic_math(10,32,"^"),"*"),basic_math(R0,basic_math(239,R0,"^"),"*"),"//"[0:2]),
                      basic_math(-1,n,"^"),
                      "*"
                      )
        R=basic_math(R1,R2,"-")
        pi+=R;n+=1#马青公式:pi*10^17=sum(16(-1)^n/(2n+1)5^(2n+1)-4(-1)^n/(2n+1)239^(2n+1))
    pi=float(str(pi)[0]+"."+str(pi)[1:18])#整数转字符浮点化

    return (e if C=="e" else pi)

#---defblock---#

def basic_math(x,y,o):
    #基础计算
    basic_dict={
                "+":lambda:x+y,"-":lambda:x-y,
                "*":lambda:x*y,"/":lambda:x/y,"//":lambda:x//y,"%":lambda:x%y,
                "&":lambda:x*y,
                "^":lambda:x**y
                }
    return basic_dict[o]()

#---defblock---#

def absolute(x):
    #绝对值计算
    if isinstance(x,complex):return(basic_math(basic_math(basic_math(x.real,2,"^"),basic_math(x.imag,2,"^"),"+"),0.5,"^"))
    else:return(x if x>=0 else -x)

#---defblock---#

def modular_math(limit):
    #模块化求值
    def decorator(func):
        #装饰器
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            #打包器
            modular_name=func.__name__;args=list(args);x=args[0]
            if absolute(x)>=limit or x!=x:raise OverflowError if absolute(x)>=limit else ModularError
            #初始数据合法性判断
            if modular_name in ("factorial","defactor"):
            #阶乘初始化
                if x<0 or x%1!=0 or x>10**5:raise OverflowError
                elif x==0:return 1

            elif modular_name=="anhyperbolic":
            #反双曲初始化
                a=args[1]
                if (a in ("ach","acosh") and x<1) or (a in ("ath","atanh") and absolute(x)>=1):raise ModularError

            elif modular_name=="logarithm":
            #对数初始化
                if x<=0:raise ModularError
                k=0
                while absolute(x)>2:
                    x/=2;k+=1

                args.append(k);args[0]=x

            elif modular_name in ("trigono","antrigono"):
            #三角函数初始化
                if modular_name=="trigono":
                #正三角函数初始化
                    x=args[0].real if isinstance(args[0],complex) else args[0]
                    #复数域扩展
                    x-=basic_math(round(x/(2*main.pi)),2*main.pi,"*")

                    args[0]=x+1j*args[0].imag if isinstance(args[0],complex) else x

                else:
                #反三角函数初始化
                    a=args[1]
                    if a in ("asin","arcsin","acos","arccos"):
                    #反正余弦初始化
                        if absolute(x)>1:raise ModularError
                        elif absolute(x)==1 and not isinstance(x,complex):
                            if a in ("asin","arcsin"):return(main.pi/2 if x==1 else -main.pi/2)
                            else:return(0 if x==1 else main.pi)

                        else:
                        #反正余弦转化为反正切问题,变参x>>x/(1-x^2)^0.5
                            x=basic_math(x,basic_math(basic_math(1,basic_math(x,2,"^"),"-"),0.5,"^"),"/")#x=x/(1-x^2)^0.5
                    k=0
                    while absolute(x.real)>0.2 or absolute(x.imag)>0.2:
                    #反正切参数缩放:atanx=2antan(x/(1+(1+x^2)^0.5),变参x>>x/1+(1+x^2)^0.5
                        x=basic_math(x,basic_math(1,basic_math(basic_math(1,basic_math(x,2,"^"),"+"),0.5,"^"),"+"),"/")
                        #x=x/1+(1+x^2)^0.5
                        k+=1

                    args.append(k);args[0]=x

            module=func(*args,**kwargs)
            if absolute(module)>=limit or module!=module:raise OverflowError if absolute(module)>=limit else ModularError
            #结果数据合法性判断
            return module
        return wrapper
    return decorator

#---defblock---#

@modular_math(1e301)
def factorial(*args):
    #阶乘计算
    x=args[0];y=1
    for n in range(int(x),1,-1):y*=n
    return y

#---defblock---#

@modular_math(1e301)
def defactor(*args):
    #双阶乘计算
    x=args[0];y=1
    for n in range(int(x),1,-2):y*=n
    return y

#---defblock---#

@modular_math(1e301)
def hyperbolic(*args):
    #双曲函数计算
    x=args[0];h=args[1]
    shx=basic_math(basic_math(basic_math(main.e,x,"^"),basic_math(main.e,-x,"^"),"-"),2,"/")
    chx=basic_math(basic_math(basic_math(main.e,x,"^"),basic_math(main.e,-x,"^"),"+"),2,"/")
    hyperbolic_dict={
                     "sh":lambda:shx,"sinh":lambda:shx,"ch":lambda:chx,"cosh":lambda:chx,
                     "th":lambda:shx/chx,"tanh":lambda:shx/chx
                     }#双曲推导式

    return hyperbolic_dict[h]()

#---defblock---#

@modular_math(1e301)
def anhyperbolic(*args):
    #反双曲函数计算
    x=args[0];a=args[1];ashx=None;achx=None;athx=None

    if a in ("ath","atanh"):
    #反双曲正切计算
        athx=x;R=1;n=1
        while absolute(R)>basic_math(10,-17,"^"):
            R=basic_math(
                        basic_math(x,basic_math(basic_math(2,n,"*"),1,"+"),"^"),
                        basic_math(basic_math(2,n,"*"),1,"+"),"/"
                        )#R=x^(2n+1)/(2n+1)
            athx+=R;n+=1

    else:
    #反双曲正余弦计算
        ashx=logarithm(basic_math(x,basic_math(basic_math(basic_math(x,2,"^"),1,"+"),0.5,"^"),"+"),"ln")#ashx=ln(x+(x^2+1)^0.5)
        achx=logarithm(basic_math(x,basic_math(basic_math(basic_math(x,2,"^"),1,"-"),0.5,"^"),"+"),"ln")#achx=ln(x+(x^2-1)^0.5)

    anhyperbolic_dict={"ash":ashx,"asinh":ashx,"ach":achx,"acosh":achx,"ath":athx,"atanh":athx}#反双曲推导式

    return anhyperbolic_dict[a]

#---defblock---#

@modular_math(1e301)
def logarithm(*args):
    #对数计算
    x=args[0];l=args[1];k=args[2]
    ln2=basic_math(anhyperbolic(1/3,"ath"),2,"*");ln10=basic_math(anhyperbolic(9/11,"ath"),2,"*")
    lnx=basic_math(
                   anhyperbolic(basic_math(
                                           basic_math(x,1,"-"),
                                           basic_math(x,1,"+"),
                                           "/"
                                           ),"ath"),
                   2,"*"
                   )#lnx=2arth((x-1)/(x+1))
    lnx+=basic_math(k,ln2,"*")#lnx=kln2+lnx(利用ln2=2arth(1/3)进行参数缩放)

    logarithm_dict={"ln":lambda:lnx,"lg":lambda:lnx/ln10}

    return logarithm_dict[l]()

#---defblock---#

@modular_math(1e15)
def trigono(*args):
    #三角函数计算
    x=args[0];t=args[1]
    sinx=x;cosx=1
    R=1;n=1
    while absolute(R)>basic_math(10,-17,"^"):
    #正弦计算
        R=basic_math(
                     basic_math(-1,n,"^"),
                     basic_math(
                                basic_math(x,basic_math(basic_math(2,n,"*"),1,"+"),"^"),
                                factorial(basic_math(basic_math(2,n,"*"),1,"+")),"/"
                                ),"*"
                     )#R=(-1)^n*x^(2n+1)/(2n+1)!
        sinx+=R;n+=1
    if not isinstance(sinx,complex):sinx=float(f"{sinx:.16f}")

    R=1;n=1
    while absolute(R)>basic_math(10,-17,"^"):
    #余弦计算
        R=basic_math(
                     basic_math(-1,n,"^"),
                     basic_math(
                                basic_math(x,basic_math(2,n,"*"),"^"),
                                factorial(basic_math(2,n,"*")),"/"
                                ),"*"
                     )#R=(-1)^n*x^(2n)/(2n)!
        cosx+=R;n+=1
    if not isinstance(cosx,complex):cosx=float(f"{cosx:.16f}")

    trigono_dict={
                  "sin":lambda:sinx,"cos":lambda:cosx,"tan":lambda:sinx/cosx,
                  "cot":lambda:cosx/sinx,"sec":lambda:1/cosx,"csc":lambda:1/sinx
                  }#三角推导式

    try:
        return trigono_dict[t]()
    except ZeroDivisionError:print("这个三角函数不存在喵，趋于无穷了喵");return main.inf

#---defblock---#

@modular_math(1e301)
def antrigono(*args):
    #反三角函数计算
    x=args[0];a=args[1];k=args[2]
    antri=x;R=1;n=1
    while absolute(R)>basic_math(10,-17,"^"):
    #反正切计算(反正余弦转化为正切:asinx=atan(x/(1-x^2)^0.5))
        R=basic_math(
                     basic_math(-1,n,"^"),
                     basic_math(
                                basic_math(x,basic_math(basic_math(2,n,"*"),1,"+"),"^"),
                                basic_math(basic_math(2,n,"*"),1,"+"),"/"
                                )
                     ,"*"
                     )#R=(-1)^n*x^(2n+1)/(2n+1)
        antri+=R;n+=1
    
    antri*=basic_math(2,k,"^")
    antrigono_dict={
                    "arctan":lambda:antri,"atan":lambda:antri,"arcsin":lambda:antri,"asin":lambda:antri,
                    "arccos":lambda:basic_math(main.pi/2,antri,"-"),"acos":lambda:basic_math(main.pi/2,antri,"-")
                    }#反三角推导式

    return antrigono_dict[a]()

#---defblock---#

def saver(data):
    os.makedirs(os.path.join(os.path.dirname(__file__),"saves"),exist_ok=True)
    p=os.path.join(os.path.join(os.path.dirname(__file__),"saves"),"save.json")
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#---defblock---#

def loader():
    p=os.path.join(os.path.join(os.path.dirname(__file__),"saves"),"save.json")
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)            
    except FileNotFoundError:return []        
    except json.JSONDecodeError:print("历史记录坏掉了喵~下班修喵~");return []
    if not isinstance(data,list):print("历史记录坏掉了喵~下班修喵~");return []
    return data

#---defblock---#

def history(data):
    print("历史记录如下喵~")
    if not data:print("这次的历史记录为空喵，应该是坏了喵");return True
    else:
        try:
            for record in data:
                print(f"你在第{record['序号']}轮\n问了：{record['问题']}喵\n答案是：{record['答案']}喵~\n")
            return True
        except (TypeError,KeyError):
            print("这次的记录被搞坏了喵，我给你清空了喵");return False
        
#---defblock---#

main=Main()
main.main_run()