# -*- coding:gbk -*-
import urllib
import re
import pandas as pd
# this function grab inday price data, 
# the data is refreshed for every 6 seconds,
# can be called for every 6 seconds.

def get_stock_inday_data(code):
    # r is a psudo random number 
    response = urllib.urlopen("http://qt.gtimg.cn/r=3.14159265357q="+code).read()
    rr = re.compile(b'~([\w|\.|\/|\\|:|-]*)')
    array = rr.findall(response)
    # data:
    # 1: current price
    # 2: close
    # 3: open
    # 4: dealed lot (shou)
    # 5: out buy volume (buy at the sel1 price)
    # 6: in sel volume (sell at the buy1 price)
    # 7: buy1 price
    # 8: buy1 lot
    # 9: buy2 price
    #10: buy2 lot
    #11: buy3 price
    #12: buy3 lot
    #13: buy4 price
    #14: buy4 lot
    #15: buy5 price
    #16: buy5 lot
    #17: sel1 price
    #18: sel1 lot
    #19: sel2 price
    #20: sel2 lot
    #21: sel3 price
    #22: sel3 lot
    #23: sel4 price
    #24: sel4 lot
    #25: sel5 price
    #26: sel5 lot
    #27: recent deal
    #28: time
    #29: change (in Yuan)
    #30: change rate (in percent)
    #31: high
    #32: low
    #33: price/lot(shou)/volume(in Yuan)
    #34: dealed lot(shou)
    #35: dealed volume (in wan) (turnover)
    #36: turnover ratio
    #37: PE TTM (trailing twelve months)
    #38: NaN
    #39: high
    #40: low
    #41: range (in percent) (high - low)/close
    #42: total value in market (can be traded)
    #43: total capital
    #44: PB
    #45: high limit
    #46: low limit
    #47: Volume Ratio Index (Dealed_Lot_per_Minues)/(Average_Dealed_Lot_per_Minues_in_past_5_days)
    #48: Unknown
    #49: Average price
    #50: PE (active)
    #51: PE (static)
    res = pd.DataFrame(array[2:])
    
    # return the res in row
    return res.T
