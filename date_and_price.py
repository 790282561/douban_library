import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.display.max_rows = None
pd.options.display.max_columns = 10
a = pd.read_csv('booklist2.csv', header=None, na_values=0, encoding='utf-8')

#数据清洗
a = a.drop([1, 3, 5, 7, 9], axis=0)
a = a.stack().unstack(0) #换轴
a.columns = ['书名', '作者', '出版社', '出版日期', '书价', '评论热度']
a.columns.name = '项目'
a.index.name = '序号'
a['评论热度'] = a['评论热度'].apply(pd.to_numeric, errors='ignore') #字符转为数值
a['书价'] = a['书价'].apply(pd.to_numeric, errors='coerce') #字符转为数值
a['出版日期'] = a['出版日期'].apply(pd.to_datetime, errors='coerce') #字符串转为日期
a['出版日期'] = a['出版日期'].dt.year
a = a.drop_duplicates(['书名']).sort_values(by='评论热度', ascending=False).fillna(0).head(500) #倒序并补全NA值
a.set_index('书名', inplace=True)
a.loc['撒哈拉的故事', '书价'] = 36.5

df_date = pd.pivot_table(a, index=['出版日期', '书名']).sort_index(by='出版日期').drop([0.0], axis=0)
mean_price = df_date.mean(level = '出版日期')['书价'] #书价-时间
decade_list = [1953.0, 1972, 1979, 1989, 1999, 2009, 2019]
gradient_price = pd.Series(np.gradient(mean_price[decade_list].values), index=decade_list, name='变化率')
gradient_price = gradient_price.reindex(mean_price.index).interpolate()
price_date_results = pd.merge(mean_price, gradient_price, how='inner', left_index=True, right_index=True)
#各年出版量
books_publications = df_date.count(level=0)['书价'].drop([0], axis=0)
books_publications.name = '出版量'

#显式设置
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
plt.rcParams['figure.figsize'] = (10.0, 8.0)

def boos_publications():
    fig, ax = plt.subplots(1, 1)
    ax.bar(books_publications.index, books_publications.values, color='r', label='数量', alpha=0.6)
    plt.ylim([0, 35])
    plt.ylabel('出版量(单位:本)')
    plt.xlabel('时间')
    plt.title('出版量-时间变化曲线.jpg')
    plt.savefig('出版量-时间变化曲线.jpg', dpi=300, bbox_inches='tight')
    plt.show()

def price_and_date():
    #生成图表
    fig, ax = plt.subplots(1, 1)
    ax.plot(price_date_results.index, price_date_results['书价'], label='价格', color='r', alpha=0.6)
    plt.ylim([0, 100])
    plt.ylabel('单位:元')
    plt.xlabel('时间')
    plt.legend(loc=1)

    ax1 = ax.twinx()
    ax1.plot(price_date_results['变化率'], label='变化率', color='b', alpha=0.6)
    plt.ylabel('变化率')
    plt.legend(loc=1, bbox_to_anchor=(1, 0.96))
    plt.title('书价-时间变化曲线')
    plt.savefig('书价-时间变化曲线.jpg', dpi=300, bbox_inches='tight')
    plt.show()

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
    #appraise_and_price()
    #price_and_date()
    boos_publications()

main()