@echo off

set YEAR=%date:~6,4%
set MONTH=%date:~0,2%
set DAY=%date:~3,2%
set LOGDAY=%YEAR%%MONTH%%DAY%

rem Get the date from WMI (on one line).
for /f "skip=2 tokens=2-7 delims=," %%A in ('wmic
path win32_localtime get day^,month^,year^ /format:csv') do (
set /a "yest_yyyy = %%C"
set /a "yest_mm = %%B"
set /a "yest_dd = %%A"
)

rem Not the first of the month, just decrement day.
if not %yest_dd%==1 (
set /a yest_dd = yest_dd - 1
goto done
)

rem Jan 1, set to Dec 31 previous year.
if %yest_mm%==1 (
set /a "yest_dd = 31"
set /a "yest_mm = 12"
set /a "yest_yyyy = yest_yyyy - 1"
goto :done
)

rem Any other day, decrement month.
set /a "yest_mm = yest_mm - 1"

rem Need to find last day, default to 31.
set dim=31

rem Apr/Jun/Sep/Nov all have 30 days. Feb gets special handling.
if %yest_mm%==4 set dim=30
if %yest_mm%==6 set dim=30
if %yest_mm%==9 set dim=30
if %yest_mm%==11 set dim=30
if not %yest_mm%==2 goto :got_dim

rem Default Feb to 28 then use rules to override.
set dim=28
set /a "divid=yest_yyyy%%400"
if "%divid%"=="0" goto daysinmonth_29days
set /a "divid=yest_yyyy%%100"
if "%divid%"=="0" goto :done
set /a "divid=yest_yyyy%%4"
if not "%divid%"=="0" goto :got_dim

rem Adjust to 29 days.
:daysinmonth_29days
set dim=29
:got_dim
set yest_dd=%dim%
:done

rem Pad out and return value.
if %yest_mm% lss 10 set yest_mm=0%yest_mm%
if %yest_dd% lss 10 set yest_dd=0%yest_dd%

set YESTERDAY=%yest_yyyy%%yest_mm%%yest_dd%

set BASEPATH=D:\elsys\solar
set KEY=7JeY7Iuc7Iqk7IS47KKF64yA
set USERIDX1=UR00000126
set USERIDX2=UR00000140
set USERIDX3=UR00000172

set INVOID11=1018201609091504.1.1.9.160110033
set INVOID12=1018201609091504.1.1.9.160110034
set INVOID13=1018201609091504.1.1.9.160110035
set INVOID14=1018201609091504.1.1.9.160110036
set INVOID21=1018201609091504.1.1.9.160110107
set INVOID22=1018201609091504.1.1.9.160110108
set INVOID23=1018201609091504.1.1.9.160110109
set INVOID24=1018201609091504.1.1.9.160110110
set INVOID25=1018201609091504.1.1.9.160110111
set INVOID31=1018201609091504.1.1.9.1908271116
set INVOID32=1018201609091504.1.1.9.1908271117
set INVOID33=1018201609091504.1.1.9.1908271118
set INVOID34=1018201609091504.1.1.9.1908271119

set POW24PATH=%BASEPATH%\pow_24
:: 저장 = 오후 11시 58분 이 적당

curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow_24h?userIdx=%USERIDX1%&key=%KEY%" > %POW24PATH%\%USERIDX1%\%LOGDAY%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow_24h?userIdx=%USERIDX2%&key=%KEY%" > %POW24PATH%\%USERIDX2%\%LOGDAY%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow_24h?userIdx=%USERIDX3%&key=%KEY%" > %POW24PATH%\%USERIDX3%\%LOGDAY%.json


set POWDAYPATH=%BASEPATH%\pow_day
::refresh - 실시간 최소간격 2초, 저장 = 다음날 전날 데이터를 저장하는 것이 적당함

curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow_day?userIdx=%USERIDX1%&logDay=%YESTERDAY%&key=%KEY%" > %POWDAYPATH%\%USERIDX1%\%YESTERDAY%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow_day?userIdx=%USERIDX2%&logDay=%YESTERDAY%&key=%KEY%" > %POWDAYPATH%\%USERIDX2%\%YESTERDAY%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow_day?userIdx=%USERIDX3%&logDay=%YESTERDAY%&key=%KEY%" > %POWDAYPATH%\%USERIDX3%\%YESTERDAY%.json


