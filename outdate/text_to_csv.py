import csv
import re

f = open('booklists.text', 'r', encoding='UTF-8-sig')
data = f.readlines()
f.close()

name = []
author = []
press = []
time = []
price = []
appraise = []

for i in range(len(data)):
    if i % 3 == 0:
        name.append(data[i].rstrip('\n'))
    if i % 3 == 1:
        d = data[i].split('/')
        try:
            price.append(re.search('(\d+.\d+)|\d+', d[-1]).group(0))
        except AttributeError:
            price.append(None)
        try:
            time.append(d[-2].rstrip())
            press.append(d[-3].rstrip())
            author.append(d[:-3])
        except IndexError:
            time.append(None)
            press.append(None)
            author.append(None)
    if i % 3 == 2:
        try:
            appraise.append(int(re.search('\d+', data[i]).group(0)))
        except AttributeError:
            appraise.append(None)
with open('booklist.csv', 'w', encoding='UTF-8') as f2:
    f_csv = csv.writer(f2)
    f_csv.writerows([name, author, press, time, price, appraise])