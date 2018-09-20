import pandas as pd
import glbdata
import string

def rpt_total_capital(current_date):
    total_cap = 0.0
    current_asset = 0.0
    for i in range(1,glbdata.position.size/3):
        stock_code = glbdata.position.get_value(i,'CODE')
        stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')
        date_list = stock_data['date']
        price_list = stock_data['close']

        for j in range(date_list.size):
            date = date_list.get_value(j, 'date')
            if (string.atoi(current_date[0:4] + current_date[5:7] + current_date[8:10]) == string.atoi(
                        date[0:4] + date[5:7] + date[8:10])):
                current_asset = price_list.get_value(j,'close') * float(glbdata.position.get_value(i,'VOL')) * 100.0
                break
            else:
                continue

        total_cap = total_cap + current_asset

    total_cap = total_cap + glbdata.cash

    current_profit_delta = pd.DataFrame(data=[(current_date, total_cap/glbdata.cash_init)], columns=['DATE', 'PROFIT'])
    glbdata.profit_delta = glbdata.profit_delta.append(current_profit_delta, ignore_index=True)
    #print '[INFO] ',current_date, " : Total capital is ", total_cap
    #print 'Position:',glbdata.position
    print '[INFO] Current profit delta is : ', total_cap/glbdata.cash_init


    return 0