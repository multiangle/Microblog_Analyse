__author__ = 'multiangle'
import jieba
import time
import math
from pymongo import MongoClient
import File_Interface as FI
import matplotlib.pyplot as plt
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

    def Trans_Day_Time(self,value):
        t = time.localtime(value*86400)
        return time.strftime('%Y-%m-%d',t)

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

class WordFreqTotalStatistic():
    def __init__(self):
        self.word_statistic = {}
        self.word_list = []
        self.top_asDay = []
        self.top_asMonth = []
        self.top_asYear = []

    def Add_Word_With_Timestamp(self,word,timestamp):
        # 碰到新词，建立词典，扩充分词统计对象
        if word not in self.word_list:
            self.word_list.append(word)
            self.word_statistic[word] = WordFreqItemStatistic(word)
        # 对相应对象加入当前时间戳
        self.word_statistic[word].Add_Freq_By_Timestamp(timestamp)
        # 处理相应时间对象的+1
        [obj_y,obj_m,obj_d] = self.__get_Correspond_Top_Obj(timestamp)
        obj_y.Add_Word(word)
        obj_m.Add_Word(word)
        obj_d.Add_Word(word)

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

    def __get_Correspond_Top_Obj(self,timestamp):
        t = time.localtime(timestamp)
        year = t.tm_year
        month = t.tm_mon
        day = t.tm_mday
        ts_year = int(time.mktime(time.strptime("{y}".format(y=year),"%Y")))
        ts_month = int(time.mktime(time.strptime("{y}-{m}".format(y=year,m=month),"%Y-%m")))
        ts_day = int(time.mktime(time.strptime("{y}-{m}-{d}".format(y=year,m=month,d=day),"%Y-%m-%d")))

        ret = [None,None,None] # year,month ,day obj

        alist = self.top_asYear
        ts = ts_year
        i = self.__Binary_Find(alist,ts)
        if i==alist.__len__():
            alist.append({'time':ts,'obj':TopWordStatic(self.word_list,year)})
            ret[0] = alist[-1]['obj']
        elif alist[i]['time']==ts :
            ret[0] = alist[i]['obj']
        else:
            alist.insert(i,{'time':ts,'obj':TopWordStatic(self.word_list,year)})
            ret[0] = alist[i]['obj']

        alist = self.top_asMonth
        ts = ts_month
        i = self.__Binary_Find(alist,ts)
        if i==alist.__len__():
            alist.append({'time':ts,'obj':TopWordStatic(self.word_list,year,month)})
            ret[1] = alist[-1]['obj']
        elif alist[i]['time']==ts :
            ret[1] = alist[i]['obj']
        else:
            alist.insert(i,{'time':ts,'obj':TopWordStatic(self.word_list,year,month)})
            ret[1] = alist[i]['obj']

        alist = self.top_asDay
        ts = ts_day
        i = self.__Binary_Find(alist,ts)
        if i==alist.__len__():
            alist.append({'time':ts,'obj':TopWordStatic(self.word_list,year,month,day)})
            ret[2] = alist[-1]['obj']
        elif alist[i]['time']==ts :
            ret[2] = alist[i]['obj']
        else:
            alist.insert(i,{'time':ts,'obj':TopWordStatic(self.word_list,year,month,day)})
            ret[2] = alist[i]['obj']

        return ret

class TopWordStatic():
    def __init__(self, word_dict, year, month=-1, day=-1):
        if month<0:
            self.time_str = "{y}".format(y=year)
            self.time_fmt = "%Y"
            self.time_type = 1
        elif day<0:
            self.time_str = "{y}-{m}".format(y=year,m=month)
            self.time_fmt = "%Y-%m"
            self.time_type = 2
        else:
            self.time_str = "{y}-{m}-{d}".format(y=year,m=month,d=day)
            self.time_fmt = "%Y-%m-%d"
            self.time_type = 3
        self.timestamp = int(time.mktime(time.strptime(self.time_str,self.time_fmt)))

        self.dict = word_dict
        self.sorted_list = [] # 排序后的 [dict_index , freq] 对
        self.reflection = [] # 反射表 [dict_index, index of the word in sorted list]
        self.word_id_list = [] # 记录反射表中各行的位置 [dict_index,....,]

    def Add_Word(self,word):
        try:
            dict_index = self.dict.index(word)
        except Exception as e:
            raise RuntimeError("the word not exists in dict")

        if dict_index not in self.word_id_list: #该词之前未出现过
            reflect_id = self.word_id_list.__len__()
            self.word_id_list.append(dict_index)
            self.reflection.append([dict_index,self.sorted_list.__len__()])
            self.sorted_list.append([dict_index,1])
        else:
            reflect_id = self.word_id_list.index(dict_index)
            reflection_pair = self.reflection[reflect_id]
            if reflection_pair[0]!=dict_index:
                raise RuntimeError("the id of word dismatch")
            sorted_pair = self.sorted_list[reflection_pair[1]]
            if sorted_pair[0]!=dict_index:
                raise RuntimeError("the id of word dismatch")
            sorted_pair[1] += 1

            # 找到欲替换的pair
            target = reflection_pair[1]-1
            while target>=0:
                if sorted_pair[1]>self.sorted_list[target][1]:
                    target -= 1
                else:
                    break
            target += 1

            # 交换两组
            ori_pos = reflection_pair[1]
            target_pos = target
            target_word_id = self.sorted_list[target_pos][0]
            self.reflection[reflect_id][1] = target_pos
            self.reflection[self.word_id_list.index(target_word_id)][1] = ori_pos
            temp_pair = self.sorted_list[ori_pos]
            self.sorted_list[ori_pos] = self.sorted_list[target_pos]
            self.sorted_list[target_pos] = temp_pair

    def topN(self,n):
        cut = self.sorted_list[0:n]
        cut = [[self.dict[x[0]],x[1]] for x in cut]
        return cut


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
    # stop_words = FI.load_pickle('./static/stop_words.pkl')
    # wfts = WordFreqTotalStatistic()
    # client = MongoClient('localhost',27017)
    # db = client['microblog_spider']
    # latest_history = db.latest_history
    # count = 0
    # data = []
    # batch_size = 100
    # gone_size = 0
    # while count<10 :
    #     d = latest_history.find().skip(count*batch_size).limit(batch_size)
    #     d = [x for x in d]
    #     data += d
    #     count += 1
    # text = [x['dealed_text']['left_content'][0] for x in data]
    # date = [x['created_timestamp'] for x in data]
    # cutted_text = []
    # for i in range(text.__len__()):
    #     s = jieba.cut(text[i])
    #     for word in s:
    #         if word not in stop_words:
    #             wfts.Add_Word_With_Timestamp(word,date[i])
    #     print('{x} is completed'.format(x = i))
    #
    # FI.save_pickle(wfts,'./static/wfts_1000.pkl')

    wfts = FI.load_pickle('./static/wfts_1000.pkl')
    word_item_list = wfts.word_statistic.values()
    word_item_list = sorted(word_item_list, key=lambda x:x.total_freq,reverse=True)
    # for item in word_item_list:
    #     print('{a}\t{b}'.format(a=item.word,b=item.total_freq))
    # plt.plot([math.log(x.total_freq) for x in word_item_list])
    # plt.show()
    top_asDay = wfts.top_asDay
    for item in top_asDay:
        print('------------------------------')
        print(time.strftime("%Y-%m-%d",time.localtime(item['time'])))
        print(item['obj'].topN(10))


