
import File_Interface as FI
from pyword2vec import Word2Vec
from Word_Freq import WordFreqTotalStatistic
import jieba
import re

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
for line in data:
    count += 1
    line['time'] = base_timestamp + count
for line in data:
    print(line)

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

