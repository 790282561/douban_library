import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.display.max_rows = None
pd.options.display.max_columns = 10
a = pd.read_csv('booklist2.csv', header=None, na_values=0, encoding='utf-8')

#数据清洗
a = a.drop([1, 3, 5, 7, 9], axis=0)
a = a.T #换轴
a.columns = ['书名', '作者', '出版社', '出版日期', '书价', '评论热度']
a.columns.name = '项目'
a.index.name = '序号'
a['评论热度'] = a['评论热度'].apply(pd.to_numeric, errors='ignore')  #字符转为数值
a['书价'] = a['书价'].apply(pd.to_numeric, errors='coerce')  #字符转为数值
a['出版日期'] = a['出版日期'].apply(pd.to_datetime, errors='coerce')  #字符串转为日期
a['出版日期'] = a['出版日期'].dt.year
a = a.drop_duplicates(['书名']).sort_values(by='评论热度', ascending=False).fillna(0).head(500) #倒序并补全NA值
a.set_index('书名', inplace=True)
a.loc['撒哈拉的故事', '书价'] = 36.5

for i in range(500):
    a['作者'].iloc[i] = a['作者'].iloc[i][1: -1].split(',')[0][1: -1].replace('?', '·')
    if a['作者'].iloc[i] == '':
        a['作者'].iloc[i] = np.nan

a = a.dropna()
for j in range(len(a)):
    a['作者'].iloc[j] = a['作者'].iloc[j].replace(' ', '')
    a['作者'].iloc[j] = a['作者'].iloc[j].split('、')[0]
    if '（' in a['作者'][j]:
        a['作者'].iloc[j] = a['作者'].iloc[j].replace('（', '[')
        a['作者'].iloc[j] = a['作者'].iloc[j].replace('）', ']')
    if '【' in a['作者'][j]:
        a['作者'].iloc[j] = a['作者'].iloc[j].replace('【', '[')
        a['作者'].iloc[j] = a['作者'].iloc[j].replace('】', ']')
    if '(' in a['作者'][j]:
        a['作者'].iloc[j] = a['作者'].iloc[j].replace('(', '[')
        a['作者'].iloc[j] = a['作者'].iloc[j].replace(')', ']')
    if '〔' in a['作者'][j]:
        a['作者'].iloc[j] = a['作者'].iloc[j].replace('〔', '[')
        a['作者'].iloc[j] = a['作者'].iloc[j].replace('〕', ']')

a['作者'].loc['牛虻'] = '[爱尔兰]伏尼契'
a['作者'].loc['冰与火之歌（卷一）'] = '[美]乔治.R.R.马丁'
a['作者'].loc['欧也妮·葛朗台'] = '[法]巴尔扎克'
a['作者'].loc['童年 在人间 我的大学'] = '[苏]高尔基'
a['作者'].loc['艺术的故事'] = '[英]贡布里希'

a.to_csv('writer.csv')