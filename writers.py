import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.display.max_rows = None
pd.options.display.max_columns = 10
a = pd.read_csv('writer.csv', na_values=0, encoding='utf-8')

a = a.set_index(['作者', '书名']).sort_values(by='作者')
best_sellers = a.count(level=0)['书价'].sort_values(ascending=False)
best_sellers = best_sellers[best_sellers.values>6]

#显式设置
plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
plt.rcParams['figure.figsize'] = (10.0, 8.0)

def best_sellers_list():
    fig, ax = plt.subplots(1, 1)
    ax.bar(best_sellers.index, best_sellers.values, color='g', alpha=0.6, width=0.2)
    ax.set_xticklabels(best_sellers.index, rotation=90)

    for x, y in enumerate(best_sellers):
        plt.text(x, y, y, ha='center', va='bottom')

    plt.ylabel('畅销书数量')
    plt.title('热评前500最受欢迎作家')
    plt.savefig('热评前500最受欢迎作家.jpg', dpi=300, bbox_inches='tight')
    plt.show()

best_sellers_list()
