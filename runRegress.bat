echo off

set arg1=%1
set arg2=%2

python createRegressInputs.py data\\regress_para\\regresscols_path%arg2%_%arg1%.xlsx -o data\\regress_data
python regress.py data\\regress_data\\regresscols_path%arg2%_%arg1%_y.xlsx data\\regress_data\\regresscols_path%arg2%_%arg1%_x.xlsx data\\regress_out\\regress_summary_path%arg2%_%arg1%.csv
REM notepad++ data\\regress_out\\regress_summary_path%arg2%_%arg1%.txt