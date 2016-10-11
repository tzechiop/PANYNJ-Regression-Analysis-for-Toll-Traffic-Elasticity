# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:10:05 2016

@author: thasegawa
"""

import os
import pandas as pd

economic_list = list(pd.read_excel('data\\fields\\economicIndicators_Real.xlsx', header=None)[0])
#fuel_list = list(pd.read_excel('data\\fields\\fuel_binary.xlsx', header=None)[0]) + [None]
fuel_list = list(pd.read_excel('data\\fields\\fuel_binary.xlsx', header=None)[0])

# Iterate through each regression result and retrieve R^2 and coefficient
group_list = ['pathmid',
              'pathnj',
              'pathnyc',
              'pathtotal',
              'pathwtc']
path = 'data\\regress_out\\all_v2'

outcol_list = ['PATH Group',
               'R^2',
               'Elasticity Coefficient',
               'Economic Variable',
               'Economic Coefficient',
               'Fuel Variable',
               'Fuel Coefficient',
               'M1 Coefficient',
               'M2 Coefficient',
               'M3 Coefficient',
               'M4 Coefficient',
               'M5 Coefficient',
               'M6 Coefficient',
               'M7 Coefficient',
               'M8 Coefficient',
               'M9 Coefficient',
               'M10 Coefficient',
               'M11 Coefficient',
               'Recession_FRED Coefficient',
               'Sandy Coefficient',
               'Snow_Median Coefficient',
               'Intercept']

out_dict = {key: [] for key in outcol_list}

fname_list = os.listdir(path)
for index, group in enumerate(group_list):
    R2_list = []
    coef_list = []
    for fuel in fuel_list:
        for economic in economic_list:
            fname = 'regress_summary_{0}_{1}.txt'.format(group, economic)
            with open(os.path.join(path,fname)) as f:

                lines = f.readlines()
                for line in lines:
                    if line[:9] == 'R-squared':
                        R2 = float(line.strip().split(' ')[-1])
                    linesplit = line.split('    ')
                    if (len(linesplit) > 2):
                        if (linesplit[1] == 'Fare-1Trip'):
                            coef = float(linesplit[2])
                if R2 is not None:
                    R2_list.append(R2)
                else:
                    R2_list.append(-999)
                if coef is not None:
                    coef_list.append(coef)
                else:
                    coef_list.append(-999)
        if index == 0:
            R2_out = pd.DataFrame({'Economic Indicator': economic_list,
                                   group: R2_list})
            coef_out = pd.DataFrame({'Economic Indicator': economic_list,
                                     group: coef_list})
        else:
            R2_out[group] = R2_list
            coef_out[group] = coef_list
R2_out.to_excel('data\\regress_out\\regresssummary_R2.xlsx', index = False)
coef_out.to_excel('data\\regress_out\\regresssummary_coef.xlsx', index = False)