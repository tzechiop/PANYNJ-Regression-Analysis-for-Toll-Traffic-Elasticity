# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:29:50 2016

@author: thasegawa
"""

import argparse
import os
import pandas as pd
from pandas.stats.api import ols

# Function to create output filename
def createOutfilename(infile, add):
    outfile, ext = os.path.splitext(infile)
    outfile += add + ext
    return outfile

# ============================================================================

print('Running regress.py...')

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('infiley')
parser.add_argument('infilex')
parser.add_argument('outfile', help="specify the output filename")
parser.add_argument('-o', '--outpath', help="specify the output folder")

args = vars(parser.parse_args())
infiley, infilex, outpath, outfile = args['infiley'], args['infilex'],  args['outpath'], args['outfile']

print('Infile for y: %s' % infiley)
print('Infile for x: %s' % infilex)
print('Outfile for regression: %s' % outfile)

y = pd.read_excel(infiley)
x = pd.read_excel(infilex)

# Perform Regerssion and output summary
print('Performing regression')
res = ols(y=y['y'], x=x[x.columns[1:]])
outdf = res.summary_as_matrix
outdf['R^2'] = res.r2
outdf.to_csv(outfile)
