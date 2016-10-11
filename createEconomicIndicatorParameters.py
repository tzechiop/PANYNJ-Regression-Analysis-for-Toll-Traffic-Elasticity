# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:31:20 2016

This script creates parameter files that have one of each economic indicator.

@author: thasegawa
"""

import os
import pandas as pd

basepath = r'C:\Users\thasegawa\Documents\53 Port Authority Toll\06 Python Projects\Regression Analysis\data\regress_para'
group_list = ['pathmid',
              'pathnj',
              'pathnyc',
              'pathtotal',
              'pathwtc']
              
economic_list = list(pd.read_excel('data\\fields\\economicIndicators_Real.xlsx', header=None)[0])
fuel_list = list(pd.read_excel('data\\fields\\fuel_binary.xlsx', header=None)[0]) + [None]
              
for group in group_list:
    para = pd.read_excel(os.path.join(basepath, 'templates\\regresscols_%s_template_limited.xlsx' % group))
    for fuel in fuel_list:    
        for economic in economic_list:
            remove = [column for column in economic_list if column != economic]
            remove += [column for column in fuel_list if column != fuel]
            columns = [column for column in para['column'] if column not in remove]
            df = para[para['column'].isin(columns)]
            df.to_excel(os.path.join(basepath, 'regresscols_{0}_{1}_{2}.xlsx'.format(group, economic, fuel)), index = False)