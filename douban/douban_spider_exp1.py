# -*- coding:utf-8 -*-

import os
import requests
import time
from bs4 import BeautifulSoup


class DouBanouseSpider(object):

    """
    抓取豆瓣小组房源信息

     Attributes:
        key_word: 房源标题关键字
        page_num: 每个小组的抓取页数
        group_list: 豆瓣小组列表
        index_url: 豆瓣小组列表链接
        data: 存放抓取结果
    """
    def __init__(self, key_word, page_num):
        self.key_word = key_word
        self.page_num = page_num
        self.group_list = ['shanghaizufang', 'homeatshanghai', '383972', 'shzf', '251101']
        self.index_url = [os.path.join('https://www.douban.com/group', i, 'discussion') for i in self.group_list]
        self.data = {}
        print('豆瓣房源爬虫准备就绪, 开始爬取数据...')

    def get_url_content(self, url):
        """
        根据 url 抓取页面数据

        Args:
            url: 豆瓣小组链接
        """
        try:
            time.sleep(1)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            title_list = soup('td', class_='title')
            for tl in title_list:
                if self.key_word in tl.a.attrs['title']:
                    self.data[tl.a.attrs['title']] = tl.a.attrs['href']
            next_page = soup('span', class_='next')
            if next_page:
                next_url = next_page[0].link.attrs['href']
                end_title = next_url.split('=')[1]
                if int(end_title) < (self.page_num * 25):
                    self.get_url_content(url)
        except Exception as e:
            print('抓取过程报错：%s' % e)

    def start_spider(self):
        """
        爬虫入口
        """
        for i in self.index_url:
            self.get_url_content(i)
        for k, v in self.data.items():
            print('标题：%s, 链接地址：%s'%(k,v))


def main():
    """
    主函数
    """
    print("""
            ###############################
                豆瓣房源小组爬虫
                Author: Abnerzhao
                Version: 0.0.1
                Date: 2018-04-04
            ###############################
        """)
    key_word = input('请输入找房关键字：')
    page_num = input('请输入抓取页面数：')
    if not key_word:
        key_word = '1号线'
    if not page_num:
        page_num = 5
    house_spider = DouBanouseSpider(key_word, int(page_num))
    house_spider.start_spider()
    print('豆瓣房源爬虫爬取结束...')


if __name__ == '__main__':
    main()
