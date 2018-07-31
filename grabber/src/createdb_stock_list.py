# -*- coding:utf8 -*-
####################################
# Fetch stock list from server
# and save (update) it into local
# DB:
# local_db.stock_list_collection

####################################
# library section and global variable
import tushare as ts
import pymongo as mg
client = mg.MongoClient('localhost', 27017)
dbg = 0

####################################
# fetch stock list from server
# and sort in sequence
full_stock_pd = ts.get_stock_basics()
stock_list_pd = full_stock_pd.index
stock_list_int = []
for j in range(stock_list_pd.size):
    stock_list_int.append(int(stock_list_pd[j]))
stock_list_int.sort()

stock_list_str = []
for j in range(len(stock_list_int)):
    stock_list_str.append(str(stock_list_int[j]).zfill(6))

stock_list_uni = []
for j in range(len(stock_list_str)):
    stock_list_uni.append(unicode(stock_list_str[j], encoding='utf-8'))

if dbg == 1:
    print "\033[0;33;40m",  # yellow
    print "[DBG INFO]",
    print "\033[0m",
    print ": update_stock_list.py (dbg spot 1): data: ", stock_list_uni[0:5]


####################################
# Check local DB and update accordingly
# if cannot find, then insert
# so this keep updating stock list in
# local db
local_db = client.local_db
stock_list_collection = local_db.stock_list_collection
inserted_nr = 0

try:
    for j in range(len(stock_list_uni)):
        if stock_list_collection.find_one({stock_list_uni[j]: "1"}) is None:
            stock_list_collection.insert_one({stock_list_uni[j]: "1"})
            inserted_nr += 1
except Exception, err:
    print "\033[0;31;m",  # red
    print "[Exception]",
    print "\033[0m",
    print ": update_stock_list.py (exception spot 1): info: \t"
    print repr(err)

print "\033[0;32;m",  # green
print "[INFO]",
print "\033[0m",
print ": Updated local stock list: newly inserted: ", inserted_nr
client.close()
