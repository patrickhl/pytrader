import pandas as pd
import multiprocessing
# How to use:
# import glbdata (for module inside stockanalysis)
# from stockanalysis import glbdata (for module outside stock_analysis)
# call it as glbdata.xxx

# current position list
position = pd.DataFrame(data=[('000000', 0.0, 0.0)], columns=['CODE', 'PRICE', 'VOL'])
# targeting position list
new_position = pd.DataFrame(data=[('000000', 0.0, 0.0)], columns=['CODE', 'PRICE', 'VOL'])
# INITIAL case
cash_init = 1000000.0
# current total cash
cash = 1000000.0
# risk list
risk_list = pd.DataFrame(data=[('000000', 0.0, 0.0)], columns=['CODE', 'strategy1','weight1'])

# total stocks in SH A
SH_A_NR = 1208

# threading lock
mutex = multiprocessing.Lock()

# stock_validation
#validation = multiprocessing.Manager().list(['000000',False])
#pd.DataFrame(data=[('000000', False)], columns=['CODE', 'VALID'])

#profit delta
#Base date is 1 (100%)
profit_delta = pd.DataFrame(data=[('Base', 1)], columns=['DATE', 'PROFIT'])
