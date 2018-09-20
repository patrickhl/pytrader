import pandas as pd
import os
def eval_kdj(stock_code,kdj_N,kdj_M1,kdj_M2,force_eval):
# This function calculates $N period KDJ index
# kdj_N/M1/M2: integer, period
# read CSV file
# CSV format:
# index date open close high low volume code
    # use existing value
    if (os.path.exists('../data/' + stock_code + '/kdj_res.csv') and not force_eval):
        kdj_cur_res = pd.read_csv('../data/' + stock_code + '/kdj_res.csv')
        return (0, pd.Series(kdj_cur_res['K']), pd.Series(kdj_cur_res['D']), pd.Series(kdj_cur_res['J']))

    if (not os.path.exists('../data/' + stock_code + '/hist_k_day.csv')):
        #print "[Error]Cannot find file ../data/", stock_code, "/hist_k_day.csv"
        return (1, 0, 0, 0)

    stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')

    # fetch data according mode
    kdj_o = stock_data['open']
    kdj_c = stock_data['close']
    kdj_h = stock_data['high']
    kdj_l = stock_data['low']

    # calculate KDJ
    kdj_size = kdj_o.size
    kdj_rsv = [i for i in range(1,kdj_size)]
    kdj_k = [i for i in range(1,kdj_size)]
    kdj_d = [i for i in range(1,kdj_size)]
    kdj_j = [i for i in range(1,kdj_size)]


    for i in range(1, kdj_size):
        if (i==1):
            kdj_rsv[i-1] = 50.0
            kdj_k[i-1] = 0.0
            kdj_d[i-1] = 0.0
            kdj_j[i-1] = kdj_k[i-1]*3.0 - kdj_d[i-1]*2.0
        elif (1<i and i<kdj_N):
            if ((max(kdj_h[0:i])-min(kdj_l[0:i]))!=0):
                kdj_rsv[i-1] = (kdj_c[i-1]-min(kdj_l[0:i]))/(max(kdj_h[0:i])-min(kdj_l[0:i]))*100.0
            else:
                kdj_rsv[i-1] = 50.0
            kdj_k[i-1] = kdj_k[i-2]*float(kdj_M1-1)/float(kdj_M1) + kdj_rsv[i-1]/float(kdj_M1)
            kdj_d[i-1] = kdj_d[i-2]*float(kdj_M2-1)/float(kdj_M2) + kdj_k[i-1]/float(kdj_M2)
            kdj_j[i-1] = kdj_k[i-1]*3.0 - kdj_d[i-1]*2.0
        else:
            if ((max(kdj_h[i-kdj_N:i])-min(kdj_l[i-kdj_N:i]))!=0):
                kdj_rsv[i-1] = (kdj_c[i-1]-min(kdj_l[i-kdj_N:i]))/(max(kdj_h[i-kdj_N:i])-min(kdj_l[i-kdj_N:i]))*100.0
            else:
                kdj_rsv[i-1] = 50.0
            kdj_k[i-1] = kdj_k[i-2]*float(kdj_M1-1)/float(kdj_M1) + kdj_rsv[i-1]/float(kdj_M1)
            kdj_d[i-1] = kdj_d[i-2]*float(kdj_M2-1)/float(kdj_M2) + kdj_k[i-1]/float(kdj_M2)
            kdj_j[i-1] = kdj_k[i-1]*3.0 - kdj_d[i-1]*2.0


    if (not os.path.exists('../data/' + stock_code + '/kdj_res.csv') or force_eval):
        kdj_res = [kdj_k,kdj_d,kdj_j]
        kdj_res_pd = pd.DataFrame(data=map(list, zip(*kdj_res)), columns=['K', 'D', 'J'])
        kdj_res_pd.to_csv('../data/' + stock_code + '/kdj_res.csv')


    return (0,pd.Series(kdj_k),pd.Series(kdj_d),pd.Series(kdj_j))
