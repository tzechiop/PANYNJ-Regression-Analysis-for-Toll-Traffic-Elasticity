# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 12:53:59 2016

@author: thasegawa
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:29:50 2016

This script is used to split the regress input data by date.

python splitByDate.py data\\external.xlsx 2000-1 2015-12 -o external_2000_2015.xlsx -p data

@author: thasegawa
"""

import os
import argparse
import pandas as pd

# Function to create output filename
def createOutfilename(infile, add):
    outfile, ext = os.path.splitext(infile)
    outfile += add + ext
    return outfile

# Function to iterate through months
def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    dates = []
    for ym in range( ym_start, ym_end + 1 ):
        y, m = divmod( ym, 12 )
        dates.append('{0:d}-{1:d}'.format(y, m+1))
    return dates

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('infile')
parser.add_argument('datestart', type = str, help="specifies the start date")
parser.add_argument('dateend', type = str, help="specifies the start date")
parser.add_argument('-c', '--groupcol', default='Year-Month', help="specifies the column that specifies the time scale")
parser.add_argument('-p', '--outpath', help="specify the output folder")
parser.add_argument('-o', '--outfile', help="specify the output filename")
args = vars(parser.parse_args())
infile, datestart, dateend, groupcol, outpath, outfile = args['infile'], args['datestart'], args['dateend'], args['groupcol'], args['outpath'], args['outfile']

# If the outfile names were not specified, create defualt outfile names
if outfile is None:
    outfile = createOutfilename(infile, '_date')
    
if outpath is not None:
    outfile = os.path.join(outpath, os.path.basename(outfile))
    
print('Infile: %s' % infile)
print('Outfile: %s' % outfile)
print('Start date: %s' % datestart)
print('End date: %s' % dateend)

# Create array for Year-Month
start_year, start_month = [int(x) for x in datestart.split('-')]
end_year, end_month = [int(x) for x in dateend.split('-')]
dates = month_year_iter( start_month, start_year, end_month, end_year )

# Read input data
data = pd.read_excel(infile)

# Retrieve rows within date range
data = data[data[groupcol].isin(dates)]
data.to_excel(outfile, index = False)

print('Success!')