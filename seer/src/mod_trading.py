import tushare as ts
import pandas as pd
import glbdata
import string
def mod_trading(stock_code, op, vol, price, alpha,current_date):
    # stock_code: string 'xxxxxxx'
    # op: string, "sell", "buy"
    # vol: integer, unit in lot
    # price: floating
    # alpha: floating, if current price can not sell/buy, allow how much of adjustment on current price
    # for sell (buy) op, price goes down (up)

    # get current price
    #stock_data = ts.get_realtime_quotes(stock_code)
    stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')
    date_list  = stock_data['date']
    price_list = stock_data['close']
    current_price = 0.0
    for i in range(date_list.size):
        date = date_list.get_value(i,'date')
        if (string.atoi(current_date[0:4]+current_date[5:7]+current_date[8:10]) <= string.atoi(date[0:4]+date[5:7]+date[8:10])):
            current_price = price_list.get_value(i,'close')
            break


    if (current_price==0.0):
        print "[Error] Current price of "+stock_code+"is 0.0"
        return 1

    op_status = 0

    if (op=='sell_wp'):
        # sell with price
        while op_status!=1:
            for i in range(1, glbdata.position.size / 3):
                if (glbdata.position.get_value(i,'CODE')==stock_code):
                    old_vol = glbdata.position.get_value(i, 'VOL')
                    if (old_vol>vol):
                        # sell part of the position
                        glbdata.position.set_value(i, 'VOL', (old_vol-vol))
                        if (price == 0.0):
                            # use current price
                            glbdata.cash = glbdata.cash + float(vol) * 100.0 * current_price
                        else:
                            glbdata.cash = glbdata.cash + float(vol) * 100.0 * price
                    else:
                        print "Error at sell_wp mod_trading.py"
                    break
            op_status = 1
        return 0
    elif (op=='buy_wp'):
        # buy with price
        buy_new = 1
        while op_status!=1:
            for i in range(1, glbdata.position.size / 3):
                if (glbdata.position.get_value(i, 'CODE') == stock_code):
                    buy_new = 0
                    old_vol = glbdata.position.get_value(i, 'VOL')
                    old_price = glbdata.position.get_value(i, 'PRICE')
                    if (old_vol<vol):
                        # add this position
                        glbdata.position.set_value(i, 'VOL', vol)
                        if (price==0.0):
                            # use current price
                            glbdata.cash = glbdata.cash - float(vol-old_vol) * 100.0 * current_price
                            # reevaluate price (average)
                            glbdata.position.set_value(i, 'PRICE', (old_price*float(old_vol)+current_price*(float(vol-old_vol)))/float(vol))
                        else:
                            glbdata.cash = glbdata.cash - float(vol-old_vol) * 100.0 * price
                            # reevaluate price (average)
                            glbdata.position.set_value(i, 'PRICE', (old_price*float(old_vol)+price*(float(vol-old_vol)))/float(vol))
                    else:
                        print "Error at buy_wp mod_trading.py"
                    break

            if (buy_new==1):
                if (price == 0.0):
                    glbdata.cash = glbdata.cash - float(vol) * 100.0 * current_price
                    new_position = pd.DataFrame(data=[(stock_code, current_price, vol)], columns=['CODE', 'PRICE', 'VOL'])
                else:
                    glbdata.cash = glbdata.cash - float(vol) * 100.0 * price
                    new_position = pd.DataFrame(data=[(stock_code, price, vol)], columns=['CODE', 'PRICE', 'VOL'])
                glbdata.position = glbdata.position.append(new_position,ignore_index=True)

            op_status=1
        return 0
    elif (op=='sell_all'):
        # sell with price
        while op_status!=1:
            for i in range(1,glbdata.position.size / 3):
                if (glbdata.position.get_value(i,'CODE')==stock_code):
                    total_vol = glbdata.position.get_value(i,'VOL')
                    glbdata.position = glbdata.position.drop(i)
                    # redo index
                    glbdata.position = glbdata.position.set_index([range(glbdata.position.size / 3)])
                    glbdata.cash = glbdata.cash + float(total_vol)*100.0*current_price
                    break
            op_status = 1
        return 0
    else:
        return 1
