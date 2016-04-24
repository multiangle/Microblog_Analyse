import jieba
import File_Interface as FI
from collections import Counter
import math

def word_count(text_list):
    len = text_list.__len__()


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

# total_word = FI.load_pickle('./static/total_word.pkl')
# total_word_unique = list(set(total_word))
# word_freq = FI.load_pickle('./static/word_freq.pkl')
# for i in range(total_word_unique.__len__()):
#     if word_freq[i]>=5 :
#         print(total_word_unique[i],'\t',word_freq[i])

class TrainVecModel():
    def __init__(self,settings):
        self.settings = settings
        self.stop_word = self.get_stop_words()
        self.word_set = {}
        self.dict = []
        self.cutted_text_list = []

    # count the freq of words
    def word_count(self,text_list):

        filtered_word_list = []

        if self.settings.__contains__('cut_all') :
            cut_all = self.settings['cut_all']
        else:
            cut_all = True

        for line in text_list:
            res = jieba.cut(line,cut_all=cut_all)
            res = list(res)
            self.filter_stop_words(res)
            self.cutted_text_list.append(res)
            filtered_word_list += res

        self.word_set = Counter(filtered_word_list)

    def create_vector(self):
        if self.settings.__contains__('dict_size') :
            dict_size = self.settings['dict_size']
        else:
            dict_size = min(1500,self.word_set.__len__())
        standard_word_set = self.word_set.most_common(dict_size)
        standard_word_value = [x[0] for x in standard_word_set]
        standard_word_freq = [x[1] for x in standard_word_set]
        standard_word_freq_sum = sum(standard_word_freq)

        # judge the type of weighting the value in vector
        if self.settings.__contains__('weight_type'):
            if self.settings['weight_type'] in ['BOOL','TF-IWF','TF']:
                weight_type = self.settings['weight_type']
            else:
                weight_type = 'TF-IWF'
        else:
            weight_type = 'TF-IWF'

        vector_list = []
        for line in self.cutted_text_list:
            temp = [0]*dict_size
            if weight_type == 'BOOL' :
                for item in line:
                    try:
                        temp[standard_word_value.index(item)] = 1
                    except:
                        pass
            elif weight_type == 'TF' :
                for item in line:
                    try:
                        temp[standard_word_value.index(item)] += 1
                    except:
                        pass
            elif weight_type == 'TF-IWF' :
                for item in line:
                    try:
                        pos = standard_word_value.index(item)
                        temp[pos] += math.log(standard_word_freq_sum/standard_word_freq[pos])**2
                    except:
                        pass
            vector_list.append(temp)
        self.vector = vector_list

    # drop the words in stop words list
    def filter_stop_words(self,word_list):
        for i in range(word_list.__len__())[::-1]:

            if word_list[i] in self.stop_word:
                word_list.pop(i)
                continue

            try:
                int(word_list[i])
                word_list.pop(i)
                continue
            except:
                pass

    def get_stop_words(self):
        ret = []
        ret = FI.load_pickle('./static/stop_words.pkl')
        return ret

if __name__ == '__main__' :
    tvm = TrainVecModel({'weight_type':'TF'})
    data = FI.load_pickle('./static/demo.pkl')
    data = [x['dealed_text']['left_content'][0] for x in data]
    tvm.word_count(data)
    tvm.create_vector()
    x = tvm.vector
    FI.save_pickle(x,'./static/vector_test.pkl')
    for i in x:
        print(i)




