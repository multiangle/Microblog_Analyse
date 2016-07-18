
import File_Interface as FI
from pyword2vec import Word2Vec

path = r'.\static\stop_words.txt'
# file = open(path,'r',encoding='gbk')
file = open(path,'rb')
line = file.readline()
count = 0
s = []
while line:
    try:
        line = file.readline()
        line = line[:-4]
        line = line.decode('gbk')
        s.append(line)
        print(line)
    except:
        print('ERROR')
        count += 1
    finally:
        line = file.readline()
# print(count)

stop_words = FI.load_pickle('.\static\stop_words.pkl')
wdict = FI.load_pickle('.\static\斗破dict_huffman.pkl')
wdict = list(wdict.values())
wdict = sorted(wdict,key=lambda x:x['freq'],reverse=True)
for line in wdict:
    if line['word'] not in stop_words:
        print('{w}\t{pos}\t{huffman}\t{hufflen}\t{f}'
              .format(w=line['word'],
                      pos = line['possibility'],
                      huffman = line['Huffman'],
                      hufflen = line['Huffman'].__len__(),
                      f = line['freq']
        ))