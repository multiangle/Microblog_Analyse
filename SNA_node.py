__author__ = 'multiangle'
class SNA_node():
    def __init__(self, content_dict):

        self.next = []
        self.isHeadNode = True
        self.hasPre = False
        self.preId = None
        self.id = None # 后面会赋值

        item_list = [
            'created_at',
            'created_timestamp',
            'user_name',
            'id',
            'idstr',
            'reposts_count',
            'attitudes_count',
            'comments_count',
            'is_retweeted',
            ]
        content_key = list(content_dict.keys())
        self.data = {}
        for item in item_list:
            if item in content_key:
                self.data[item] = content_dict[item]
        self.id = self.data['id']

        if 'retweeted_status' in content_key: # 处理转载的信息
            retweet_keys = list(content_dict['retweeted_status'].keys())
            self.data['retweeted_status'] = {}
            retweet_item_list = [
                'created_at',
                'created_timestamp',
                'user_name',
                'user_id',
                'id',
                'idstr',
                ]
            for item in retweet_item_list:
                if item in retweet_keys:
                    self.data['retweeted_status'][item] = content_dict['retweeted_status'][item]
            self.hasPre = True
            self.preId = self.data['retweeted_status']['id']
            self.isHeadNode = False

        if 'user' in content_key:  # 处理作者的信息
            user_keys = list(content_dict['user'].keys())
            self.data['user'] = {}
            user_item_list = [
                'blog_num',
                'description',
                'fans_num',
                'name',
                'gender',
                'uid',
                'basic_page'
            ]
            for item in user_item_list:
                if item in user_keys:
                    self.data['user'][item] = content_dict['user'][item]


    def add_Next(self, SNA_node):
        self.next.append(SNA_node)

    def build_Head_Node(retweeted_content):
        node = SNA_node(retweeted_content)
        return node

    def analyse(self):
        result = {}
        result['retweet_num'] = self.next.__len__()
        for msg in self.next : # 递归统计
            msg.analyse()

        if self.next.__len__()==0 : # 统计 转载深度
            result['retweet_depth'] = 0
        else:
            max = 0
            for msg in self.next:
                if max<msg.result['retweet_depth'] :
                    max = msg.result['retweet_depth']
            result['retweet_depth'] = max + 1

        if self.next.__len__()==0 : # 统计 有记录的转载次数
            result['retweet_times'] = 0
        else:
            sum = 0
            for msg in self.next:
                sum += msg.result['retweet_times']
            result['retweet_depth'] = sum

        self.result = result


    def __str__(self):
        return self.data.__str__()