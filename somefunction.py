import numpy as np
import pandas as pd
from datetime import *

def getlastweekday(day=date.today):
    now = day
    if now.isoweekday() == 1:
        day_step = 3
    else:
        day_step = 1
    return now - timedelta(days=day_step)

#-------------------------------------------分割线----------------------------------------------------






def calc_fee(net_value_yesterday, )



def make_sheet(data_path):
    b, c = total_calc(data_path)
    stock_summary(c['股票账户'], b['股票账户'])
    futures_summary(c['期货账户'], b['期货账户'])[0]
    etf_summary(c['ETF'], b['ETF'])
    swap_summary(b['场外收益互换'])