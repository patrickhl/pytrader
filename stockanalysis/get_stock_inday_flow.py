# -*- coding:gbk -*-
import urllib
import re
import pandas as pd
# this function grab inday money flow data, 
# the data is refreshed for every 6 seconds,
# can be called for every 6 seconds.

def get_stock_inday_flow(code):
    response = urllib.urlopen("http://qt.gtimg.cn/r=3.14159265357q=ff_"+code).read()
    rr = re.compile(b'~([\d|\^|\.]*)')
    array = rr.findall(response)
    # data:
    # 1: large flow in
    # 2: large flow out
    # 3: large net flow in (flow_in - flow_out)
    # 4: large net_flow_in/(flow_in + flow_out)
    # 5: retail flow in
    # 6: retail flow out
    # 7: retail net flow in (flow_in - flow_out)
    # 8: retail net_flow_in/(flow_in + flow_out)
    # 9: total flow (1 + 2 + 5 + 6)
    #10: time
    res = array[0:9]
    res.append(array[-1])
    final_res = pd.DataFrame(res)

    # return the final res in row
    return final_res.T

