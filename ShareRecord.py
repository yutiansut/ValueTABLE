import pandas as pd
import numpy as np
from datetime import datetime,timedelta
class ShareRecord(object):
    """
    ShareRecord是记录基金份额的类
    该类的成员变量有：份额记录的表格（份额记录须包括：人名，何时以多少价格买入多少份额，该份额上一次提取业绩报酬的日期）
    该类的成员函数有：计算业绩报酬，改变份额记录
    """
    def __init__(self,record,ways_calc,path=0):
        """

        :param record:
        :param ways_calc:
        :param path:
        """
        if path==0:
            self.now_record = record
        else:

    def calc_reward(self):
        print('请说明是何种业绩报酬计算方式')
    def change_share(self, change_xlsx):
        """
        该函数用于改变份额记录，如申购，赎回，以红利转股的方式提取业绩报酬时，需调用该函数
        该函数的输入为一个xlsx格式的表格，上面需记录 ，人名，何时以多少价格买入（或赎回）多少份额
        """


class FenDuan(ShareRecord):
    """
    PieceWise表明分段计算业绩报酬
    该类的成员变量有：分段节点piece_point，分段提取比例piece_ratio，上一次提取业绩报酬日期last_day
    该类的成员函数有：计算业绩报酬

    """
    def __init__(self,point,ratio,date1,baseline = 0):
        """
        :param point: list格式，如[0,0.25,0.5]
        :param ratio: list格式，如[0.2,0.3,0.4]，这意味着收益率 0-25%提取0.2,25%-50%提0.3，大于50%提0.4
        :param date1: str格式，上一次提取业绩报酬日期
        :param baseline : float格式，对应时期的业绩基准收益率
        """
        self.piece_point = np.array(point)
        self.point_gap = np.append( np.array(point[1:]) - np.array(point[:-1]) ,float('inf'))
        self.piece_ratio = np.array(ratio)
        self.last_day = pd.to_datetime(date1)
        self.baseline = baseline

    def calc_reward(self,P1,P0,P0X,N,date_today = datetime.now()):
        """
        :param P1: 当天累计净值
        :param P0: 上次计提日累计净值
        :param P0X: 上次计提日净值
        :param N: 总份额
        :param date_today: 今天日期 （datetime格式）
        """
        period_len = (date_today - self.last_day).days/365
        annual_return  = (P1-P0)/ P0X / period_len - self.baseline
        temp_extraprofit = np.where(annual_return - self.piece_point>= 0 ,
                                    np.where(annual_return - self.piece_point>self.point_gap,
                                             self.point_gap,
                                             annual_return - self.piece_point),
                                    0)
        return np.sum(temp_extraprofit * self.piece_ratio * N * P0X * period_len)

    def change_point(self,point,ratio):
        self.piece_point = np.array(point)
        self.piece_ratio = np.array(ratio)

    def change_last_day(self,date1):
        self.last_day = pd.to_datetime(date1)

    def change_baseline(self,baseline):
        self.baseline = baseline




class DanShuiWei(ShareRecord):

    def __init__(self,arr_share,arr_shuiwei,ratio):
        """

        :param arr_share:
        :type arr_share: numpy.array
        :param arr_shuiwei:
        :param ratio:
        """
        self.arr_share = arr_share
        self.arr_shuiwei  = arr_shuiwei
        self.ratio = ratio

    def calc_reward(self,P1):
        return np.sum(self.arr_share * np.where(P1-self.arr_shuiwei>0,self.P1-self.arr_shuiwei,0) *  self.ratio)

class DanShuiWei_FenDuan(ShareRecord):
    def __init__(self, arr_share, arr_shuiwei,arr_date,  point,ratio):
        """

        :param arr_share:
        :param arr_shuiwei:
        :param arr_date:
        :param point:
        :param ratio:
        """
        self.arr_share = arr_share
        self.arr_shuiwei = arr_shuiwei
        self.arr_shuiwei_date =  arr_date
        self.piece_ratio = ratio
        self.piece_point = point
        self.point_gap = np.append(np.array(point[1:]) - np.array(point[:-1]), float('inf'))

    def calc_reward(self,P1,date_today = datetime.now()):
        arr_period_len = (pd.to_datetime(self.arr_shuiwei_date)-date_today).days
        piece_base = (P1  / self.arr_shuiwei -1) \
                     / arr_period_len
        def calc_every(num1):
            return np.where(num1 - self.piece_point >= 0,
                            np.where(num1 - self.piece_point > self.point_gap,
                                     self.point_gap,
                                     num1 - self.piece_point),
                            0)
        every_profit=[]
        for i,j in enumerate(piece_base):
            every_profit[i] = sum(calc_every(j)*self.piece_ratio * self.arr_share[i] * arr_period_len[i] * self.arr_shuiwei[i])
        return sum(every_profit)


class FundShuiWei(ShareRecord):
    """

    """

    def __init__(self,NAVh):
        self.NAVh = NAVh
    def calc_reward(self):

