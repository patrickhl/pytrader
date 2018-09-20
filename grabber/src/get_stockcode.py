# -*- coding:utf8 -*-
import requests as rq
import re
import os

# Get all stock code for sh and sz
stocklist_html = rq.get('http://quote.eastmoney.com/stocklist.html')
html = stocklist_html.text
#html = unicode(html, "gb2312").encode("utf8")
#print(html[0:100])
all_stock = re.findall('\([0-9]{6}\)</a></li>',html)
#for stock in all_stock:
#    str = stock.encode('ascii')
#    print(str[1:6])

# Store in file
f = open(os.getenv('TRADERHOME')+'/container/puretxt/stock_code.txt','w')
for stock in all_stock:
    ss = stock.encode('ascii')
    f.write(ss[1:7]+'\n')

f.close()

f = open(os.getenv('TRADERHOME')+'/container/puretxt/stock_code.csv','w')
f.write(',CODE\n')
i = 0
for stock in all_stock:
    ss = stock.encode('ascii')
    f.write(str(i)+','+ss[1:7]+'\n')
    i = i+1
f.close()
