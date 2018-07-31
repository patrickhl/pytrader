import stock_analysis as sa
import pandas as pd
from stock_analysis import glbdata
import os


def eval_strategy1(stock_code,till_date,force_eval):
    hit_date = 0
    hit_code = 0
    risk = 0.0
    weight = 1.0

    # check if the till_date is valid (tradable)
    if (os.path.exists('../data/' + stock_code + '/hist_k_day.csv')==False):
        return 1

    stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')
    stock_data_date = stock_data['date']

    for i in range(stock_data_date.size):
        if (till_date==stock_data_date.get_value(i,'date')):
            hit_date = 1;
            break

    # if today is not tradable, then set weight to 0.0 to decline this stock for today
    if (hit_date==0):
        weight = 0.0
        risk   = 0.0
    else:
        (kdj_status,kdj_k,kdj_d,kdj_j) = sa.eval_kdj(stock_code,3,5,15,force_eval)
        if (kdj_status==1):
            return 1

        (macd_status, macd_dif, macd_dea) = sa.eval_macd(stock_code, 3, 5, 15, 1, force_eval)
        if (macd_status==1):
            return 1

        for i in range(stock_data_date.size):
            # find the date
            if (till_date==stock_data_date.get_value(i,'date')):
                hit_date = 1
                if (kdj_j.iat(i) > kdj_j.iat(i-1) and \
                    kdj_j.iat(i-1) > kdj_j.iat(i-2) and \
                    kdj_j.iat(i)  < kdj_k.iat(i) and \
                    kdj_k.iat(i)  < kdj_d.iat(i) and \
                    macd_dif.iat(i)< macd_dea.iat(i)):

                    risk = 1.0/(macd_dea.iat(i)-macd_dif.iat(i))

                    break
                else:
                    risk = 0.0
                    break
            else:
                continue

    # update existing risk
    for j in range(1, glbdata.risk_list.size / 3):
        if (glbdata.risk_list.get_value(j, 'CODE') == stock_code):
            hit_code = 1
            glbdata.risk_list.set_value(j, 'strategy1', risk)
            break
        else:
            continue
    # add stock in risk list
    if (hit_code == 0):
        new_risk = pd.DataFrame(data=[(stock_code, risk, weight)], columns=['CODE', 'strategy1', 'weight1'])
        if glbdata.mutex.acquire():
            glbdata.risk_list = glbdata.risk_list.append(new_risk, ignore_index=True)
            glbdata.mutex.release()

    return 0
