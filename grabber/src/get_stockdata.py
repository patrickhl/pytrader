# -*- coding:utf8 -*-
import stock_analysis as sa
import os
import datetime
from stock_analysis import glbdata
import tushare as ts
import pandas as pd
import multiprocessing
import string


if __name__ == '__main__':
    validation = multiprocessing.Manager().list([('000000', False)])
    # Read in stock code
    stock_code_list = pd.read_csv('../data/stock_code.csv')
    i = 1

    #start_date = datetime.date(2014, 1, 5)
    #today = datetime.date.today()
    #diff = today - start_date
    #total_days = diff.days
    start_date = '2014-06-01'
    nr_of_try = 0
    while (nr_of_try<5):
        data = ts.get_k_data('000001', start=start_date, retry_count=3)
        total_days = data['date'].size
        if (nr_of_try<1):
            pre_total_days = total_days
            nr_of_try += 1
        else:
            if (pre_total_days==total_days):
                nr_of_try += 1
                continue
            else:
                break

    if (nr_of_try!=5):
        print "Code 000001 is not stable on date"
    else:
        print "Total ", total_days, " trading days of data"
        process_list = []
        #glbdata.validation.to_csv('../data/stock_code_validation.csv')

        for code in stock_code_list['CODE']:
            if (True):#code>600000 and code<600200):
                if (os.path.exists('../data/'+str(code))==False):
                    os.mkdir('../data/'+str(code))
                #file_name = '../data/'+code+'/'+'basic.txt'
                #fw = open(file_name,'w')

                p = sa.get_stock_data_process(str(code),start_date,0,total_days,validation)
                process_list.append(p)
                p.start()

                #fw.write(data)
                #fw.close()

                if(i%100==0):
                    for p in process_list:
                        p.join()
                    print 'Issued ', i, 'stocks'

                i += 1

        print 'Issued all stocks'
        for p in process_list:
            p.join()

        validation_loc = []
        for i in range(len(validation)):
            validation_loc.append(validation[i])
        validation_list = pd.DataFrame(validation_loc, columns=['CODE','VALID'])

        validation_list.to_csv('../data/stock_code_validation.csv')
        os.system('shutdown -s -t 30')
