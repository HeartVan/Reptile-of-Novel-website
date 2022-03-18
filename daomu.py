#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from tkinter import *
import tkinter as tk   #用户界面
from bs4 import BeautifulSoup #解析数据
import requests  #模仿浏览器发起请求
import xlwt      #excel表格存储
import wordcloud  #词云设计
from wordcloud import ImageColorGenerator
import jieba      #分词
import matplotlib.pyplot as plt  #云图弹窗
import matplotlib as mpl
import numpy as np    #数学函数库

import re # 正则表达式库
import collections # 词频统计库
from PIL import Image # 图像处理库
import pymysql   #数据库


#用户界面设计
class application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.create()
    def create(self):
        self.label1 = tk.Label(root, text='网址', relief=GROOVE).grid(row=0, column=0)
        self.en = tk.Entry(root)
        self.en.grid(row=0, column=3)

        self.label = tk.Label(root, text='响应标题', relief=GROOVE).grid(row=1, column=0)

        self.t1 = tk.Text(root, height=25, width=50, highlightcolor='red')
        self.t1.grid(row=1, column=1, sticky='n', columnspan=4)

        self.but1 = tk.Button(root, text='爬取', command=self.beg_title)
        self.but1['bg'] = 'gray'
        self.but1.grid(row=2, column=2, sticky='n')

        self.but2 = tk.Button(root, text='存取', command=self.beg_save)
        self.but2['bg'] = 'gray'
        self.but2.grid(row=2, column=3, sticky='n')

        self.but3 = tk.Button(root, text='词云', command=self.beg_select)
        self.but3['bg'] = 'gray'
        self.but3.grid(row=2, column=4, sticky='n')

        self.but4 = tk.Button(root, text='柱形图', command=self.beg_bing)
        self.but4['bg'] = 'gray'
        self.but4.grid(row=2, column=5, sticky='n')


    def entry_get(self):
        url = self.en.get()
        #print(url)
        return url

    #网页数据爬写小说标题
    def beg_title(self):
        temp = []
        #模仿浏览器并发出请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
        }
        #url = 'http://www.xbiquke.com/bq/2/2336/'
        url = self.entry_get()
        html = requests.get(url=url, headers=headers)
        html.encoding = 'UTF-8'
        page_text = html.text
        # 在首页中解析出章节的标题和详情页的URL
        soup = BeautifulSoup(page_text, 'lxml')
        #解析数据存放在列表里
        li_list = soup.select('.box_con > div > dl > dd')
        for li in li_list:
            title = li.a.string
            temp.append(title)
            self.t1.insert(INSERT, title + '\n')
            print(title, '爬取成功!!!!')
        return temp
    #爬取目录及每章具体内容
    def beg_save(self):
        temp = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
        }
        url = 'http://www.xbiquke.com/bq/2/2336/'
        html = requests.get(url=url, headers=headers)
        html.encoding = 'UTF-8'
        page_text = html.text
        # 在首页中解析出章节的标题和详情页的URL
        soup = BeautifulSoup(page_text, 'lxml')
        li_list = soup.select('.box_con > div > dl > dd')
        '''for li in li_list:
            title = li.a.string
            print(title)'''
        def creat_excel(list):
            # 新建excel
            i = 0
            j = 0
            book = xlwt.Workbook(encoding="utf-8", style_compression=0)
            sheet = book.add_sheet('盗墓', cell_overwrite_ok=True)
            for z in list:
                sheet.write(i, j, z)
                i = i + 1
            book.save('盗墓.xls')
        #存储至txt文本文档
        fp = open('./daomu.txt', 'w', encoding='utf-8')
        for li in li_list:
            title = li.a.string
            temp.append(title)
            detail_url = 'http://www.xbiquke.com/bq/2/2336/' + li.a['href']
            text1 = requests.get(url=detail_url, headers=headers)
            text1.encoding = 'UTF-8'
            text = text1.text
            soup1 = BeautifulSoup(text, 'lxml')
            detail_soup1 = soup1.find('div', id='content')
            content = detail_soup1.text
            fp.write(title + ':' + content + '\n')
            print(title, '爬取成功!!!!')
        #存储至excel文件
        creat_excel(temp)

    def beg_select(self):

        # 读取文件

        fn = open('daomu.txt', 'rt',encoding='utf-8')  # 打开文件

        string_data = fn.read()  # 读出整个文件

        fn.close()  # 关闭文件

          # 文本预处理

        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式

        string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

          # 文本分词

        seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词

        object_list = []

        remove_words = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'。', u' ', u'、', u'中', u'在',
                        u'了',
                                         u'通常', u'如果', u'我们', u'需要']  # 自定义去除词库


        for word in seg_list_exact:  # 循环读出每个分词

            if word not in remove_words:  # 如果不在去除词库中

                object_list.append(word)  # 分词追加到列表

          # 词频统计

        word_counts = collections.Counter(object_list)  # 对分词做词频统计

        word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词

        print(word_counts_top10)  # 输出检查

          # 词频展示

        mask = np.array(Image.open('aaa.jpg'))  # 定义词频背景

        wc = wordcloud.WordCloud(

        font_path = 'simhei.ttf',  # 设置字体格式

        mask = mask,  # 设置背景图

        max_words = 1000,  # 最多显示词数

        min_font_size = 10  # 字体最大值
        )


        wc.generate_from_frequencies(word_counts)  # 从字典生成词云

        image_colors = ImageColorGenerator(mask)  # 从背景图建立颜色方案

        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案

        plt.imshow(wc)  # 显示词云

        plt.axis('off')  # 关闭坐标轴

        plt.show()  # 显示图像


    def beg_bing(self):

        #柱状图数据处理
        json = open("daomu.txt", "r", encoding="utf-8").read()
        # jieba.lcut精确模式，饭后json文件中分词后的列表变量
        words = jieba.lcut(json)
        # 定义一个字典
        counts = {}
        data = []
        num = []
        # 遍历words列表的分词 并计数
        for word in words:
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word, 0) + 1
        # items()返回可遍历的元组数组
        items = list(counts.items())
        # sort()排序函数
        # lambda匿名函数
        items.sort(key=lambda x: x[1], reverse=True)


        for i in range(10):
            word, count = items[i]
            data.append(word)
            num.append(count)
            # format函数字符串格式化
            print("{0:<10}{1:<5}".format(word, count))
        print(items)

        # 进行数据库存储数据
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", database="sanguo", charset="utf8")
        cs = conn.cursor()
        cs.execute("use sanguo;")
        cs.execute("DROP TABLE IF EXISTS daomu")
        cs.execute("create table daomu(name char(20),num char(20))character set utf8;")
        for i in items:
            cs.execute("insert into daomu(name,num) values('{name}','{num}')" .format(name=i[0],num=i[1]))
        cs.execute('select * from daomu')
        a = cs.fetchall()
        print(a)
        cs.close()
        conn.commit()
        conn.close()





        #柱状图的显示

        mpl.rcParams['font.sans-serif'] = ['SimHei']  # X 轴可以显示中文
        mpl.rcParams['axes.unicode_minus'] = False  # X 轴可以显示中文

        plt.figure(figsize=(8, 6))
        plt.bar([i for i in range(10)], align='center', label="词频", color='yellow', edgecolor='r',height=num)

        plt.legend()
        plt.xlabel('词名')
        plt.ylabel('词频')

        # 设置x轴刻度标签
        plt.xticks(np.arange(0, 10), [str(data[i]) for i in range(10)])

        plt.title('词频图')

        plt.show()
#主函数
root = tk.Tk()
root.title('title')
app = application(master = root)
app.mainloop()