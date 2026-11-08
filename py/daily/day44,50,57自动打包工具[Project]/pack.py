"""
打包工具:用于打包,拷贝文件
"""
import time,os,inspect

#---defblock---#

def copyer(path,name,skip):
    """
    拷贝函数,用于将当前文件内容拷贝到指定路径的指定文件中,按年月日时分类\n
    第一个参数为期望拷贝路径:为字符串形式的绝对路径,调用对象将会被拷贝到该路径下\n
    第二个参数为拷贝文件名:为字符串形式的期望文件名,调用对象将会被拷贝到该文件中\n
    第三个参数为读取跳过行:可以用单一整数x表示跳过第x行,或单一元组(s,e)表示跳过从s行到e行,或将上述参数放入同一列表中来逐个读取\n
    """
    ori=os.path.abspath(inspect.stack()[1].frame.f_globals["__file__"])#起点路径
    timedir=time.strftime("%Y_%m_%d_%H")#时间戳
    code=""#对象源码
    os.makedirs(
                os.path.join(
                             os.path.abspath(path),#指定文件夹
                             timedir
                             ),
                exist_ok=True
                )
    end=os.path.join(os.path.abspath(path),timedir,name)#终点路径

    with open(ori,"r",encoding="utf-8") as f:
        for i,line in enumerate(f,start=1):
            if not isinstance(skip,tuple):skip=(skip,skip)
            if skip[0]<=i<=skip[1]:continue
            code+=line
    with open(end,"w",encoding="utf-8") as f:f.write(code)

#---defblock---#

def packer(path,name,filepack,skips):
    """
    打包函数,用于将指定的一系列文件内容拷贝进同一个指定路径下指定文件,按年月日时分类\n
    第一个参数为期望打包路径:为字符串形式的绝对路径,调用对象将会被拷贝到该路径下\n
    第二个参数为打包文件名:为字符串形式的期望文件名,调用对象将会被拷贝到该文件中\n
    第三个参数为同一路径下的打包文件名列表:为字符串列表形式依次排列的调用对象名\n
    第四个参数为读取参数列表:为整数/元组构成的列表,依次对应第三个参数中每个文件的读取参数,参数规则同copyer(...,line)\n
    """
    ori=os.path.dirname(os.path.abspath(inspect.stack()[1].frame.f_globals["__file__"]))#起点文件夹路径
    timedir=time.strftime("%Y_%m_%d_%H")#时间戳
    code=""#对象源码
    os.makedirs(
                os.path.join(
                             os.path.abspath(path),#指定文件夹
                             timedir
                             ),
                exist_ok=True
                )
    end=os.path.join(os.path.abspath(path),timedir,name)#终点路径
    code=""
    for n,p in enumerate(filepack):
        with open(os.path.join(ori,p),"r",encoding="utf-8") as f:
            for i,line in enumerate(f,start=1):
                if not isinstance(skips[n],tuple):skips[n]=(skips[n],skips[n])
                if skips[n][0]<=i<=skips[n][1]:continue
                code+=line
        code+="\n"
    with open(end,"w",encoding="utf-8") as f:f.write(code)