
import File_Interface as FI
from pyword2vec import Word2Vec
from Word_Freq import WordFreqTotalStatistic
import jieba
import re
import matplotlib.pyplot as plt
from pymongo import MongoClient
import json

path = r'.\static\stop_words.txt'

def read_text_to_list(path,encoding='gbk'):
    file = open(path,'rb')
    line = file.readline()
    err_count = 0
    s=[]
    while line:
        try:
            line = line[:-2]
            line = line.decode(encoding=encoding)
            s.append(line)
        except:
            err_count += 1
        finally:
            line = file.readline()
    return s

def read_HongLouMeng():
    path = r'E:\multiangle\E-BOOK\KINDLE自带\10中国古典小说名著百部\0104《红楼梦》作者：曹雪芹\0104《红楼梦》作者：曹雪芹 - 副本.txt'
    s = read_text_to_list(path)
    pattern = r'第.+?回'
    content_by_chap = []
    content_by_chap.append({})
    current_chap = content_by_chap[-1]
    current_chap['text'] = []
    content_by_chap.append(current_chap)
    for line in s:
        if line.__len__()>1:
            if re.match(pattern,line):
                # print(line)
                content_by_chap.append({})
                current_chap = content_by_chap[-1]
                current_chap['text'] = []
                current_chap['title'] = line
            else:
                # print(line)
                current_chap['text'].append(line[2:])
    fintal_content = []
    for chap in content_by_chap:
        key = chap.keys()
        if 'title' in key and 'text' in key:
            fintal_content.append(chap)
    return fintal_content

data = read_HongLouMeng()
base_timestamp = 1468937028
count = 0
client = MongoClient('localhost',27017)
db_fiction = client['fiction']

c_honglou = db_fiction.HongLouMeng
print(db_fiction.collection_names())
for line in data:
    count += 1
    line['time'] = base_timestamp + count * 86400
    # print(line)
    # c_honglou.insert(line)

res = list(c_honglou.find())
print(res.__len__())


# wfts = WordFreqTotalStatistic()
# count = 0
# for line in data:
#     count += 1
#     print(count)
#     timestamp = line['time']
#     t = line['text']
#     for x in t:
#         s = list(jieba.cut(x))
#         wfts.Add_Sentence_With_Timestamp(s,timestamp)
#     # print(t)
# FI.save_pickle(wfts,'.\static\HongLouMeng_wfts')

# # 绘制各个关键词各回的出现频率
# wfts = FI.load_pickle('.\static\HongLouMeng_wfts')
# wso = wfts.word_statistic
# ws = wso.values()
# ws = sorted(ws,key=lambda x:x.total_freq,reverse=True)
# # for word in ws:
# #     print('{a}\t{b}'.format(a = word.word,b=word.total_freq))
# freq_day_dict_list = wso['大观园'].freq_day
# frq_list = [x for x in freq_day_dict_list]
# frq = [x['freq'] for x in frq_list]
# tm = [x['time'] for x in frq_list]
# tm = [x-min(tm)+1 for x in tm]
# print(frq_list)
# plt.plot(tm,frq)
# plt.show()


# stop_words = FI.load_pickle('.\static\stop_words.pkl')
# wdict = FI.load_pickle('.\static\斗破dict_huffman.pkl')
# wdict = list(wdict.values())
# wdict = sorted(wdict,key=lambda x:x['freq'],reverse=True)
# for line in wdict:
#     if line['word'] not in stop_words:
#         print('{w}\t{pos}\t{huffman}\t{hufflen}\t{f}'
#               .format(w=line['word'],
#                       pos = line['possibility'],
#                       huffman = line['Huffman'],
#                       hufflen = line['Huffman'].__len__(),
#                       f = line['freq']
#         ))

