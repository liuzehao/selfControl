#!/usr/bin/env python
# coding=utf-8
import random as rd
import sys
import os
from datetime import datetime
sys.stdin = open('whattodo.txt', 'r',encoding='utf-8')

def get_all_files(bg_path):
    files = []
    for f in os.listdir(bg_path):
        if os.path.isfile(os.path.join(bg_path, f)):
            files.append(os.path.join(bg_path, f))
        else:
            files.extend(get_all_files(os.path.join(bg_path, f)))
    if len(files)>0:
        files.sort(key=lambda x: int(x[-6:-4]))#排序从小到大
    return files
def get_all_files_nosort(bg_path):
    files = []
    for f in os.listdir(bg_path):
        if os.path.isfile(os.path.join(bg_path, f)):
            files.append(os.path.join(bg_path, f))
        else:
            files.extend(get_all_files(os.path.join(bg_path, f)))
    return files
class randomMachine(object):
    def __init__(self):#得到今天的时间，
        #读入文件以及所有项目
        n = int(sys.stdin.readline().strip())
        self.dic=dict()#所有的项目
        i=0
        while i<n:
            a, b = sys.stdin.readline().strip().split(' ')
            self.dic[a]=b
            i+=1
        #创建一个新的以时间命名的文件夹
        self.today=datetime.now().strftime("%Y%m%d")#今天的时间
        self.strr = "log/" + self.today#今天的文件地址
        if not os.path.exists(self.strr):
            os.makedirs(self.strr)
        

    def setWeight(self, weight):
        self.weight = weight
        self.chanceList=[]
        for k,v in self.weight.items():
            for t in range(int(v)):
                self.chanceList.append(k)
    
    def drawing(self):
        files=get_all_files(self.strr)
        r = rd.randrange(0, len(self.chanceList))  # 随机数
        self.choose=self.chanceList[r]
        #这里保证了两次选择不会相等
        if len(files)>0: 
            last_file=files[-1][:-8]
            while os.path.join(self.strr,self.choose)==last_file:
                r = rd.randrange(0, len(self.chanceList))  # 随机数
                self.choose=self.chanceList[r]
        return self.choose
    def create(self):#创建一个文件，命名方式为读取当前文件夹最后一个文件编号，在此基础上加一，如果没有创建001
        #get all file
        files=get_all_files(self.strr)
        if len(files)==0:
            filename=self.choose+"_000.txt"
        else:
            # print(files)
            flag=int(files[-1][-6:-4])+1
            filename=self.choose+"_"+str('%03d'%flag)+".txt"
        full_path=os.path.join(self.strr,filename)
        newfile=open(full_path, 'w')
        newfile.write("上一次有哪些目标:" + "\n")
        newfile.write("这45分钟完成了上一次目标的哪些部分:")
        newfile.close()
        os.system("open -e "+full_path)

        #下一次的目标维护在一个temp文件夹中，每个状态维护一个文件
        file_temp=os.path.join("log","temptarget")
        file_temp_file=os.path.join(file_temp,self.choose+".txt")
        if not os.path.exists(file_temp_file):
            newfiletemp=open(file_temp_file, 'w')
            newfiletemp.write("下一次的目标是什么:")
            newfiletemp.close()
        else:
            os.system("open -e "+file_temp_file)
    def why(self,choose):#这个是为了解决为什么做的动力问题
        path='whytodo'
        files=get_all_files_nosort(path)
        for i in files:
            filee=i[8:-4]
            if i[8:-4]==choose:
                os.system("open -e "+i)
if __name__ == "__main__":
    test = randomMachine()
    test.setWeight(test.dic)#添加比例
    
    choose=test.drawing()#根据比例生成
    print(choose)
    test.create()
    test.why(choose)
    
   
