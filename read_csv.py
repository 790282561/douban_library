import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.display.max_rows = 10
a = pd.read_csv('booklist.csv', error_bad_lines=False, header=None, na_values=0, encoding='utf-8')
#数据清洗
a = a.stack().unstack(0) #换轴
a.columns = ['书名', '作者', '出版社', '书价', '评论热度']
a.columns.name = '项目'
a.index.name = '序号'
a['评论热度'] = a['评论热度'].apply(pd.to_numeric, errors='ignore') #字符转为数值
a['书价'] = a['书价'].apply(pd.to_numeric, errors='coerce') #字符转为数值
a = a.drop_duplicates(['书名']).sort_values(by='评论热度', ascending=False).fillna(0).head(50) #倒序并补全NA值
a.set_index('书名', inplace=True)
a.loc['撒哈拉的故事', '书价'] = 36.5

'''
#数据透视
#透视书名和评论热度
df_appraise = pd.pivot_table(a, values=['评论热度'], index=['书名']).sort_values(ascending=False, by='评论热度')
#用df的书名索引透视书价
df_price = pd.pivot_table(a, values=['书价'], index=df_appraise.index)
'''

#显式设置
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
plt.rcParams['figure.figsize'] = (10.0, 8.0)

def appraise_and_price():
    #生成图表
    fig, ax = plt.subplots(1, 1)
    ax.bar(a.index, a['评论热度'], color='g', label='人数', alpha=0.6)
    ax.set_xticklabels(a.index, rotation=90)
    plt.ylim([0, 500000]) #y轴左量程
    plt.ylabel('单位:人')
    plt.xlabel('书名')
    plt.legend(loc=1)

    ax1 = ax.twinx()
    ax1.plot(a['书价'] ,label='价格', color='k')
    plt.ylim([0, 75]) #y轴右量程
    plt.ylabel('单位:￥')
    plt.title('畅销书热评数量与书价')

    plt.legend(loc=1, bbox_to_anchor=(1, 0.96))
    #保存输出
    plt.savefig('畅销书热评数量与书价.jpg', dpi=300, bbox_inches = 'tight')
    plt.show()

def main():
    appraise_and_price()

main()