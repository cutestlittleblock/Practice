import time,os,inspect

#---defblock---#

def copyer(path,name,line):
    """
    拷贝函数,用于将当前文件内容拷贝到指定路径的指定文件中,按年月日时分类
    第一个参数为期望拷贝路径,第二个参数为拷贝文件名,第三个参数为读取起点行
    """
    ori=os.path.abspath(inspect.stack()[1].frame.f_globals["__file__"])#起点路径
    timedir=time.strftime("%Y_%m_%d_%H")#时间戳
    os.makedirs(
                os.path.join(
                             os.path.abspath(path),#指定文件夹
                             timedir
                             ),
                exist_ok=True
                )
    end=os.path.join(os.path.abspath(path),timedir,name)#终点路径

    with open(ori,"r",encoding="utf-8") as f:
        for _ in range(line-1):
            f.readline()
        code=f.read()
    with open(end,"w",encoding="utf-8") as f:f.write(code)

#---defblock---#

def packer(path,name,filepack,line):
    """
    打包函数,用于将指定的一系列文件内容拷贝进同一个指定路径下指定文件,按年月日时分类
    第一个参数为期望打包路径,第二个参数为打包文件名,第三个参数为同一路径下的打包文件名列表,第四个参数为读取起点行列表
    """
    ori=os.path.dirname(os.path.abspath(inspect.stack()[1].frame.f_globals["__file__"]))#起点文件夹路径
    timedir=time.strftime("%Y_%m_%d_%H")#时间戳
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
            for _ in range(line[n]-1):
                f.readline()
            code+=f.read()
    with open(end,"w",encoding="utf-8") as f:f.write(code)