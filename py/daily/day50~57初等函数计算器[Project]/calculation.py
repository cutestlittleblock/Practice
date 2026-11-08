#=========计算包=========#
"""
                           计算包\n
                基于浮点数缩放为大整数进行计算\n
        传入与返回值均为网格值(真值*zoom)的整数结果\n
方块函数为模块内调用且只由模块内一般函数传缩放后参数故无需内部缩放\n
"""
#=========计算包=========#
try:
    import pack
    pack.copyer(r"C:\Users\cutes\Desktop\copy\初等函数计算器","calculation.txt",(8,14))
except ModuleNotFoundError:pass
#调用打包复制工具(可删,以下为正文)
#=========计算包=========#
import transformer as t
inf=1e303;zoom=None;block_set={"por","exp","atan","arth","ln","arg"}
class CalculateError(Exception):pass
#初始化声明

#---defblock---#

def Zoom(calfunc):
    """"缩放装饰器用于给出缩放精度喵"""
    def wrapper(*args):
        """前面参数为运算数，最后一个参数为运算符喵"""
        global zoom
        zoom=10**t.P;cal=[]
        #参数初始化
        if calfunc.__name__ in block_set:return calfunc(*args)
        #方块函数调用直接传参
        for p in args:
            if isinstance(p,tuple) and p[1]==0:p==p[0]
            cal.append(p if isinstance(p,int) else t.transint(p))
        #一般函数缩放转化传参
        return calfunc(*cal)
    return wrapper

#---defblock---#

@Zoom
def basic(x,o,y):
    """该函数用于进行基本四则运算及处理幂函数喵"""
    evaluation={
                "+":lambda x,y:x+y,"-":lambda x,y:x-y,
                "*":lambda x,y:x*y//zoom,"/":lambda x,y:x*zoom//y,
                "//":lambda x,y:(x//y)*zoom,"%":lambda x,y:x%y,
                "@":lambda x,y:x*y,"^":exponent
                }#推导式
    #初始化声明
    if isinstance(x,tuple) or isinstance(y,tuple):
    #复数计算
        x=x if isinstance(x,tuple) else (x,0);y=y if isinstance(y,tuple) else (y,0)
        xr,xi=x;yr,yi=y
        if o in ("+","-"):return (evaluation[o](xr,yr),evaluation[o](xi,yi))
        elif o in ("*","@"):return (evaluation[o](xr,yr)-evaluation[o](xi,yi),evaluation[o](xr,yi)+evaluation[o](xi,yr))
        elif o=="/":return (evaluation[o](xr*yr+xi*yi,yi*yi+yr*yr),evaluation[o](xi*yr-xr*yi,yi*yi+yr*yr))
        elif o=="^":return exponent(x,y)
        else:raise CalculateError("复数不能整除喵" if o=="//" else "复数不能取模喵")

    else:return evaluation[o](x,y)
    #实数运算

#---defblock---#

@Zoom
def arg(z):
    """
               方块函数\n
    辐角函数用于转化复数极坐标辐角喵\n
    """
    r,i=z
    if r==0:return pi()//2 if i>0 else -pi()//2
    #实部为0时辐角为±pi/2
    if r>0:return arctan(i*zoom//r)
    else:return pi()+arctan(i*zoom//r) if i>=0 else -pi()+arctan(i*zoom//r)
    #II,III象限辐角回归:II:pi-|arctan(i/r)|,III:-pi+|arctan(i/r)|

#---defblock---#

@Zoom
def por(x,y):
    """
             方块函数\n
    整数幂函数用于计算整数次方喵\n
    """
    if y<0:return zoom*zoom//por(x,-y)
    #倒数处理:x^-y=1/x^y;(x^-y)*zoom=zoom*zoom//(x^y)
    xy=zoom
    while y:
        if y&1:xy=xy*x//zoom
        x=x*x//zoom;y>>=1
    return xy

#---defblock---#

@Zoom
def exp(x):
    """
              方块函数\n
    自然指数函数用于计算e的x次方喵\n
    """
    Rn=10**(t.P-t.precision-3)
    if not isinstance(x,tuple):
    #实数域自然指数处理
        n=0;T=zoom;expx=zoom;I=x//zoom;D=x%zoom
        while T>=Rn:
            n+=1;T=T*D//(zoom*n);expx+=T
            #T{n}=x^n/n!;Tn=T{n-1}*x/n--ZOOM-->Tn=T{n-1}*x//(zoom*n)
            #首项自带缩放,后续项去缩放
        return por(e(),I)*expx//zoom
    else:
        #复数域自然指数处理
        z=x;r,i=z
        I=r//zoom;D=r%zoom;i%=2*pi();z=(D,i)
        n=0;T=(zoom,0);expz=(zoom,0)
        while T[0]*T[0]+T[1]*T[1]>=Rn*Rn:
            n+=1;T=basic(T,"*",basic(z,"/",zoom*n));expz=basic(expz,"+",T)
        expz=basic(por(e(),I),"*",expz)
        return expz

#---defblock---#

@Zoom
def arctan(x):
    """
             方块函数\n
    反正切函数用于计算arctan(x)喵\n
    """
    Rn=10**(t.P-t.precision-3)
    n=0;T=x;atanx=x
    if not isinstance(x,tuple):
    #实数域反正切处理
        if abs(x)==zoom:return pi()//4 if x>0 else -pi()//4
        if abs(x)>zoom:return pi()//2-arctan(zoom*zoom//x) if x>0 else -pi()//2-arctan(zoom*zoom//x)
        #x=±1时arctan(1)=±pi/4,|x|>1时利用恒等式atan(x)=±pi/2-atan(1/x),绕开大量(约10^(p+3)项)递推
        while T>=Rn or T<=-Rn:
            n+=1;T=-T*x*x*(2*n-1)//(zoom*zoom*(2*n+1));atanx+=T
            #T{n}=(-1)^n*x^(2n+1)/(2n+1);T{n}=-T{n-1}*x^2*(2n-1)/(2n+1)--ZOOM-->T{n}=-T{n-1}*x*x*(2n-1)//(zoom*zoom*(2n+1))
            #首项自带缩放,后续项去缩放
        return atanx

#---defblock---#

@Zoom
def arth(x):
    """
              方块函数\n
    反双曲正切函数用于计算arth(x)喵\n
    """
    Rn=10**(t.P-t.precision-3)
    n=0;T=x;arthx=x
    if not isinstance(x,tuple):
    #实数域反双曲正切处理
        if absolute(x)<=zoom:
            if absolute(x)==zoom:raise CalculateError("反双曲正切函数在±1处为无定义极点喵,趋于±∞喵")
            while T>=Rn or T<=-Rn:
                n+=1;T=T*x*x*(2*n-1)//(zoom*zoom*(2*n+1));arthx+=T
                #T{n}=x^(2n+1)/(2n+1);T{n}=T{n-1}*x^2*(2n-1)/(2n+1)--ZOOM-->T{n}=T{n-1}*x*x*(2n-1)//(zoom*zoom*(2n+1))
                #首项自带缩放,后续项去缩放
        else:arthx=basic(basic(ln(zoom+x),"-",ln(zoom-x)),"/",2*zoom)
        #超实数域定义转复数域莫比乌斯变换:arthx=0.5ln((1+x)/(1-x))=0.5(ln(1+x)-ln(1-x))=0.5(ln(zoom+x)-ln(zoom-x))
        return arthx
    else:
    #复数域反双曲正切处理
        z=x;arthz=basic(basic(ln(basic(zoom,"+",z)),"-",ln(basic(zoom,"-",z))),"/",2*zoom)
        #复数域莫比乌斯变换:arthz=0.5ln((1+z)/(1-z))=0.5(ln(1+z)-ln(1-z))=0.5(ln(zoom+z)-ln(zoom-z))
        return arthz

#---defblock---#

@Zoom
def ln(x):
    """
             方块函数\n
    自然对数函数用于计算ln(x)喵\n
    """
    lnx=None;k=0
    if isinstance(x,tuple):
    #复数域自然对数处理
        z=x;r,i=z
        return (ln((r*r+i*i)//zoom)//2,arg(z))
        #lnz=ln(r*e^iθ)=ln(|z|*e^(iarg(z)))=ln(|z|)+iarg(z)=0.5ln(r^2+i^2)+iarg(z)=(0.5ln((r*r+i*i)//zoom),arg(z))
    else:
    #实数域自然对数处理
        if x==0:raise CalculateError("对数函数在0处为无定义极点喵,log0趋于负∞喵")
        if x<zoom:lnx=-ln(zoom*zoom//x)
        #x<1时利用恒等式ln(x)=-ln(1/x)缩放,绕开大量递推
        else:
            while x>2*zoom:
                x//=2;k+=1
            #x>2时利用lnx=kln2+ln(x/2^k)的恒等式,将x缩小到[1,2]区间内
            lnx=ln2()*k+arth((x-zoom)*zoom//(x+zoom))*2
            #莫比乌斯变换:lnx=2*arth((x-1)/(x+1))
            return lnx
        if x<0:return (ln(-x),pi())
        #超实数域定义转复数域

#---defblock---#

@Zoom
def exponent(x,y):
    """幂函数用于计算乘方喵"""
    if isinstance(x,tuple) or isinstance(y,tuple):return exp(basic(y,"*",ln(x)))
    #复数幂
    else:
    #实数幂
        if x==0 and y>0:return 0
        if x==0 and y==0:return zoom
        if x==0 and y<0:raise CalculateError("0的负数次幂为无定义极点喵,趋于∞喵")
        #0的幂
        if y%zoom==0:return por(x,y//zoom)
        #整数幂
        else:
        #非整数幂
            I=y//zoom;D=y%zoom
            return por(x,I)*exp(D*ln(x)//zoom)//zoom

#---defblock---#

@Zoom
def absolute(x):
    """绝对值函数用于计算绝对值和模长喵"""
    if isinstance(x,tuple):return exponent(por(x[0],2)+por(x[1],2),zoom//2)
    #复数模运算:(xr^2+xi^2)^(1/2)
    return(x if x>=0 else -x)
    #实数绝对值运算

#---defblock---#

@Zoom
def gamma(x,o):
    """伽马函数用于计算(双)阶乘喵"""
    if o=="!!":
    #双阶乘计算
        try:
            if x%zoom or x<0:raise ValueError
            x//=zoom;y=x
            if x==0 or x==1:return zoom
        except (ValueError, TypeError):raise CalculateError("双阶乘的输入必须正整数喵")
        for n in range(x-2,1,-2):y*=n
        return y*zoom

    if o=="!":
    #常规阶乘计算
        try:
            if x%zoom or x<0:raise ValueError
            if not x%zoom and x<0:raise CalculateError("负整数阶乘为无定义极点喵,趋于∞喵")
            x//=zoom;y=x
            if x==0:return zoom
            for n in range(x-1,1,-1):y*=n
            return y*zoom
        except (ValueError, TypeError):pass

#---defblock---#

@Zoom
def logarithm(o,x,y):
    """对数函数用于计算log(x)喵"""
    lnx=ln(x)
    if y!=None:lny=ln(y)
    #一般底数的真数计算
    evaluation={
                "ln":lambda:lnx,
                "lg":lambda:basic(basic(lnx,"*",zoom),"/",ln10()),
                "log":lambda:basic(basic(lnx,"*",zoom),"/",lny)
                }#推导式
    return evaluation[o]()

#---defblock---#

@Zoom
def trigono(o,x):
    """三角函数用于计算sin/cos/tan/cot/sec/csc喵"""
    sinx=None;cosx=None;sinz=None;cosz=None
    if not isinstance(x,tuple):
    #实数域三角函数
        tri=exp((0,x));sinx=tri[1];cosx=tri[0]
        #e^(ix)=cosx+isinx
    else:
    #复数域三角函数
        z=x;r,i=z
        sinz=basic(basic(exp((-i,r)),"-",exp((i,-r))),"/",(0,2*zoom));cosz=basic(basic(exp((-i,r)),"+",exp((i,-r))),"/",2*zoom)
        #sinz=(e^(-iz)-e^(iz))/(2i);cosz=(e^(-iz)+e^(iz))/2;z*i=(r,i)*i=(-i,r)复平面旋转
    evaluation={
                "sin":lambda:sinx if sinx!=None else sinz,
                "cos":lambda:cosx if cosx!=None else cosz,
                "tan":lambda:basic(sinx,"/",cosx) if sinx!=None else basic(sinz,"/",cosz),
                "cot":lambda:basic(cosx,"/",sinx) if cosx!=None else basic(cosz,"/",sinz),
                "sec":lambda:basic(zoom,"/",cosx) if cosx!=None else basic(zoom,"/",cosz),
                "csc":lambda:basic(zoom,"/",sinx) if sinx!=None else basic(zoom,"/",sinz)
                }#推导式
    return evaluation[o]()

#---defblock---#

Euler={};Ludolphine={};IIlog={};Xlog={}
#常数初始化缓存
def e():
    if t.P not in Euler:Euler[t.P]=exp(10**t.P)
    return Euler[t.P]
#泰勒展开:e=exp(1)=1+1/1!+1/2!+1/3!+...+1/n!+...
def pi():
    if t.P not in Ludolphine:Ludolphine[t.P]=16*arctan(10**t.P//5)-4*arctan(10**t.P//239)
    return Ludolphine[t.P]
#马青公式:pi=16*arctan(1/5)-4*arctan(1/239)
def ln2():
    if t.P not in IIlog:IIlog[t.P]=ln(2*10**t.P)
    return IIlog[t.P]
#莫比乌斯变换:lnx=2arth((x-1)/(x+1));ln2=2*arth(1/3)
def ln10():
    if t.P not in Xlog:Xlog[t.P]=ln(10*10**t.P)
    return Xlog[t.P]
#莫比乌斯变换:lnx=2arth((x-1)/(x+1));ln10=3ln2+ln(5/4)=3ln2+2*arth(5/4)