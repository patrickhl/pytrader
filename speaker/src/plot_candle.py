import matplotlib.finance as fin
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tik
import datetime as dt

def plot_candle(stock_code):
# get stock data
    stock_data = pd.read_csv('../data/' + stock_code + '/hist_k_day.csv')

    data_o = stock_data['open']
    data_c = stock_data['close']
    data_h = stock_data['high']
    data_l = stock_data['low']


# draw candle stick
    fig = plt.figure()
    #ax1 = fig.add_subplot(1,1,1)
    ax1 = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax1.set_title(stock_code)
    #ax1.set_xticks(stock_data['date'][0:80])
    ax1.set_ylabel("Price")
    fin.candlestick2_ochl(ax1, stock_data['open'][0:80], stock_data['close'][0:80], stock_data['high'][0:80],
                      stock_data['low'][0:80], width=1, colorup='r', colordown='g', alpha=0.8)

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.grid(True)
    plt.show()
