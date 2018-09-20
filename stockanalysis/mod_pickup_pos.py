import stockanalysis as sa
import pandas as pd
import glbdata
import string

def mod_pickup_pos(max_stock,min_stock,current_date):
    glbdata.risk_list.sort('strategy1',ascending=False)
    # pick up more than max_stock, in case some stocks cannot be picked (missing data on current_date)
    risk_list_topN = glbdata.risk_list.head(2*max_stock+1)
    local_new_position = pd.DataFrame(data=[('000000', 0.0, 0.0)], columns=['CODE', 'PRICE', 'VOL'])
    hitted = 0
    for i in range(1,2*max_stock+1):

        stock_code = risk_list_topN.get_value(i,'CODE')
        stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')
        date_list = stock_data['date']
        price_list = stock_data['close']

        for j in range(date_list.size):
            date = date_list.get_value(j, 'date')

            if (string.atoi(current_date[0:4] + current_date[5:7] + current_date[8:10]) == string.atoi(
                        date[0:4] + date[5:7] + date[8:10])):
                hitted = hitted + 1
                current_price = price_list.get_value(j,'close')

                # calculating vol
                new_position_vol = 100

                new_position_slot = pd.DataFrame(data=[(stock_code, current_price, new_position_vol)], columns=['CODE', 'PRICE', 'VOL'])
                local_new_position = local_new_position.append(new_position_slot, ignore_index=True)
                break
            else:
                continue

        if (hitted==max_stock):
            break


    glbdata.new_position = local_new_position

    return 0
