class NetValue(object):
    '''
    NetValue类包含三个变量，总净值，总份额和单位净值
    NetValue包含一个成员函数，赎回操作对总份额和总净值的修改
    '''
    def __init__(self,total_value,share):
        self.total_value = total_value
        self.share = share+0.0
        self.unit_value = self.total_value/self.share

    #赎回操作，赎回后扣减相应份额和总净值
    def redemption(self,redeem_share):
        self.share = self.share- redeem_share
        self.total_value = self.unit_value *self.share

class Cost_rate(object):
    '''
    Cost类包含三个变量
    托管费费率，管理费费率和服务费费率
    NetValue包含一个成员函数，赎回操作对总份额和总净值的修改
    '''
    def __init__(self,tgf_rate,glf_rate,fwf_rate):
        self.tgf_rate = tgf_rate
        self.glf_rate = glf_rate
        self.fwf_rate = fwf_rate

class Liability(object):
    def __init__(self):
        self.etf =
        self.swap =
class Asset(object):
    def __init__(self):
        self.stock =
        self.future =
        self.

# 定义一个估值表类
class BalanceSheet(object):
    #下面用BS作为BalanceSheet的简称

    def __init__(self,date,kind,stock,future,etf,swap,tgf_rate,glf_rate,fwf_rate,net_value =NetValue(0,0,0)):
        self.date = date
        self.kind = kind
        self.asset = Asset(stock,future)
        self.liability = Liability(etf,swap)
        self.cost_rate = Cost_rate(tgf_rate,glf_rate,fwf_rate)
        self.net_value = net_value

    #输入昨天的BalanceSheet和今天的交易明细，输出今天的BalanceSheet
    def calc_BS( BS_yestoday, detail_today ):

        return

    #修改份额
    #计算业绩报酬
    #打印
    #和表格比对