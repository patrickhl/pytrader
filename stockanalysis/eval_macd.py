import pandas as pd
import os

def eval_macd(stock_code,macd_A,macd_B,macd_C,macd_mode,force_eval):
# This function calculates the macd (pd.Series) for the stock $code
# macd_A: integer
# macd_B: integer
# macd_C: integer
# stock_code: string
# macd_mode: integer, [0,1,2,3] = [open,close,high,low]
# This function requires *pandas* library

# read CSV file
# CSV format:
# index date open close high low volume code
    # use existing value
    if (os.path.exists('../data/' + stock_code + '/macd_res.csv')==True and force_eval == False):
        macd_cur_res = pd.read_csv('../data/' + stock_code + '/macd_res.csv')
        return (0, pd.Series(macd_cur_res['DIF']), pd.Series(macd_cur_res['DEA']))
    # no file
    if (os.path.exists('../data/' + stock_code + '/hist_k_day.csv')==False):
        #print "[Error]Cannot find file ../data/", stock_code, "/hist_k_day.csv"
        return (1, 0, 0)

    stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')

    # fetch data according mode
    if (macd_mode==0):
        macd_data = stock_data['open']
    elif (macd_mode==1):
        macd_data = stock_data['close']
    elif (macd_mode==2):
        macd_data = stock_data['high']
    else:
        macd_data = stock_data['low']

    # calculate MACD
    macd_size = macd_data.size
    macd_ema_a = [i for i in range(1,macd_size)]
    macd_ema_b = [i for i in range(1,macd_size)]
    macd_dif   = [i for i in range(1,macd_size)]
    macd_dea   = [i for i in range(1,macd_size)]

    for i in range(1,macd_size):
        if (i==1):
            macd_ema_a[i-1] = macd_data[i-1]
            macd_ema_b[i-1] = macd_data[i-1]
            macd_dif[i-1]   = macd_ema_a[i-1] - macd_ema_b[i-1]
            macd_dea[i-1]   = 0
        else:
            macd_ema_a[i-1] = macd_data[i-1]*(2/float(macd_A+1)) + macd_ema_a[i-2]*(float(macd_A-1)/float(macd_A+1))
            macd_ema_b[i-1] = macd_data[i-1]*(2/float(macd_B+1)) + macd_ema_b[i-2]*(float(macd_B-1)/float(macd_B+1))
            macd_dif[i-1]   = macd_ema_a[i-1] - macd_ema_b[i-1]
            macd_dea[i-1]   = (macd_ema_a[i-1] - macd_ema_b[i-1])*(2/float(macd_C+1)) + macd_dea[i-2]*(float(macd_C-1)/float(macd_C+1))

    if (os.path.exists('../data/' + stock_code + '/macd_res.csv')==False or force_eval==True):
        macd_res = [macd_dif, macd_dea]
        macd_res_pd = pd.DataFrame(data=map(list, zip(*macd_res)), columns=['DIF', 'DEA'])
        macd_res_pd.to_csv('../data/' + stock_code + '/macd_res.csv')

    return (0, pd.Series(macd_dif),pd.Series(macd_dea))
