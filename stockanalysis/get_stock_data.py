import multiprocessing
import tushare as ts
import os
import pandas as pd
from stockanalysis import glbdata
import time

class get_stock_data_process (multiprocessing.Process):
    def __init__(self, stock_code,from_date,data_type,nr_of_days,validation):
        multiprocessing.Process.__init__(self)
        self.stock_code = stock_code
        self.from_date = from_date
        self.data_type = data_type
        self.nr_of_days = nr_of_days
        self.validation = validation
    def run(self):
        get_stock_data(self.stock_code,self.from_date,self.data_type,self.nr_of_days,self.validation)

def get_stock_data(stock_code,from_date,data_type,nr_of_days,validation):
    nr_of_try = 0
    if (os.path.exists('../data/' + stock_code) == False):
        os.mkdir('../data/' + stock_code)

    # give a try
    data = ts.get_k_data(stock_code, start=from_date, retry_count=1)

    while (data.empty and nr_of_try<3):
        #print 'retrying for empty data'
        data = ts.get_k_data(stock_code, start=from_date, retry_count=1)
        nr_of_try += 1

    if (data.empty):
        #print 'after 10 tries, still empty'
        glbdata.mutex.acquire()
        validation.append((stock_code, False))
        #current_code = pd.DataFrame(data=[(stock_code, False)], columns=['CODE', 'VALID'])
        #current_validation = pd.read_csv('../data/stock_code_validation.csv',dtype={'CODE':str})
        #current_validation = pd.DataFrame(current_validation, columns=['CODE', 'VALID'])
        #current_validation = current_validation.append(current_code,ignore_index=True)
        #current_validation.to_csv('../data/stock_code_validation.csv')
        print "[Error]Cannot get data for stock: ", stock_code
        #time.sleep(2)
        glbdata.mutex.release()
        return 1
    else:
        date_list = data['date']
        nr_of_try = 0
        while (date_list.size!=nr_of_days and nr_of_try<1):
            #print 'retrying for not enough data',nr_of_try
            data = ts.get_k_data(stock_code, start=from_date, retry_count=1)
            date_list = data['date']
            nr_of_try += 1

        if (date_list.size!=nr_of_days):
            #print 'after 10 tries, still not enough'
            glbdata.mutex.acquire()
            validation.append((stock_code, True))
            #current_code = pd.DataFrame(data=[(stock_code, True)], columns=['CODE', 'VALID'])
            #current_validation = pd.read_csv('../data/stock_code_validation.csv', dtype={'CODE': str})
            #current_validation = pd.DataFrame(current_validation, columns=['CODE', 'VALID'])
            #current_validation = current_validation.append(current_code,ignore_index=True)
            #current_validation.to_csv('../data/stock_code_validation.csv')
            #print "[Warning]Cannot get enough data for stock: ", stock_code
            data.to_csv('../data/' + stock_code + '/hist_k_day.csv')
            #time.sleep(2)
            glbdata.mutex.release()
            return 1
        else:
            glbdata.mutex.acquire()
            validation.append((stock_code, True))
            #current_code = pd.DataFrame(data=[(stock_code, True)], columns=['CODE', 'VALID'])
            #current_validation = pd.read_csv('../data/stock_code_validation.csv', dtype={'CODE': str})
            #current_validation = pd.DataFrame(current_validation, columns=['CODE', 'VALID'])
            #current_validation = current_validation.append(current_code,ignore_index=True)
            #current_validation.to_csv('../data/stock_code_validation.csv')
            data.to_csv('../data/' + stock_code + '/hist_k_day.csv')
            #time.sleep(2)
            glbdata.mutex.release()
            #print "return correctly"
            return 0
