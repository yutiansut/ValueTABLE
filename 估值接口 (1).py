



import numpy as np
import pandas as pd
import time
import re
import os
import csv
from datetime import timedelta, datetime


# In[2]:


#读取文件，并拆分成若干文件
def split_line(arr):
    return all([np.isnan(i) for i in arr])

        
def total_calc(data_path):
    a={}
    b={}
    c={}
    for i in ['股票账户','期货账户','ETF','场外收益互换']:
        try:
            a[i] = pd.read_excel(data_path,i)
        except:
            ValueError
        else:
            #利用split_line对表哥进行切割
            for j in range(len(a[i])):
                if split_line(a[i].iloc[j,:])==True:
                    line = j
                    break
            b[i] = a[i].iloc[:line,:]
            try:
                c[i] = pd.read_excel(data_path,i,header=line+2)
            except:
                IndexError
            else:
                c[i] = c[i].dropna(axis=1,how='all')
    return b,c




b,c = total_calc('test.xlsx')


#已有股票标准输入数据时，对其计算的函数
#股票数据文件一定要包括三列：股票代码，持仓数量，和收盘价，否则会报错，若列名与实际有出入，可以修改函数中的中文部分
#函数将返回一个计算资产价格后的表，一个总的股票资产总额,和一个股票资产总额+账户余额总额
def stock_summary(stock_data,account_data ):
    data = stock_data.copy()
    data['资产价格'] = stock_data.持仓数量*stock_data.收盘价
    return [int(account_data.可用资金),sum(data['资产价格']),sum(data['资产价格'])+int(account_data.可用资金)]


# In[7]:


stock_summary(c['股票账户'],b['股票账户'])


# In[8]:


#若没有标准输入，只有营业部对账单的流水明细和持仓明细，下面的函数可以将营业部对账单转换为股票标准输入
#输入为文件名和路径名称，两者均为字符串类型
#如输入：convert('test.txt','D://test2//')即可将营业部对账单文件'D://test2//test.txt'转换为标准的股票数据格式
def convert_data(data_raw,path_data):
    context=[line for line in open(path_data+data_raw)]
    detail_l=[int('流水' in line) for line in context].index(1)
    detail_r=[int('最新价' in line) for line in context].index(1)
    if os.path.exists(path_data+'test_detail1.txt') :
        os.remove(path_data+'test_detail1.txt')
        
    with open(path_data+'test_detail1.txt', 'w') as f2:
        for line in context[detail_r:]:
            f2.write(' '.join(line.split())+'\n')
    Q=[line for line in open(path_data+'test_detail1.txt')]
    
    def special_space(str1):
        pattern_o = r'.{10}\s\d{6}\s[\u4e00-\u9fa5]{2,4}\s.*'
        pattern_f = r'.{10}\s\d{6}\s[\u4e00-\u9fa5]{1}\s[\u4e00-\u9fa5]{1}\s.*'
        if re.match('^--',str1):
            return '\n'
        if re.match(pattern_o,str1)==None:
            if not re.match(pattern_f,str1)==None:
                pattern = re.compile(r'[\u4e00-\u9fa5]')   # 查找数字
                result1 = pattern.findall(str1)[:-3]
                s1,s2 = str1.index(result1[0]),str1.index(result1[1])
                return str1[:(s1+1)]+str1[s2]+str1[s2+2:]
            else:
                return str1
        else:
            return str1
    
    position=[special_space(line) for line in open(path_data+'test_detail1.txt')]
    if os.path.exists(path_data+'test_detail1.csv'):
        #删除文件
        os.remove(path_data+'test_detail1.csv')
    with open(path_data+'test_detail1.csv', 'w', newline='') as g2:
         csv_writer = csv.writer(g2)
         for line in position:
            csv_writer.writerow(line.split())   
    f1 = pd.read_csv(path_data+'test_detail1.csv',encoding='gbk',header=0 )
    return f1


# In[9]:


#期货的计算
#输入包括三个部分，期货数据表所在的文件路径，日期和可用资金
#期货数据一定要有期货品种，数量，保证金，成本
def futures_summary(futures_data,account_data):

    data = futures_data.copy()
    
    def calc_num(str1):
        str2 = str1[:2]
        if str2=='IF'or str2=='IH':
            return 300
        elif str2=='IC':
            return 200
        else:
            return None
                
    data['合约乘数'] = (data.期货代码).apply(calc_num)
    #利用估计的结算价计算新的保证金
    data['资产价格'] = data['合约乘数']*data.持仓数量*data.收盘价
    data['保证金'] =  data['资产价格']*0.33
    data['更新后保证金'] = data.保证金*data.估结算/data.收盘价
    #计算每个品种的期货增值税
    data['增值税'] = (data.收盘价-data.平均成本)*data.合约乘数*data.持仓数量*0.03
    #计算更新后的总资产（更新后的保证金+可用资金）
    return  data,int(account_data.可用资金)+sum(data.更新后保证金)


# In[10]:


futures_summary(c['期货账户'],b['期货账户'])[0]


# In[11]:


#ETF计算
def etf_summary(etf_data,acount_data):
    data = etf_data.copy()
    data['资产价格'] =data.持仓数量*data.收盘价
    return int(acount_data.融券利息),data,int(acount_data.融券利息)+int(data.资产价格)


# In[12]:


etf_summary(c['ETF'],b['ETF'])


# In[13]:


def swap_summary(swap_data):
    return int(swap_data.总负债)


# In[14]:


swap_summary(b['场外收益互换'])


# In[15]:


def calc_fee(net_value_yesterday,)


# In[16]:


def make_sheet(data_path):
    b,c = total_calc(data_path)
    stock_summary(c['股票账户'],b['股票账户'])
    futures_summary(c['期货账户'],b['期货账户'])[0]
    etf_summary(c['ETF'],b['ETF'])
    swap_summary(b['场外收益互换'])

