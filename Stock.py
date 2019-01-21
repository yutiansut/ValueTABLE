from WindPy import *
import pandas as  pd
w.start()
class Stock(object):
    def __init__(self, df_stock):

        df_stock['股票代码'] = df_stock['股票代码'].apply(str)
        #首先对stock按照股票数字代码进行排序
        df_stock = df_stock.sort_values(by = '股票代码')

        df_stock['成本'] = df_stock['单位成本']*df_stock['持仓数量']
        df_stock['市值'] = df_stock['收盘价']*df_stock['持仓数量']
        #接着对stock按照股票代码进行分类，
        df_stock['类别'] = df_stock['股票代码'].apply(lambda str1 : {'6':'H','3':'C','0':'S'}[str1[0]])
        df_stockgroup = df_stock.groupby(['类别'])
        #分类之后，对每一类合计成本和 市值
        self.stockgroupsum =  df_stockgroup['成本','市值 '].sum()
        self.stock = df_stockgroup