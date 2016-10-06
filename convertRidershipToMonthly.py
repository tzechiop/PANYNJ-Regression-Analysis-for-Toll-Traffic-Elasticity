# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:29:50 2016

This is a script that takes ridership data (presumably PATH) and sums it by
month. The input data should have a column 'Year-Month' (unless specified otherwise)
that can be used to group by month.

To run this script on path data, use the following command:
python covertRidershipToMonthly.py data\\path_ridership.xlsx -f 7 

@author: thasegawa
"""

import argparse
import os
import pandas as pd

# ============================================================================

print('Running convertRidershipToMonthly.py...')

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('infile')
parser.add_argument('-o', '--outfile', help="specify the output file. default is input + '_monthly'")
parser.add_argument('-f', '--firstcol', default=0, type=int, help="specifies the first column in the group of columns that should be preserved in the output")
parser.add_argument('-l', '--lastcol', type=int, help="specifies the last column in the group of columns that should be preserved in the output")
parser.add_argument('-c', '--groupcol', default='Year-Month', help="specifies the column to be used to group monthly data. Year and month should be split by '-'")
args = vars(parser.parse_args())
infile, outfile, firstcol, lastcol, groupcol = args['infile'], args['outfile'], args['firstcol'], args['lastcol'], args['groupcol']

# If the outfile name was not specified, create default outfile name
if outfile is None:
    outfile, ext = os.path.splitext(infile)
    outfile += '_monthly' + ext
print('Input: %s' % infile)
print('Output: %s' % outfile)

# Read data
data = pd.read_excel(infile)

# Determine columns to keep in output file
if lastcol is None:
    lastcol = len(data.columns.values)
keepcol_list = [column for column in data.ix[:,firstcol:lastcol]._get_numeric_data().columns.values if (column != groupcol)]

# Sum ridership data by month
monthly = data.groupby([groupcol]).sum()[keepcol_list]

# Add back in date columns
monthly[groupcol] = monthly.index
monthly['Year'], monthly['Month'] = zip(*([int(y) for y in x.split('-')] for x in monthly.index))

# Output monthly data
monthly = monthly.sort_values(['Year', 'Month'])
monthly[['Month', 'Year', groupcol] + keepcol_list].to_excel(outfile, index = False)

print('Success!')