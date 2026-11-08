class main():

#——————classblock——————#

    #---defblock---#

    def __init__(self):
        self.pillar=[]
        self.y_list=[]
        self.rain=[]

    #---defblock---#

    def run(self):
        self.pillar_creater()
        self.y_n_creater()
        self.rain_judge()
        print(sum(self.rain))

    #---defblock---#

    def pillar_creater(self):                 #造柱子函数
        given_pillar=input("请给定柱子,数字间用“,”隔开:")

        n_str=given_pillar.split(",")
        for n in n_str:
            self.pillar.append(int(n))                   #利用split把输入字符串转入列表再int遍历处理为新列表

    #---defblock---#

    def y_n_creater(self):
        pillar_shift=[]
        y=[]
        while sum(self.pillar)!=0:
            for n_wall in self.pillar:
                if n_wall>0:
                    pillar_shift.append(n_wall-1)
                    y.append(1)
                else:
                    pillar_shift.append(0)
                    y.append(0)
            self.y_list.append(y)                   #柱子按y坐标拆分
            y=[]
            self.pillar=pillar_shift
            pillar_shift=[]

    #---defblock---#

    def rain_judge(self):
        for y_n in self.y_list:
            for x,wora in enumerate(y_n):
                if wora ==1:                    #wall=1
                    pass
                else:                   #air=0
                    right=has_wall_right(x,y_n)                     #x is air`s idnex,y_n is one of element in y_list
                    left=has_wall_left(x,y_n)                    #累加/累减函数找air的wall
                    if right==True and left==True:
                        self.rain.append(1)
        return self.rain

#——————classblock——————#

#---defblock---#

def has_wall_right(x,y_n):
    for i in range(x+1,len(y_n)):
        if y_n[i]==1:
            return True
    return False

#---defblock---#

def has_wall_left(x,y_n):
    for i in range(x-1,-1,-1):
        if y_n[i]==1:
            return True
    return False

#---defblock---#

Save_Rain=main()
Save_Rain.run()