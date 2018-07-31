# -*- coding:utf8 -*-
####################################
# Fetch stock k day data from server
# and save (update) it into local
# DB:
# local_db.k_day_collection_######

####################################
# library section and global variable
import tushare as ts
import pymongo as mg
import json as js
import pandas as pd
client = mg.MongoClient('localhost', 27017)
dbg = 0

####################################
# setup variables
stock_code = "000001"
start_date = "2014-01-05"
if_force   = False

####################################
# fetch stock k data from internet server
try:
    stock_data = ts.get_k_data(stock_code, start=start_date, pause=1)
    data_json = js.loads(stock_data.to_json(orient='records'))

    if dbg == 1:
        print stock_data

####################################
# fetch local conf file to check the
# preserved start date

    preserved_start_date = "2014-01-05"

####################################
# Check the start date,
# if same as before, then do nothing,
# if force update or not same, then clean local db
# and insert data fetched above
    local_coll_name = "stock_k_day_collection_"+stock_code
    local_db = client.local_db
    stock_k_day_collection = local_db[local_coll_name]

    if if_force is False:
        stock_k_day_collection.remove()
        stock_k_day_collection.insert_many(data_json, ordered=True)
        save to conf file
    elif start_date != preserved_start_date:
        stock_k_day_collection.remove()
        stock_k_day_collection.insert_many(data_json, ordered=True)
        save
        to
        conf
        file
    else:
        # do nothing

    if dbg == 1:
        fetched_data = stock_k_day_collection.find()
        print pd.DataFrame(list(fetched_data))['high']


except Exception, err:
    print "\033[0;31;m",  # red
    print "[Exception]",
    print "\033[0m",
    print ": update_stock_k_day.py (exception spot 1): info: \t"
    print "stock_code: ", stock_code , "\t",
    print repr(err)
finally:
    client.close()