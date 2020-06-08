import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.display.max_rows = None
pd.options.display.max_columns = 10
a = pd.read_csv('booklist.csv', header=None, na_values=0, encoding='utf-8')

#数据清洗
a = a.drop([1, 3, 5, 7, 9], axis=0)
a = a.stack().unstack(0) #换轴
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

publishing_df = pd.pivot_table(a, index=['出版社', '书名'])
publishing_num = publishing_df.count(level=0).sort_values(by='评论热度', ascending=False)['评论热度']
main_publishing = publishing_num[publishing_num.values > 9]
other_publising = 500 - publishing_num[publishing_num.values > 9].sum()
main_publishing['其他'] = other_publising
#平均评论热度
publishing_appraise = publishing_df.loc[main_publishing.index[:-1]].mean(level=0).sort_values(by='评论热度', ascending=False)

#显式设置
plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
plt.rcParams['figure.figsize'] = (10.0, 8.0)

def publishing_mean_appraise():
    fig, ax = plt.subplots(1, 1)
    ax.bar(publishing_appraise.index, publishing_appraise['评论热度'], color='orange', alpha=0.6, width=0.2)
    ax.set_xticklabels(publishing_appraise.index, rotation=90)
    for x, y in enumerate(publishing_appraise['评论热度']):
        plt.text(x, y, int(y), ha='center', va='bottom')
    plt.ylabel('平均评论次数:人次')
    plt.title('出版社平均评论热度排行')
    plt.savefig('出版社平均评论热度排行.jpg', dpi=300, bbox_inches='tight')
    plt.show()

def publishing_houses_accounts():
    fig, ax = plt.subplots(1, 1)
    ax.pie(main_publishing.values, labels=main_publishing.index, autopct='%1.1f%%', shadow=False)
    plt.axis('equal')
    plt.title('评论数量前500图书的出版社占比')
    plt.savefig('评论数量前500图书的出版社占比.jpg', dpi=300, bbox_inches='tight')

def main():
    publishing_mean_appraise()
    #publishing_houses_accounts()

main()