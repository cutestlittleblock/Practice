#=========转化器=========#
"""
转化器\n
负责处理原始输入及缩放转化\n
"""
#=========转化器=========#
try:
    import pack
    pack.copyer(r"C:\Users\cutes\Desktop\copy\初等函数计算器","transformer.txt",(6,12))
except ModuleNotFoundError:pass
#调用打包复制工具(可删,以下为正文)
#=========转化器=========#
import re
token=re.compile(
                r"""
                \d+\.?\d*|e|pi|π|i|°|#数与角度
                \+|\-|\*|/|//|%|\^|!!|!|#算符
                \(|\)|<|>|#括号与绝对值
                sin|cos|tan|cot|sec|csc|#三角函数
                arcsin|asin|arccos|acos|arctan|atan|#反三角函数
                ln|lg|log|~|#对数函数
                sh|sinh|ch|cosh|th|tanh|#双曲函数
                arsh|ash|arsinh|asinh|arch|ach|arcosh|acosh|arth|ath|artanh|atanh#反双曲函数
                """,
                re.VERBOSE
                )#分词器
precision=None;P=None#精度
#初始化声明

#---defblock---#

def adjustment(switch):
    """该函数用于调节精度喵"""
    global precision,P
    #初始化声明
    if switch=="p":precision=None;P=None
    #精度复位
    while precision is None:
        try:
            precision=int(input("你需要小数点后几位喵："))
            if precision<0:raise ValueError
        except (ValueError, TypeError):print("没有这样的精度喵");precision=None;continue
    P=precision*2+10

#---defblock---#

def transint(N):
    """该函数用于精度初始化
    将浮点转为指定精度的大整数进行计算喵"""
    try:float(N)
    except (ValueError, TypeError):return N
    #跳过算符及e,pi
    I,_,D=str(N).partition(".")
    return int(I+(D+"0"*P)[:P])

#---defblock---#

def transstr(N):
    """该函数用于表达最终答案
    将最终结果转换为指定精度的浮点字符串喵"""
    zoom=10**(P-precision)
    if isinstance(N,str):N=transint(N)
    #单一输入处理
    if isinstance(N,tuple):
    #复数答案处理
        R=transstr(N[0]);I=transstr(N[1])
        if N[0] and N[1]:return R+(I if I[0]=="-" else "+"+I)+"i"
        else:return (I+"i" if N[0]==0 else R)

    A=str(((N if N>=0 else -N)+zoom//2)//zoom).zfill(precision+1)
    return ("-" if N<0 else "")+A[:-precision]+"."+A[-precision:]