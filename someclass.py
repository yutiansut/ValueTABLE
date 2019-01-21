class NetValue(object):
    """
    NetValue类包含三个变量，总净值，总份额和单位净值
    NetValue包含一个成员函数，赎回操作对总份额和总净值的修改
    """
    def __init__(self,total_value,share):
        self.total_value = total_value
        self.share = share+0.0
        self.unit_value = self.total_value/self.share

    #赎回操作，赎回后扣减相应份额和总净值
    def redemption(self,redeem_share):
        self.share = self.share- redeem_share
        self.total_value = self.unit_value *self.share

class CostRate(object):
    """
    CostRate类包含三个变量
    托管费费率，管理费费率和服务费费率
    NetValue包含一个成员函数，赎回操作对总份额和总净值的修改
    """
    def __init__(self,tgf_rate,glf_rate,fwf_rate):
        """

        :type tgf_rate: object
        """
        self.tgf_rate = tgf_rate
        self.glf_rate = glf_rate
        self.fwf_rate = fwf_rate

class Liability(object):
    def __init__(self,df_etf=0,df_swap=0):
        if not df_etf==0:
            self.etf = df_etf
        if not df_swap==0:
            self.swap = df_swap

class Stock(object):
    def __init__(self, df_stock):
        #首先对stock按照股票数字代码进行排序
        df_stock = df_stock.sort_values(by = '股票代码')
        #接着对stock按照股票代码进行分类，
        df_stock['类别'] = df_stock['股票代码'].apply(lambda str1 : {'6':'H','3':'C','0':'S'}[str1[0]])
        df_stockgroup = df_stock.groupby(['类别'])
        #分类之后，对每一类合计成本和 市值
        self.stockgroupsum =  df_stockgroup['成本','市值 '].sum()
        self.stock = df_stockgroup
        if df_future==0:
            pass
        else:
            self.future = df_future

class Future(object):

class yfglrbc()







