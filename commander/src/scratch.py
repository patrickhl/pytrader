# -*- coding:utf8 -*-
import tushare as ts
import stock_analysis as sa
from stock_analysis import glbdata
import pandas as pd
import string
import sys
import time
import datetime
import multiprocessing




# Get current Tushare version
#print('Current Tushare version : ' + ts.__version__)

debug = 1

# Eval MACD
#rsi_res5 = sa.eval_rsi('166105',5,1)
#print(plt.figure())
#print(rsi_res5.plot())
#print(plt.show())

if (debug==1):
    start = time.clock()

    #data = [['000','001','002'],[True,False,True]]
    data = []
    data.append(['000', True])
    data.append(['001',False])
    data.append(['002',True])
    data.append(['003',False])
    print data[1]
    print len(data)
    data_pd = pd.DataFrame(data, columns=['CODE','VALID'])
    print data_pd
    #sa.mod_schedule(10,5,'2017-04-01')

    end = time.clock()
    print "Cost time: ",end-start
else:
    #stock_data = ts.get_realtime_quotes('166105')
    #print stock_data.get_value(0,'date')
    sa.eval_strategy1('601857', '2016-01-04')
    print glbdata.risk_list

    #stock_data = ts.get_realtime_quotes('166105')
    #print stock_data.get_value(0,'price')

    print "before calling function"
    print glbdata.position
    print glbdata.cash
    #print glbdata.position.size

    print "calling buy function"
    sa.mod_trading('601857', 'buy_wp', 10.0, 0.961, 0.05)
    sa.mod_trading('600009', 'buy_wp', 10.0, 0.961, 0.05)

    print "after calling buy function"
    print glbdata.position
    print glbdata.cash
    #print glbdata.position.size

    print "calling sell function"
    sa.mod_trading('600009', 'sell_wp', 5.0, 0.961, 0.05)

    print "after calling sell function"
    print glbdata.position
    print glbdata.cash
    #glbdata.position.set_value(1,'PRICE',100.0)
    #print "price = ", glbdata.position.get_value(1,'PRICE')
    #print "index = ", glbdata.position.CODE=='000000'
    #glbdata.new_position = glbdata.new_position.append(glbdata.new_position1,ignore_index=True)
    #glbdata.new_position = glbdata.new_position.append(glbdata.new_position2,ignore_index=True)
    #sa.mod_update_pos()
    #print "after calling update_pos function"
    #print glbdata.position
    #print glbdata.cash