#=========实验0=========#
print("#=========实验0=========#")
a=[1,2,3]
b=a
print(id(a),id(b))                  #数据id不变
#=========实验1=========#
print("#=========实验1=========#")
s="str"
print(id(s))
s="str_"
print(s,type(s),id(s))                    #字符串不可变，type查类型，名牌转贴数据变id变
#=========实验2=========#
print("#=========实验2=========#")
list_1=[1,5,9]
list_1[0]=2
print(list_1)                   #列表可变
#=========实验3=========#
print("#=========实验3=========#")
tuple_1=(1,5,9)
#tuple_1[0]=2
#tuple_1.append(13)
print(tuple_1,tuple_1[1],tuple_1[-1],9 in tuple_1,len(tuple_1),sum(tuple_1))                    #元组不变,其余类同列表
#=========实验4=========#
print("#=========实验4=========#")
a=[1,2,3];b=a;b.append(4);print(a);print(b);c=a.copy();c.append(4);print(c)
x=1;y=x;y=y+1;print(x,y)                    #int不变，不用copy
#=========实验5=========#
print("#=========实验5=========#")
list_2=[1,2,3,4];list_2.append(5)
#list_2.append(5,6)                 #同时append2个元素会报错，那么怎么同时添加多个元素
print(list_2[-1])                   #负索引，[-x]表示倒数第x个列表的元素，若x>列表总元素数会报错
#=========实验6=========#
print("#=========实验6=========#")
empty_dict={}
empty_set=set();empty_set.add(1)
print(empty_dict,empty_set,type(empty_set),type(empty_dict))                    #空字典和集合区别
set_1={1,2,3,2,3,1,3,2,1,1}
set_1.add(0)
print(set_1)                    #集合无序且不重复且可改,用add添加
#=========实验7=========#
print("#=========实验7=========#")
#i=int(42/10)
f=float(42/10);i=int(42//10);i_m=int(42%10);print(f,i,i_m)                 #int为整数，浮点可小数
print(int(-42/10));print(int("  5  "));print(-42//10)                #int向0取整，//整除向负无穷取整
print(2**3)                   #乘方
#=========实验8=========#
print("#=========实验8=========#")
list_3=[0,1,2,3,4,5]
print(list_3[1:4],list_3[:2],list_3[2:],list_3[:2]+list_3[2:],list_3[::2],list_3[::-2])                  #[开始索引:结束索引:步长],步长为负则从尾部开取（结束索引含头不含尾）
#list_3[100]                    #索引越界报错
print(list_3[100:],list_3[:100],list_3[::6],list_3[::-6])                  #切片越界会截取到首尾部，步长越界取第一个切片元素
list_4=list_3[::]
list_4.append(6);print(list_4,list_3)                   #==list_3.copy()
#=========实验9=========#
print("#=========实验9=========#")
s_1="  s  xxx "
print(s_1.strip(),s_1.strip("x"),s_1.strip(" x"),s_1.split())                   #strip从两头开剥，直到遇到非方法内参数停止
s_2="bx,lx,ox,cx,k"
print(s_2.split(","),s_2.split("x,"))                   #split("x")将x视作字符串的隔板，去掉隔板进列表
s_l=["b","l","o","c","k"]
#print("".join([1,2,3]))                  #join只收字符串
print("".join(s_l),"x".join(s_l))                   #"x".join(list)x作用类同split
block_m="bxxloxxxccckxxk"
print(block_m.replace("x","",1),block_m.replace("x",""))                    #既然replace默认全部，replace方法中第三个参数为替换的个数限制
block=""
for ch in block_m:
    if ch not in block:
        block+=ch                   #累加器去重
block=block.replace("x","",1)
print(block)
block_=("".join(dict.fromkeys(block_m))).replace("x","",1);print(block_)                    #dict.fromkeys型去重器(利用字典键不重合特性去重)
#=========实验10=========#
print("#=========实验10=========#")
print(f"{2.676:.2f}{2.675:.2f}")
dict_1={1:"a",2:"b",3:"c"}
num_1=round(3/7,2)
for k,v in dict_1.items():
    print(k,v,f"{k}:{v}")                   #.items()键值对应取出
#print(dict_1[4])                   #KeyError: 4
print(num_1,type(num_1),dict_1.get(3,"d"),dict_1.get(4,"d"),dict_1.get(3))
#get(键:值)可以赋予不存在的键一个临时的值，但不能用临时值覆盖原有值，同时也具有[键]的功能
dict_add={}
while True:
    dict_add["add"]=dict_add.get("add",1)+1
    print(dict_add)
    if dict_add["add"]>3:
        break                   #dict.get()型累加器
print(dict_add)
#=========实验11=========#
print("#=========实验11=========#")
list_og=[1,2,3]
list_co=[1,2,3]
list_og_1=list_og
list_os=list_og[:]
print(list_og==list_co,list_og is list_co,list_og is list_og_1,list_og==list_os,list_og is list_os)
#==比较对象内容是否一致，is比较对象是否一致，由于缓存优化（python的int不会溢出）
#仅-5~256范围的数每次被定义的id一定一致，故定义(-∞，-5)U(256,+∞)上的数不能用is比较
#故数字，字符串比较一律用==
#=========实验12=========#
print("#=========实验12=========#")
def none():pass
def func():f="x";return f
print(none(),type(none),type(None),type(none()),type(func()),none() is None)                   #None是一个对象,全程序只有一份，故用is
#另外，定义函数后，函数名的类型为函数，而函数名()为调用值(返回值)的属性
print(None==False,None==0,bool(None))
#None为空
for TorF in [0,1,-1,"","0",[],[0],{},{"k":1},None,0.0,False,True,()]:
    print(repr(TorF),bool(TorF))                    #预测与结果一致，[0],"0",-1都为真值
list_TF=[]
while not list_TF:
    print("NOT")
    list_TF.append(1)
print(list_TF,"BOOLTRUE")                   #not也可以用于判断真假值
#bool()为真假值(是否为空值)转换器，目前我只知道None(代码空值)，False(逻辑空（假）值)，0 or 0.0(数学空值)，{} or [] or ()(结构空值)为空，而[0],"0"在代码上均有意义，故为真值
#=========实验13=========#
print("#=========实验13=========#")
def func_1(a):
    print("1alright",a)
    return ret
    #return ret()                   #若子函数下没有返回非空值则会报错
def func_2(b):
    print("2alright",b)
    return ret
def ret():
    print("returned")
dict_func={1:func_1,2:func_2,3:func_1(1),4:func_2(2)}
dict_func[1](1),dict_func[2](2),dict_func[3](),dict_func[4]()
#函数名也属于“名牌”，也可以通过函数返回函数套娃
#=========实验14=========#
print("#=========实验14=========#")
dict_up={1:"a",2:"b",3:"c"}
dict_down={v:k for k,v in dict_up.items()};print(dict_down)
#利用字典推导式颠倒字典，倒置时键也不能重复
#=========实验15=========#
print("#=========实验15=========#")                 #祖先代打实验
class Father(Exception):pass
class Son(Father):
    def __init__(self,*args):
        super().__init__(*args)
son=Son("son");empty_son=Son();print(son,empty_son,Son(1,2,3))                 #son打印结果为son，empty_son打印结果为空
#代打成功，字符串"son"通过*args打包由Son(Father):没有__str__→Father(Exception):没有__str__→Exception(BaseException):没有__str__→BaseException(Object):__str__
#然后打印
#=========实验16=========#
print("#=========实验16=========#")
list_add_1=[1,1,1]
list_add_2=[2,2,2]
print(list_add_1+list_add_2,list_add_2+list_add_1)                    #列表相加只倒入元素（后一个列表的元素排在前一个后面）
#=========实验17=========#
print("#=========实验17=========#")
def add(a,b):print(a+b)
add(list_add_1,list_add_2)#;add(list_add_1)                    TypeError: add() missing 1 required positional argument: 'b':所给参数与所需参数不符
def add_pro(*add):                 #用*拆解包就可以一定程度上避免乱给参数问题
    b=list(add)                    #为什么是一定程度？因为这只能解决乱给参数数量的问题，而不是类型，例如只给一个参数就不能简单地将参数相加减
    print(sum(b))
    #print([sum(a for a in add)])                 #列表强制执行推导式，注意不能直接sum(a),sum一个元素会报错
add_pro(1,2),add_pro(*[1,2]),add_pro(1,2,3)                 #打包的东西注意提前拆包！否则报错
#=========实验18=========#
print("#=========实验18=========#")
def myprint(*prt,sep=" "):
    print(sep.join(str(str_p) for str_p in prt))                  #我以为你说的myprint里不含print()方法所以我说不会，但是这种形式的话我其实是会的
myprint(*[1,2,3]),myprint("block"),myprint(*"block"),myprint(1,2,3,sep="-"),myprint()                  #记得拆包，同样的集合会去重，若要121则把{}换为[]即可
#可为什么block不受影响？哦对，我给的参数是一坨字符串，*打包的元组只有一个元素，拆开看看，这就对了，中间有空格
#与预测基本一致，都带空格，sep="-"时中间带-
def calculation(*num,operator=""):                  #顺便优化了以前写的四则运算
    error="我不会算喵"
    if len(num)<2 or not operator:
        return error
    else:
        if operator=="+":result=sum(num)
        elif operator=="-":
            result=num[0]
            for n in num[1:]:
                result-=n
        elif operator=="*":
            result=num[0]
            for n in num[1:]:
                result*=n
        elif operator=="/":
            result=num[0]
            for n in num[1:]:
                if n!=0:
                    result/=n
                else:
                    return error
            result=float(f"{result:.2f}")                   #保留两位小数
        else:
            result=error
        return result
print(calculation(1,2,3,operator="+"),calculation(1,2,3,operator="-"),calculation(1,2,3,operator="*"),calculation(1,2.01,0.07,operator="/"),calculation(1,0,3,operator="/"))                  #一次性直接输入数字，连续运算
print(calculation(1),calculation(1,2,3,operator="block"))                   #防住乱给参数的报错
#=========实验19=========#
print("#=========实验19=========#")
