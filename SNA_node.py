__author__ = 'multiangle'
class SNA_node():
    def __init__(self, content_dict):
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
        if 'retweeted_status' in content_key:
            retweet_keys = list(content_dict['retweeted_status'].keys())
            self.data['retweeted_status'] = {}
            retweet_item_list = [
                'created_at',
                'user_name',
                'user_id',
                'created_timestamp',
                'id',
                'idstr',
                ]
            for item in retweet_item_list:
                if item in retweet_keys:
                    self.data['retweeted_status'][item] = content_dict['retweeted_status'][item]
        if 'user' in content_key:
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