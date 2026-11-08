import random                   #调用random工具，用于生成随机数（randint）
import json                 #调用json工具，用于写读存档模块
import os

#——————classblock——————#

class Egg(Exception):                   #定义（异常）彩蛋类，用于写彩蛋
    pass

#——————classblock——————#

class ModeEgg(Egg):

    #---defblock---#

    def __init__(self, *args):                  #实例化执行方法
        super().__init__(*args)                 #super的init传递

    #---defblock---#

    def __str__(self):                 #彩蛋展示方法
        return"your game had blocked by 'littleblock'\nblocked by block...?"                   #模式彩蛋输出

    #---defblock---#

#——————classblock——————#

class LevelEgg(Egg):

    #---defblock---#

    def __init__(self, *args):
        super().__init__(*args)

    #---defblock---#

    def __str__(self):
        return "littleblock is watching YOU...\nhow did you get that number?!\n...and you win...?"                    #等级菜单输出
        
    #---defblock---#

#——————classblock——————#

class KeyEgg(Egg):

    #---defblock---#

    def __init__(self, *args):
        super().__init__(*args)

    #---defblock---#

    def __str__(self):
        return "sure,you got the really key"                    #答案菜单输出返回

    #---defblock---#

#——————classblock——————#

class Game():                   #定义（object）主类，主程序

    #---defblock---#

    def __init__(self):                 #主类下的__init__(self)方法（类下函数），用于储存实例属性便于调用
        self.data=[]                    #data=[{result1},{result2},...]
        self.save=load_history()        #save=[{result1},{result2},...]开机从硬盘读入存档，每局与data同源双收result，最后写回硬盘存档
        self.level_dict={1:10,2:100,3:200,4:1000,9:5000}                    #dict={键:值}，等级字典，用于选择难度以及通过键映射的值来定义游戏最大数
        self.mode_dict={"N":"常规模式","H":"困难模式","E":"专家模式","block":"彩蛋模式","debug":"开发者模式"}                   #模式字典，用于显示当前模式
        self.mode_weight_dict={"N_healthy":-1,"H_healthy":5,"E_healthy":3,"block_healthy":-1,"debug_healthy":-1,                    #模式权重字典，用于定义健康值（剩余猜测次数）权重
                               "N_score":None,"H_score":1,"E_score":3,"block_score":0,"debug_score":0}                  #用于定义得分权重
        self.num_min=1                  #固定最小值
        self.num_max=None                   #最大值，与难度字典联动，哨兵初始化
        self.result=None                    #游戏结果，哨兵初始化
        self.score=game_stats(self.save)["总得分"]
    
    #---defblock---#

    def __str__(self):
        return f"当前模式{self.mode}，当前难度{self.level},你的积分{self.score}"

    #---defblock---#
    def main_run(self):                 #主类下的主程序方法
        start="是否开始游戏？是为y,其他任意字符为否:"
        answer=input(start)                 #开始游戏选项

        while answer.lower()=="y":                  #开始条件判断
            try:                    #彩蛋判断
                self.choose_mode()                  #调用选择模式方法
            except ModeEgg as e:                 #模式彩蛋模块
                print(e)
                game_result={"答案":"彩蛋","猜测":["彩蛋"],"模式":"彩蛋模式","得分":0}                  #彩蛋结果
                self.data.append(game_result)                   #结果入数据
                history_print(self.data)                    #调用历史打印函数，打印当局数据
                self.save.extend([game_result])                 #结果入存档
                self.save_def()                 #调用存档函数
                continue                    #彩蛋结束，继续循环
   
            self.choose_level()                 #调用选择难度方法

            if self.level=="WIN":                   #难度彩蛋判断
                self.result={"答案":"彩蛋","猜测":["彩蛋"],"模式":"彩蛋","得分":0}                  #难度彩蛋返回
            else:
                self.num_max=self.level_dict[self.level]                   #正常游戏流程，定义最大值

                self.guess_game()                  #调用游戏方法，游戏开始

            self.data.append(self.result)                   #数据存入
            history_print(self.data)                    #调用历史打印函数打印历史数据
            self.save.extend([self.result])                 #存档记录，加入列表外壳防止game_stats函数for循环报错，extend会拆一层外壳
            self.save_def()                 #调用存档方法

            answer=input(start)                 #下一轮开始游戏选项

        data_stats=game_stats(self.data)                    #游戏结束，预热数据值型收官函数
        save_stats=game_stats(self.save)                    #游戏结束，预热存档值型收官函数

        print("感谢游玩！")
        print(f"你总共猜了{data_stats["总局数"]}局,你总共猜了{data_stats["总猜测数"]}次！平均每局猜{data_stats["平均"]:.2f}次！一共赢得了{data_stats["总得分"]}积分！")

        mode_freq_print(data_stats,"你这次都玩过这些模式：")

        print(f"你现在的积分为{save_stats["总得分"]}！")                    #结束输出

        load=input("输入load读档，否则退出：")                  #读档选项

        if load.lower()=="load":                    #读档判断
            history_print(self.save)                    #调用历史打印函数打印存档

            mode_freq_print(save_stats,"你过去都玩过这些模式：")

            print(f"在过去，你总共猜了{save_stats["总局数"]}局,你总共猜了{save_stats["总猜测数"]}次！平均每局猜{save_stats["平均"]:.2f}次！你现在的积分为{save_stats["总得分"]}！")                 #存档数据总结

    #---defblock---#

    def save_def(self):                 #存档方法
        p=os.path.join(os.path.join(os.path.dirname(__file__),"saves"),"save.json")
        with open(p,"w",encoding="utf-8") as f:               #with自动关闭文件，w覆盖重写，utf-8识别中文，f为with定义的（管家）变量
            json.dump(self.save,f,indent=4,ensure_ascii=False)              #json.dump全部写入

        print("存档已记录")                 #存档提示

    #---defblock---#

    def choose_mode(self):                  #模式选择方法
        print("N：普通模式，你可以一直猜，但积分较少")
        print("H：困难模式，你的猜测次数有限，但能得到较多积分")
        print("E：专家模式，你的猜测次数非常有限，但积分很多")                      #模式特征
        mode=input("请选择模式：")                  #定义模式变量

        while mode not in self.mode_dict.keys():
            print("唔嘿~这个还没做~")
            mode=input("请选择模式：")                   #错误输入判断

        if mode!="N":                   #非常规模式判断
            if mode=="debug":                   #开发者模式判断
                print(f"\033[31m[世界意志]\033[0m\033[33m@WILLOFBLOCK.All rights reserved.\033[0m")
                print("\033[31m[世界意志]\033[0m\033[33m欢迎回家，开发者\033[0m")
                print("\033[31m世界凝视着你\033[0m")                 #开发者模式的炫酷红字（自嗨）
            elif mode=="block":                 #彩蛋模式判断
                raise ModeEgg()                 #模式彩蛋异常类抛出
            else:                   #正常非常规模式处理
                print(f"你居然选了{self.mode_dict[mode]}唉~加油~")                  #非常规小彩蛋（雌小鬼语气）
        else:
            print("你选择常规模式，玩的开心")                   #程序（入机）语气

        self.mode=mode                  #mode变量定义（返回）

    #---defblock---#

    def choose_level(self):                   #等级选择方法
        for dif,m in self.level_dict.items():
            print(f"难度{dif}为（1~{m}）")                    #等级难度特征输出

        print("请选择难度")                   #提示语打印，input在询问整数函数

        while True:                   #等级校验循环
            try:
                level_chose=ask_int()                   #等级判断
            except Egg:                 #等级彩蛋（异常）处理
                level_egg="WIN"                 #等级彩蛋胜利处理
                self.level=level_egg
                print(LevelEgg())                   #等级彩蛋异常类调用，提前结束防止报错
                return
            if level_chose in self.level_dict:                  #判断多种变量值时用and（与）或not in（非）
                break
            elif level_chose<min(self.level_dict):
                print("宝宝这太简单了。。。")
            elif level_chose>max(self.level_dict):
                print("宝宝这太难了吧。。。")
            else:
                print("唔嘿~这个还没做~")                       #字典外等级处理

        self.level=level_chose
        return                  #等级变量返回

    #---defblock---#

    def guess_game(self):                    #游戏主体方法
        guesses=[]
        num=None
        score=0                  #哨兵初始化
        key=random.randint(self.num_min,self.num_max)                   #取随机答案
        healthy=self.level*self.mode_weight_dict[f"{self.mode}_healthy"]                    #定义健康值

        while num!=key:                 #猜数字循环
            if self.mode=="debug":
                print(f"\033[31m[世界意志]\033[0m\033[33m@WILLOFBLOCK.All rights reserved.\033[0m")
                print(f"\033[31m[世界意志]\033[0m\033[33m{key}\033[0m")
                print(f"\033[31m[世界意志]\033[0m\033[33mscore changed\033[0m")
                score=-274380                  #debug模式分数重置（与自嗨）
            if healthy==0:                   #失败判断
                print("哦不~你失败了~真是杂鱼~")
                self.result={"答案":key,"猜测":guesses,"模式":self.mode_dict[self.mode],"得分":0}
                return                  #失败结果返回
            elif healthy>0:
                print(f"你还有{healthy}次~加油哦~")                  #生命值提示

            print(self)
            if len(guesses)>2:
                print(f"你最近三次的猜测：{guesses[-3:]}")
            print("请猜数字")                   #猜测输入提示

            try:
                num=ask_int()                   #调用询问整数函数
                guesses.append(num)                     #猜测记录

                if num<key:
                    print("猜小了！")
                    healthy=healthy-1
                elif num>key:
                    print("猜大了！")
                    healthy=healthy-1                   #错误判断与生命值减少

            except Egg:                 #彩蛋（异常）处理
                print(KeyEgg())                 #答案彩蛋异常类调用
                guesses.append(274380)                  #彩蛋记录
                score=-274380
                break                   #彩蛋触发游戏胜利，清零分数

        print("恭喜你猜对了！")                 #胜利输出

        if score!=-274380:                  #清零判断
            score=self.level_dict[self.level]/100                   #一阶得分公式
            if self.mode!="N":
                print("好厉害呢~")                  #非常规模式胜利彩蛋
                score+=healthy*self.level*self.mode_weight_dict[f"{self.mode}_score"]                  #二阶得分公式
        else:
            score=0                 #清零处理

        self.result={"答案":key,"猜测":guesses,"模式":self.mode_dict[self.mode],"得分":score}
        return                  #成功记录返回
    
    #---defblock---#

#——————classblock——————#

#---defblock---#

def ask_int():                 #询问整数函数 
    while True:                 #始终为真循环（因为函数只有一个循环）
        num=input("：")                   #值型定义
        if num=="274380":                   
            raise Egg()                 #彩蛋（异常）抛出
        else:
            try:
                return int(num)                 #值型正常则返回
            except ValueError:
                print("至少输个整数吧宝宝。。。")                   #值型异常输出

#---defblock---#

def history_print(data_h_p):                    #历史打印函数
    for n,history in enumerate(data_h_p):                   #for循环拆分列表，enumerate=编号（从0开始），元素
        print(f"第{n+1}局历史记录：{history}")
        print(f"该局猜过的数字有{history["猜测"]}，该局答案为{history["答案"]}！")                  #历史打印

#---defblock---#

def game_stats(stats):                   #值型收官函数
    if not stats:                  #0值判断
        print("你还没玩过呢宝宝")
        return{"总局数":0,"总猜测数":0,"平均":0,"总得分":0,"模式频率":{}}                 #0值返回

    mode_freq={}
    for data_dict in stats:
        mode_freq[data_dict["模式"]]=mode_freq.get(data_dict["模式"],0)+1                   #字典型去重计数器统计模式频率

    guesses_num=sum(len(data_dict["猜测"]) for data_dict in stats)
    score_all=sum(data_dict["得分"] for data_dict in stats)                    #变量初始化计算定义

    return{"总局数":len(stats),"总猜测数":guesses_num,"平均":guesses_num/len(stats),"总得分":score_all,"模式频率":mode_freq}                   #收官输出

#---defblock---#

def mode_freq_print(stats_f,title):
    print(title)
    for mode_nam,mode_num in stats_f["模式频率"].items():
        print(f"{mode_nam}：{mode_num}")

#---defblock---#

def load_history():                 #读档函数
    os.makedirs(os.path.join(os.path.dirname(__file__),"saves"),exist_ok=True)
    p=os.path.join(os.path.join(os.path.dirname(__file__),"saves"),"save.json")
    try:
        with open(p,"r",encoding="utf-8") as f:
            return json.load(f)                 #读档返回
        
    except FileNotFoundError:
        return []                   #空存档返回处理
    except json.JSONDecodeError:
        print("谁把你存档搞坏了？没关系我帮你重置了宝宝~")
        return []                   #坏存档返回处理

#---defblock---#

game=Game()                 #主类预热
game.main_run()                 #主运行方法调用，开机

#=========四阶段毕业=========#