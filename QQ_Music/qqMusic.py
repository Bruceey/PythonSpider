import requests
from fake_useragent import UserAgent
from datetime import datetime
import pymongo
import logging
import imageio
import pandas as pd
import jieba
from wordcloud import WordCloud, STOPWORDS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


class QQMusic:
    # mongodb配置
    MONGO_URL = 'localhost'
    MONGO_DB = 'qqMusic'
    COLLECTION = 'music'

    def __init__(self):
        self.client = pymongo.MongoClient(QQMusic.MONGO_URL)
        self.collection = self.client[QQMusic.MONGO_DB][QQMusic.COLLECTION]
        self.headers = {
            'User-Agent': UserAgent().random,
        }
        self.comment_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'

        self.params = {'g_tk_new_20200303': '5381',  # 更前一步
                       'g_tk': '5381',  # 更前一步
                       'loginUin': '0',
                       'hostUin': '0',
                       'format': 'json',
                       'inCharset': 'utf8',
                       'outCharset': 'GB2312',
                       'notice': '0',
                       'platform': 'yqq.json',
                       'needNewCode': '0',
                       'cid': '205360772',
                       'reqtype': '2',
                       'biztype': '1',
                       'topid': '102296996',
                       'cmd': '8',
                       'needmusiccrit': '0',
                       'pagenum': '0',
                       'pagesize': '25',
                       'lasthotcommentid': '',
                       'domain': 'qq.com',
                       'ct': '24',
                       'cv': '10101010'
                       }
        # 总评论数
        self.commenttotal = 10000000
        self.cur_page = 0
        self.cur_comment_num = 0

    # f.url = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk_new_20200303=5381&g_tk=5381"

    @staticmethod
    def parse_time(seconds):
        dt = datetime.fromtimestamp(seconds)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def save_to_mongo(self, item: dict):
        self.collection.insert_one(item)

    @staticmethod
    def parse_comment(comment: dict, not_hot_comment=True):
        item = {}
        # 人
        item['name'] = comment.get('nick')
        # 内容
        item['content'] = comment.get('rootcommentcontent') if not_hot_comment else (
                "热评：" + comment.get('rootcommentcontent'))
        middleCommentContentList = comment.get('middlecommentcontent')
        if middleCommentContentList:
            content = ''
            for middleComment in middleCommentContentList:
                content += middleComment.get('subcommentcontent') + ';'
            item['content'] = content

        # 时间
        comment_time = comment.get('time')
        item['comment_time'] = QQMusic.parse_time(float(comment_time))
        # 点赞数
        item['praisenum'] = comment.get('praisenum')
        # 等级徽标
        vipicon = comment.get('vipicon')
        if vipicon:
            item['vipicon'] = vipicon.split('/')[-1].split('.')[0]
        else:
            item['vipicon'] = '未开通会员'
        return item

    def request_comment_url(self, page):
        self.params['pagenum'] = str(page)
        r = requests.get(self.comment_url, params=self.params, headers=self.headers)
        return r.json()

    def run(self):
        while self.cur_comment_num <= self.commenttotal:
            logging.info(f'正在请求第{self.cur_page}页')
            comments_info = self.request_comment_url(self.cur_page)
            self.cur_page += 1
            self.cur_comment_num += 25
            hot_comments = comments_info.get('hot_comment')
            if hot_comments:
                hot_comments = hot_comments.get('commentlist')
                print('增在解析热评。。。')
                for comment in hot_comments:
                    hot_comment_item = self.parse_comment(comment, False)
                    self.save_to_mongo(hot_comment_item)

            comments = comments_info['comment']['commentlist']
            # 总评论数
            if self.cur_page == 0:
                commenttotal = int(comments_info['comment']['commenttotal'])
                self.commenttotal = commenttotal

            print('正在解析评论。。。')
            for comment in comments:
                comment_item = self.parse_comment(comment)
                self.save_to_mongo(comment_item)
        print('抓取完毕')

    def get_stopwords(self):
        stopwords = set(STOPWORDS)
        with open('stopwords.txt') as f:
            for word in f:
                stopwords.add(word.strip())
        stopwords.add('em')
        stopwords.add('e400867')
        stopwords.add('e400408')
        stopwords.add('e400824')
        stopwords.add('e400842')
        stopwords.add('e400832')
        stopwords.add('e400823')
        stopwords.add('首歌')
        stopwords.add('歌')

        return stopwords

    def generate_wordcloud(self):
        df = pd.DataFrame(list(self.collection.find()))
        df.drop('_id', axis=1, inplace=True)
        df = df.drop_duplicates()
        content = '\n'.join(df.content)
        texts = jieba.cut(content)
        texts = ' '.join(texts)
        mask = imageio.imread('周传雄.png')
        stopwords = self.get_stopwords()

        wc = WordCloud(
            font_path='/Users/wangrui/Library/Fonts/阿里巴巴普惠体 M.ttf',
            background_color='white',
            max_words=1000,
            mask=mask,
            stopwords=stopwords,
        )
        wc.generate(texts)
        wc.to_file("《我的心太乱》评论.png")

    def __del__(self):
        self.client.close()
        print('已关闭mongodb客户端.')


if __name__ == '__main__':
    qqMusic = QQMusic()
    # qqMusic.run()
    qqMusic.generate_wordcloud()
    del qqMusic
