try:
    import pack
    pack.copyer(r"C:\Users\cutes\Desktop\copy\初等函数计算器","terminals.txt",10)
    pack.packer(
                r"C:\Users\cutes\Desktop\copy\初等函数计算器","初等函数计算器.txt",
                ["terminals.py","main.py","transformer.py","stack.py","calculation.py"],[10,6,6,6,6]
                )
except ModuleNotFoundError:pass
#调用打包复制工具(可删,以下为正文)
#=========终端=========#
"""
          终端
负责调用主交互文件运行程序
"""
import main
shift=True
#初始化声明
while shift:
#运行
    main.run(shift)
    shift=input("回车下班喵，键入h查看历史记录喵，键入p改变精度喵，键入其他任意继续算喵：")