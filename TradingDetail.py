import pandas as pd
import numpy as np


# 下面这些函数均为构造Trading Detail类所需要的函数
# 读取文件，并拆分成若干文件
def split_line(arr):
    return all([np.isnan(i) for i in arr])


def total_calc(data_path):
    # 字典a用于记录excel表的每个sheet文件
    a = {}
    # 字典b用于记录每天交易的概述，如：股票总资产，期货总保证金，股票账户总的可用现金
    b = {}
    # 字典c用于记录每天交易细，如：具体的股票期货持仓
    c = {}
    for i in ['股票账户', '期货账户', 'ETF', '场外收益互换']:
        try:
            if i=='股票账户':
                a[i] = pd.read_excel(data_path, i,os.getcwd() + os.sep + 'stock.xlsx',converters ={'股票代码':str} )
            else:
                a[i] = pd.read_excel(data_path, )
        except:
            ValueError
        else:
            # 利用split_line对表哥进行切割
            for j in range(len(a[i])):
                if split_line(a[i].iloc[j, :]):
                    break
            b[i] = a[i].iloc[:j, :]
            try:
                c[i] = pd.read_excel(data_path, i, header=j + 2)
            except:
                IndexError
            else:
                c[i] = c[i].dropna(axis=1, how='all')
    return b, c


# 股票的计算
# 股票计算的两个输入均为DataFrame格式，stock_data一定要包括三列：股票代码，持仓数量，和收盘价，否则会报错，若列名与实际有出入，可以修改函数中的中文部分
# 函数将返回一个计算资产价格后的表，一个总的股票资产总额,和一个股票资产总额+账户余额总额
def stock_summary(df_stock, account_data):
    df_stock['股票代码'] = df_stock['股票代码'].apply(zfill(5))
    df_stock['市值'] = df_stock.持仓数量 * df_stock.收盘价
    df_stock['成本'] = df_stock['单位成本'] * df_stock['持仓数量']
    df_stock['估值增值'] = df_stock['成本'] - df_stock['市值']
    account_data['持仓市值'] = sum(df_stock['市值'])
    account_data['总资产'] = account_data['持仓市值'] + int(account_data.可用资金)
    # 接着对stock按照股票代码进行分类，
    #df_stock['类别'] = df_stock['股票代码'].apply(lambda str1: {'6': 'H', '3': 'C', '0': 'S'}[str1[0]])
    #df_stockgroup = df_stock.groupby(['类别'])
    # 分类之后，对每一类合计成本和 市值
    #self.stockgroupsum = df_stockgroup['成本', '市值 '].sum()
    ##self.stock = df_stockgroup
    data = df_stock.copy()
    return data, account_data


# 期货的计算
# 期货计算的两个输入均为DataFrame格式，futures_data的columns一定要有期货品种，数量，保证金，成本
def futures_summary(futures_data, account_data):
    data = futures_data.copy()

    # 一手IF或者IH对应300份，一手 IC对应200份
    def calc_num(str1):
        str2 = str1[:2]
        if str2 == 'IF' or str2 == 'IH':
            return 300
        elif str2 == 'IC':
            return 200
        else:
            return None

    data['合约乘数'] = data.期货代码.apply(calc_num)
    # 利用估计的结算价计算新的保证金
    data['资产价格'] = data['合约乘数'] * data.持仓数量 * data.收盘价
    data['保证金'] = data['资产价格'] * 0.33
    data['更新后保证金'] = data.保证金 * data.估结算 / data.收盘价
    # 计算每个品种的期货增值税
    data['增值税'] = (data.收盘价 - data.平均成本) * data.合约乘数 * data.持仓数量 * 0.03
    # 计算更新后的总资产（更新后的保证金+可用资金）
    account_data['更新后总资产'] = int(account_data.可用资金) + sum(data.更新后保证金)
    return data, account_data


# ETF计算
def etf_summary(etf_data, account_data):
    data = etf_data.copy()
    data['etf资产价格'] = data.持仓数量 * data.收盘价
    account_data['总负债'] = int(account_data.融券利息) + int(data.资产价格)
    return data, account_data


# swap无需计算任何东西


# TradingDetail类可以记录每天交易细节，每天的交易细节的格式如test.xlsx所示
# 在记录每天的交易细节时，会计算：
'''
1.每个股票的持仓总资产
2.每种期货的总负债，更新后保证金
'''

class TradingDetail(object):
    # TradingDetail类的构造函数的输入变量仅为一个xlsx文件的路径
    def __init__(self, path):
        self.raw_summary, self.raw_detail = total_calc(path)

        try:
            self.fut_detail, self.fut_summary = futures_summary(self.raw_detail['期货账户'], self.raw_summary['期货账户'])
        except:
            ValueError

        try:
            self.sto_detail, self.sto_summary = stock_summary(self.raw_detail['股票账户'], self.raw_summary['股票账户'])
        except:
            ValueError

        try:
            self.etf_detail, self.etf_summary = etf_summary(self.raw_detail['ETF'], self.raw_summary['ETF'])
        except:
            ValueError

        try:
            self.swap_summary = self.raw_detail['场外收益互换']
        except:
            ValueError
