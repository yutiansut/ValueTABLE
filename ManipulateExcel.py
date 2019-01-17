#!/usr/bin/env python
#-*- coding: utf-8 -*-
# 导入xlwt模块

import xlwt
import copy

# 创建一个Workbook对象，这就相当于创建了一个Excel文件

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

'''
Workbook类初始化时有encoding和style_compression参数
encoding:设置字符编码，一般要这样设置：w = Workbook(encoding='utf-8')，就可以在excel中输出中文了。
style_compression:表示是否压缩，不常用。
'''

# 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格。
sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
# 其中的sheet1是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，默认值是False

#设置单元格宽度
for i in range(11):
    sheet.col(i).width = 217*20
# 向表test中添加数据

#设置字体
style = xlwt.XFStyle()
'''
如果要设置背景颜色的话
pattern =  xlwt.Pattern()
pattern.pattern_fore_colour = 5
style.pattern = pattern
'''
fnt = xlwt.Font()   # 创建一个文本格式，包括字体、字号和颜色样式特性
fnt.name = u'黑体'  # 设置其字体为微软雅黑
fnt.bold = True
fnt.height = 400
style.font = fnt   #将赋值好的模式参数导入Style

#设置居中格式
alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER    #水平居中
alignment.vert = xlwt.Alignment.VERT_CENTER    #垂直居中
style.alignment = alignment

style2  = copy.deepcopy(style)
style2.font.height =220

#写入数据
sheet.write_merge(0,0,0,10,'证券投资基金估值表',style)
sheet.write_merge(1,1,0,10,'广发证券___致远若谷二号私募证券投资基金___专用表',style2)
sheet.write_merge(2,2,0,1,'估值日期：')
sheet.write_merge(2,2,7,9,'单位净值：')
sheet.write(2,10,'单位：元')
data = [ '科目代码','科目名称','数量','单位成本','成本','成本占净值%','市价','市值','市值占净值%','估值增值','停牌信息']
i = 0#控制列
for i in range(len(data)):
    sheet.write(3,i,data[i],style2)
#到这里为止，已经写完了[0,3]行
for i in range(4,)
book.write
book.save(r'e:\test1.xls')  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错