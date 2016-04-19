import jieba
import File_Interface as FI

# data = FI.load_pickle('demo.pkl')
# user_list = [x['user_name'] for x in data]
# text_list = [x['dealed_text']['left_content'] for x in data]
#
# def remove_sig(l):
#     st_list = ['',',','.','。','，','【','】','？']
#     for i in range(l.__len__())[::-1]:
#         if l[i] in st_list:
#             l.pop(i)
#
# total_word = []
# for line in text_list:
#     res = jieba.cut(line[0],cut_all=True)
#     # print(list(seg_list))
#     res = list(res)
#     remove_sig(res)
#     total_word += res

def word_freq_count():
    pass

total_word = FI.load_pickle('./static/total_word.pkl')
total_word_unique = list(set(total_word))
word_freq = FI.load_pickle('./static/word_freq.pkl')
for i in range(total_word_unique.__len__()):
    if word_freq[i]>=5 :
        print(total_word_unique[i],'\t',word_freq[i])