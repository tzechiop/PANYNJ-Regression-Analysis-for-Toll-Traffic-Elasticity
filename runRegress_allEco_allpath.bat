echo off
echo ============================All============================
call runRegress_allEco.bat total
echo ============================NYC============================
call runRegress_allEco.bat nyc
echo ============================NJ============================
call runRegress_allEco.bat nj
echo ============================Midtown============================
call runRegress_allEco.bat mid
echo ============================WTC============================
call runRegress_allEco.bat wtc