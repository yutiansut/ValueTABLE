
import somefunction
from someclass import NetValue, Cost_rate, Liability, Asset

# 定义一个估值表类
class BalanceSheet(object):
    #下面用BS作为BalanceSheet的简称

    def __init__(self,date,kind,stock,future,etf,swap,tgf_rate,glf_rate,fwf_rate,net_value =NetValue(0,0)):
        self.date = date
        self.kind = kind
        self.asset = Asset(stock,future)
        self.liability = Liability(etf,swap)
        self.cost_rate = Cost_rate(tgf_rate,glf_rate,fwf_rate)
        self.net_value = net_value

    #输入昨天的BalanceSheet和今天的交易明细，输出今天的BalanceSheet
    def calc_BS( BS_yestoday, detail_today ):
        #首先要检查两天的内容是否只间隔一个工作日，如果并非只间隔一个工作日，则需提醒运行该函数的人
        #由于电脑无法判别清明中秋等传统假期，因此提醒之后仍然需要运行函数者自行判断
        #因此电脑仅会提示，但无论何种情况都会计算出结果
        if BS_yestoday.date == somefunction.getlastweekday(detail_today.date):
            pass
        else:
            print('信息并不来自两个连续的工作日 ')

        return

    #修改份额
    def correct_share(self):
        return

    #计算业绩报酬
    def calc_return(self):
        return
    #打印
    def print_table(self):
        return

    #和表格比对