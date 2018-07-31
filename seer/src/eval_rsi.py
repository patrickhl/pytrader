import pandas as pd

def eval_rsi(stock_code, rsi_N, rsi_mode):
    # This function calculates the macd (pd.Series) for the stock $code
    # rsi_N: integer
    # stock_code: string
    # rsi_mode: integer, [0,1,2,3] = [open,close,high,low]
    # This function requires *pandas* library

    # read CSV file
    # CSV format:
    # index date open close high low volume code
    try:
        stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')
    except IOError:
        print "[Error]Cannot find file ../data/",stock_code,"/hist_k_day.csv"
        return (1,0)
    else:
        # fetch data according mode
        if (rsi_mode == 0):
            rsi_data = stock_date['open']
        elif (rsi_mode == 1):
            rsi_data = stock_date['close']
        elif (rsi_mode == 2):
            rsi_data = stock_date['high']
        else:
            rsi_data = stock_date['low']

        # calculate RSI
        rsi_size = rsi_data.size
        rsi_rs = [i for i in range(1, rsi_size)]
        rsi_res = [i for i in range(1, rsi_size)]
        rsi_u = [i for i in range(1, rsi_size)]
        rsi_d = [i for i in range(1, rsi_size)]
        avg_g = 0
        avg_l = 0

        for i in range(1, rsi_size):
            if (i == 1):
                rsi_u[i - 1] = 0.0
                rsi_d[i - 1] = 0.0
            else:
                if (rsi_data[i - 1] > rsi_data[i - 2]):
                    rsi_u[i - 1] = rsi_data[i - 1] - rsi_data[i - 2]
                    rsi_d[i - 1] = 0.0
                elif (rsi_data[i - 1] < rsi_data[i - 2]):
                    rsi_u[i - 1] = 0.0
                    rsi_d[i - 1] = rsi_data[i - 2] - rsi_data[i - 1]
                else:
                    rsi_u[i - 1] = 0.0
                    rsi_d[i - 1] = 0.0

        for i in range(1, rsi_size):
            if (i == 1):
                rsi_rs[i - 1] = 0.0
                rsi_res[i - 1] = 0.0
                avg_g = 0.0
                avg_l = 0.0
            else:
                avg_g = avg_g*float(rsi_N-1)/float(rsi_N) + rsi_u[i-1]/float(rsi_N)
                avg_l = avg_l*float(rsi_N-1)/float(rsi_N) + rsi_d[i-1]/float(rsi_N)
                if (avg_l != 0):
                    rsi_rs[i - 1] = avg_g / avg_l;
                    rsi_res[i - 1] = 100 - 100 / (1 + rsi_rs[i - 1])
                else:
                    rsi_rs[i - 1] = 100.0
                    rsi_res[i - 1] = 100.0

        return (0,pd.Series(rsi_res))
