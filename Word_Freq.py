__author__ = 'multiangle'
import time
#对词的统计
class WordFreqItemStatistic():
    def __init__(self,word):
        self.word = word

        self.freq_day = [] # 以天为单位的统计
        self.freq_month = [] # 以月为单位的统计
        self.freq_year = [] # 以年为单位的统计

        self.circle_hour = [0]*24 # 该词在一天24小时中的出现频率
        self.total_freq = 0 # 该词出现的总次数

        self.min_day = -1
        self.max_day = -1
        self.min_month = -1
        self.max_month = -1
        self.min_year = -1
        self.max_year = -1



    def Add_Freq_By_Timestamp(self,timestamp):
        t = time.localtime(timestamp)
        year = t.tm_year
        month = (year-2000)*12 + t.tm_mon
        day = int(timestamp/86400)
        hour = t.tm_hour

        self.__Binary_Find_andAdd(self.freq_day,day)
        self.__Binary_Find_andAdd(self.freq_month,month)
        self.__Binary_Find_andAdd(self.freq_year,year)
        self.circle_hour[hour] += 1
        self.total_freq += 1

        if day<self.min_day:
            self.min_day = day
        if day>self.max_day:
            self.max_day = day
        if month<self.min_month:
            self.min_month = month
        if month>self.max_month:
            self.max_month = month
        if year<self.min_year:
            self.min_year = year
        if year>self.max_year:
            self.max_year = year



    def __Binary_Find_andAdd(self,list,value):
        i = self.__Binary_Find(list,value)
        if i==list.__len__() :
            list.append({'time':value,'freq':1})
        elif list[i]['time']==value :
            list[i]['freq'] += 1
        else:
            list.insert(i,{'time':value,'freq':1})

    def __Binary_Find(self,list,value):
        low = 0
        high = list.__len__()
        while low<high :
            mid = int((low+high)/2)
            if list[mid]['time'] == value :
                return mid
            if list[mid]['time'] < value :
                low = mid + 1
            else:
                high = mid - 1
        return low


def Binary_Find(list,value):
    low = 0
    high = list.__len__()
    i= -1
    while low<high :
        mid = int((low+high)/2)
        if list[mid]['time'] == value :
            i = mid
            break
        if list[mid]['time'] < value :
            low = mid + 1
        else:
            high = mid - 1
    if i<0:
        i = low
    if i==list.__len__() :
        list.append({'time':value,'freq':1})
    elif list[i]['time']==value :
        list[i]['freq'] += 1
    else:
        list.insert(i,{'time':value,'freq':1})

if __name__=='__main__':
    a = []
    Binary_Find(a,1)
    Binary_Find(a,1)
    Binary_Find(a,2)
    Binary_Find(a,4)
    Binary_Find(a,3)
    Binary_Find(a,3)
    Binary_Find(a,5)
    Binary_Find(a,1)
    Binary_Find(a,3)
    print(a)


