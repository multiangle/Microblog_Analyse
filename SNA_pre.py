__author__ = 'multiangle'

from pymongo import MongoClient
import json
import File_Interface as FI
from SNA_node import SNA_node

### 将转载的内容贴出来
# client = MongoClient('localhost',27017)
# db = client['microblog_spider']
# latest_history = db.latest_history
# retweeted_data = []
# skip = 0
# valid = True
# batch_size = 100
# total_count = 0
# valid_count = 0
# while valid:
#     data = latest_history.find().skip(skip).limit(batch_size)
#     data = [x for x in data]
#     if data.__len__()==0:
#         valid = False
#     skip = skip + batch_size
#     for line in data:
#         if line['is_retweeted']:
#             valid_count += 1
#             retweeted_data.append(line)
#         total_count += 1
#     print("{a}/{b}".format(a=valid_count,b=total_count))
#     if total_count>200000:
#         valid= False
# FI.save_pickle(retweeted_data,'./static/retweeted_data.pkl')

# 去除其他信息
data = FI.load_pickle('./static/retweeted_data.pkl')
info_list = []
for line in data:
    node = SNA_node(line)
    info_list.append(node)




