#=========主交互文件=========#
"""
主交互文件\n
负责调用相关模块处理输入\n
"""
#=========主交互文件=========#
try:
    import pack
    pack.copyer(r"C:\Users\cutes\Desktop\copy\初等函数计算器","main.txt",(6,12))
except ModuleNotFoundError:pass
#调用打包复制工具(可删,以下为正文)
#=========主交互文件=========#
import transformer as t;import stack as s;import calculation as c;import information as i
#初始化声明

#---defblock---#

def mode_choose():
    """该函数用于选择分式或小数结果输出喵"""
    global mode
    #初始化声明
    mode=None
    while True:
        mode=input("键入/或.切换分式或小数结果输出喵:")
        if mode not in ("/","."):print("没有这样的模式喵")
        else:return True

#---defblock---#

def run(shift):
    """这是主程序运行函数喵"""
    put_stack=t.token.findall(input("我需要算什么喵："))
    #分词入栈
    t.adjustment(shift)
    #精度调节
    try:
        answer=t.transstr(s.stack(put_stack))
        mode_choose()
        if mode == "/":
            if isinstance(answer,list):print(f"答案是{answer[0]}/{answer[1]}喵")
            else:
                if answer[-1] == "i":print("复数不支持转为分式喵",f"答案是{answer}喵")
                else:answer=c.reduce(t.transint(answer));print(f"答案是{answer[0]}/{answer[1]}喵")
        else:
            if isinstance(answer,list):answer=t.transstr(c.basic(answer,"//",None))
            print(f"答案是{answer}喵")
    except ZeroDivisionError:print("分母不能为0喵")
    except OverflowError:print("太大了喵，算不出来了喵")
    except s.EmptyError:print("这根本没东西可算喵")
    except c.CalculateError:print("别乱输喵")
    #答案出栈