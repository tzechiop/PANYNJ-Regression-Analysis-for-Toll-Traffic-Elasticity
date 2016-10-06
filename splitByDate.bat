echo off

set arg1=%1
set arg2=%2
python splitByDate.py data\\external.xlsx %arg1% %arg2% -o external_%arg1%_%arg2%.xlsx -p data
python splitByDate.py data\\path_fares.xlsx %arg1% %arg2% -o path_fares_%arg1%_%arg2%.xlsx -p data
python splitByDate.py data\\path_ridership_monthly.xlsx %arg1% %arg2% -o path_ridership_monthly_%arg1%_%arg2%.xlsx -p data
