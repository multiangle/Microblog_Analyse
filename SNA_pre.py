__author__ = 'multiangle'

from pymongo import MongoClient
import json
import File_Interface as FI
from SNA_node import SNA_node
import copy

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

# # 去除其他信息
# data = FI.load_pickle('./static/retweeted_data.pkl')
# info_list = []
# for line in data:
#     node = SNA_node(line)
#     info_list.append(node)
# FI.save_pickle(info_list,'./static/info_list.pkl')

# # 建立转载链接关系
# info_list = FI.load_pickle('./static/info_list.pkl')
# info_dict ={}
# for i in info_list:
#     info_dict[i.data['id']] = i
# info_id_list = list(info_dict.keys())
# head_id_list = list(info_dict.keys())
# changed = True
# ite_times = 1
# while changed:
#     changed = False
#     undealed_head = copy.deepcopy(head_id_list)
#     num = undealed_head.__len__()
#     for id in undealed_head:
#         item = info_dict[id]
#         if item.hasPre:
#             changed = True
#             if item.data['retweeted_status']['id'] in info_id_list:
#                 info_dict[item.data['retweeted_status']['id']].add_Next(item)
#                 head_id_list.remove(id)
#             else:
#                 pre_node = SNA_node.build_Head_Node(item.data['retweeted_status'])
#                 pre_node.add_Next(item)
#                 info_dict[pre_node.id] = pre_node
#                 info_id_list.append(pre_node.id)
#                 head_id_list.append(pre_node.id)
#                 head_id_list.remove(id)
#     print(ite_times)
#     ite_times += 1
#     print(head_id_list.__len__())
# FI.save_pickle(info_dict,'./static/dealed_info_list.pkl')

# 统计
data = FI.load_pickle('./static/dealed_info_list.pkl')
id_list = list(data.keys())
for id in id_list:
    data[id].analyse()
FI.save_pickle(data,'./static/analyse_info_list.pkl')







