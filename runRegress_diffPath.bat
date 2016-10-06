echo off
echo ===All===
call runRegress.bat 6 total
echo ===NYC===
call runRegress.bat 2 nyc
echo ===NJ===
call runRegress.bat 2 nj
echo ===Midtown===
call runRegress.bat 2 mid
echo ===WTC===
call runRegress.bat 2 wtc