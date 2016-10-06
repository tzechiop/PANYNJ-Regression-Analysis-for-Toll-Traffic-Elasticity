# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:29:50 2016

This script is used to create the x and y data files to be used for regression.
The script compiles columns from spreadsheets specified in 'colfile'. The column
'groupcol' (default = 'Year-Month') is used to combine the columns from every
spreadsheet, and thus should be included in every spreadsheet.
The file colfile should have have the following fields: 'infile', 'column', 'xy'

The file also converts variables to log if specified in 'colfile'.

The line below provides an example of a command used to run this script.
python createRegressInputs.py data\\regress_para\\regresscols_pathtotal_1.xlsx -o data\\regress_data


@author: thasegawa
"""

import argparse
import os
import pandas as pd
import numpy as np

# Function to create output filename
def createOutfilename(infile, add):
    outfile, ext = os.path.splitext(infile)
    outfile += add + ext
    return outfile
    
# Function to combine new x or y data
def addNew(data, newdata, groupcol, columns):
    if data is None:
        data = pd.DataFrame(newdata[[groupcol] + columns])
    else:
        data = pd.merge(data, newdata[[groupcol] + columns], how = 'left', on = groupcol)
    return data

# Convert speficied columns to log form
def convertToLog(data, column_list):
    for column in column_list:
        data[column] = data[column].apply(np.log10)
    return data

# ============================================================================

print('Running createRegressInputs.py...')

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('colfile')
parser.add_argument('-o', '--outpath', help="specify the output folder")
parser.add_argument('-oy', '--outfiley', help="specify the output file. default is colfile + '_x' and colfile + '_y'")
parser.add_argument('-ox', '--outfilex', help="specify the output file. default is colfile + '_x' and colfile + '_y'")
parser.add_argument('-c', '--groupcol', default='Year-Month', help="specifies the column that specifies the time scale")
parser.add_argument('-y', '--sumY', default=True, help="specifies if the Y data should be summed or not")
args = vars(parser.parse_args())
colfile, outpath, outfiley, outfilex, groupcol, sumY = args['colfile'], args['outpath'], args['outfiley'], args['outfilex'], args['groupcol'], args['sumY']

# If the outfile names were not specified, create defualt outfile names
if outfiley is None:
    outfiley = createOutfilename(colfile, '_y')
if outfilex is None:
    outfilex = createOutfilename(colfile, '_x')
    
if outpath is not None:
    outfiley = os.path.join(outpath, os.path.basename(outfiley))
    outfilex = os.path.join(outpath, os.path.basename(outfilex))

print('Column file: %s' % colfile)
print('Outfile for y: %s' % outfiley)
print('Outfile for x: %s' % outfilex)

# Read column file
coldata = pd.read_excel(colfile)
infile_list = coldata['infile'].unique()

# Compile Y data
ydata = None
xdata = None
for infile in infile_list:
    rdata = pd.read_excel(infile)

    # Iterate through x and y data of each input spreadsheet    
    subdata = coldata[coldata['infile'] == infile]    
    xy_list = subdata['xy'].unique()
    for xy in xy_list:
        print('Compiling {0} data from {1}'.format(xy, infile))
        idx = subdata['xy'] == xy
        columns = list(subdata['column'][idx])
        if xy == 'y':
            ydata = addNew(ydata, rdata, groupcol, columns)
        else:
            xdata = addNew(xdata, rdata, groupcol, columns)
                
# Sum the Y columns if specified
if sumY:
    cols = [column for column in ydata.columns.values if column != groupcol]
    ydata = pd.concat([ydata[groupcol], ydata[cols].sum(axis=1)], axis = 1)
    ydata.columns = [groupcol, 'y']

# Convert columns to log
print('Converting columns to log')
logcolumn_list = coldata['column'][(coldata['xy'] == 'x') & (coldata['log'] == True)]
xdata = convertToLog(xdata, logcolumn_list)
if sumY:
    ydata = convertToLog(ydata, ['y'])
else:
    logcolumn_list = coldata['column'][(coldata['xy'] == 'y') & (coldata['log'] == True)]
    ydata = convertToLog(ydata, logcolumn_list)
        
# Output files
ydata.to_excel(outfiley, index = False)
xdata.to_excel(outfilex, index = False)
print('Success!')