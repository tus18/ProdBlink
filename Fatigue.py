import subprocess
import time
from List import list_create


class Fatigue:#数値から疲れを検出するクラス(画像は扱わない)
    def __init__(self):
        #音楽ファイル名
        name='music'
        #サブプロセスの呼び出しコマンド
        self.cmd = "python sub.py "+str(name)

        self.is_open = False
        self.time_start = time.time()
        self.count = 0
        self.minutes = 0
        self.l = []
        self.l_count = []
        self.up_count = 0
        self.down_count =0
        self.stock = 0
        self.sleepy_count = 0
        self.is_alarm_on = False
        self.list_creator = list_create()
        self.sample_time = 30
        self.sleepy_time = 300



    def __call__(self,eye):
        if eye > self.EYE_AR_OPEN:
            self.is_open = True
            self.sleepy_count = 0
        elif eye < self.EYE_AR_CLOSED and self.is_open == True:
            self.count += 1
            self.is_open = False
        elif self.is_open == False:
            self.sleepy_count += 1

        if self.sleepy_count > self.sleepy_time:
            #眠たい時に起こす処理
            self.alarm()

        #各メソッドの呼び出し
        self.add_list()

        return self.count,self.is_open  #仕様変更


    def setting(self,person):#EYE_AR_OPENとself.EYE_AR_CLOSEDの設定を変更
        file_name = "user/"+person+".data"
        file = open(file_name, "r")
        line = file.readline()
        file.close()
        max, min = line.split()
        max = float(max)
        min = float(min)

        print("max:",max,"\nmin:",min)

        n = (max+min)/2

        self.EYE_AR_OPEN = n*1
        self.EYE_AR_CLOSED = n*0.7

        self.EYE_AR_OPEN = round(self.EYE_AR_OPEN,4)
        self.EYE_AR_CLOSED = round(self.EYE_AR_CLOSED,4)
        print("middle:",n)
        print("open:",self.EYE_AR_OPEN,"\nclose:",self.EYE_AR_CLOSED)


    def add_list(self):
        time_end = time.time()
        tim = time_end - self.time_start
        if tim  >=  60:
            self.l_count.append(self.count)
            self.time_start = time_end
            self.minutes += 1
            if self.minutes == self.sample_time:
                #1mの平均瞬き回数
                self.a = self.count/self.sample_time
                self.a = int(self.a)
                #直近の最大値に設定
                self.peak = self.count - self.a*self.minutes
                self.l.append(self.peak)

            if self.minutes > self.sample_time:
                self.analyze()


    def analyze(self):#30m以降に1m毎実行される(疲れを検出する)

        self.l.append(self.count - self.a*self.minutes)
        print(self.l)#確認用(消してもOK)

        #グラフの作成
        self.list_creator(self.l)

        if self.l[len(self.l)-3] < self.l[len(self.l)-2] > self.l[len(self.l)-1]:
            if self.peak < self.l[len(self.l)-2]:
                self.up_count += 1
                if self.down_count < 2:
                    self.down_count = 0
            elif self.peak > self.l[len(self.l)-2]:
                self.down_count += 1
                if self.up_count < 2:
                    self.up_count = 0
            self.peak = self.l[len(self.l)-2]
            self.stock = len(self.l)-1

        elif self.l[len(self.l)-3] < self.l[len(self.l)-2] < self.l[len(self.l)-1]:
            self.up_count += 1
            self.stock = len(self.l) - 1
            self.peak = self.l[len(self.l)-1]
            if self.down_count < 2:
                self.down_count = 0
        
        elif self.l[len(self.l)-3] > self.l[len(self.l)-2] > self.l[len(self.l)-1]:
            self.down_count += 1
            self.stock = len(self.l) - 1
            self.peak = self.l[len(self.l)-1]
            if self.up_count < 2:
                self.up_count = 0
        
        if self.down_count > 1 and self.up_count > 1:#疲れの検出
            self.down_count = self.up_count = 0
            self.alarm()


    def alarm(self):#音楽を流す
        if hasattr(self, 'pro'):
            if not self.pro.poll() is None:
                self.pro = subprocess.Popen(self.cmd)
        else:
            self.pro = subprocess.Popen(self.cmd)
        self.is_alarm_on = True  # アラームがオンになったらフラグをTrueに


    def alarm_end(self):
        if hasattr(self, 'pro'):
            if self.pro.poll() is None:
                self.pro.terminate()
        self.is_alarm_on = False  # アラームを止めたらフラグをFalseに
    

    def end_process(self):#ファイルに書き込みなどを記述(途中)
        print(self.l)
        self.alarm_end()
        if len(self.l) != 0:
            with open("data/analyze.txt","a") as file:
                file.write(f"{self.l}\n")
        if len(self.l_count) != 0:
            with open("data/brink.txt","a") as file:
                file.write(f"{self.l_count}\n")

