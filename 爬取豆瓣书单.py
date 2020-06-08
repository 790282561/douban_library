#确定技术实现方法
#获取豆瓣读书网页
#从豆瓣页面获取书店那分类，返回列表，作为下一步爬取的依据
#爬取书单名称、简介、作者，并按照评论数量排名
#保存到txt文件

import requests
from lxml import etree
from threading import Thread
import time

def get_bookclass(url, headers, s):
    try:
        bookclass_results = s.get(url, headers=headers)
        print(bookclass_results.text)
        if bookclass_results.status_code == 200:
            bookclass = r_class.xpath('//table[@class="tagCol"]//td/a/@href')
            return bookclass
    except:
        print('爬取失败')

def get_booklist(book_tag, headers, s):
    for i in range(6):
        bookclass_search = s.get('https://book.douban.com'+book_tag+'?start='+str(i*20), headers=headers)
        page = etree.HTML(bookclass_search.text)
        names = page.xpath('//div[@class="info"]/h2/a/@title')
        for name in names:
            name.strip()
            with open('doubanbooklists.text', 'a', encoding='utf-8') as f:
                f.write(name)
        appraises = page.xpath('//div[@class="info"]//span[@class="pl"]/text()')
        for appraise in appraises:
            appraise.strip()
            with open('doubanbooklists.text', 'a', encoding='utf-8') as f:
                f.write(appraise)
        authers = page.xpath('//div[@class="info"]/div[@class="pub"]/text()')
        for auther in authers:
            auther.strip()
            with open('doubanbooklists.text', 'a', encoding='utf-8') as f:
                f.write(auther)
                f.write('-'*20)
        print('{}第{}页爬取完毕'.format(book_tag, i))
        time.time(1)

def main():
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    headers = {'Connection': 'keep-alive',
               'Cookie': 'll="108288"; bid=dMyTI0lPzp4; _vwo_uuid_v2=D372113324ED23988E571D7F26557DE61|9ca6f10837dc28c0510e8fdc77da1d4a; douban-fav-remind=1; __utmv=30149280.8970; gr_user_id=7ba93b69-a386-423c-b811-d35fe7fbf0a9; __yadk_uid=eXxGaxO2do4Z3H9YaYzIjFisCojPbnDc; viewed="30247662_27138747"; __utma=30149280.1947401256.1547913154.1561385103.1561870380.6; __utmc=30149280; __utmz=30149280.1561870380.6.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; gr_cs1_f5c1adde-f6cb-4ae9-be49-ae3416091a35=user_id%3A0; __utma=81379588.1339520277.1558747692.1561385117.1561870414.3; __utmc=81379588; __utmz=81379588.1561870414.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1561870421%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; ap_v=0,6.0; ct=y; __utmb=30149280.22.10.1561870380; __utmb=81379588.21.10.1561870414; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=ff3ee197-60be-4b10-ad69-e1f869036e22; gr_cs1_ff3ee197-60be-4b10-ad69-e1f869036e22=user_id%3A0; _pk_id.100001.3ac3=b28b41fee9c151a0.1558747694.3.1561872395.1561386437.; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_ff3ee197-60be-4b10-ad69-e1f869036e22=true; dbcl2="89703883:gzJwV38thh0"',
               'Host': 'book.douban.com',
               'Referer': 'https://accounts.douban.com/passport/login?source=book',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               }
    s = requests.Session()
    bookclass = get_bookclass(url, headers, s)
    print(bookclass)
    for book_tag in bookclass:
        print(book_tag)
        t = Thread(target=get_booklist, args=(book_tag, headers, s,))
        t.start()

main()
