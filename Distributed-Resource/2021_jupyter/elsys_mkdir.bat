@echo TESTESTESTEST

set BASEPATH=C:\solar\HY_TEST
set SENSORPATH=%BASEPATH%\SENSOR
set KPXPATH=%BASEPATH%\KPX
set OMNPATH=%BASEPATH%\OMN

set RSRSID1=RSRS0000000239
set RSRSID2=RSRS0000000241
set RSRSID3=RSRS0000000247
set RSRSID4=RSRS0000000249

rem Environmental sensor
mkdir %SENSORPATH%\%RSRSID1%
mkdir %SENSORPATH%\%RSRSID2%
mkdir %SENSORPATH%\%RSRSID3%
mkdir %SENSORPATH%\%RSRSID4%

rem KPX previous day
rem curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_pre?rsrsId=%RSRSID1%" > %KPXPATH%\%RSRSID1%\%LOGDAY%.json

rem KPX power
mkdir %KPXPATH%\%RSRSID1%
mkdir %KPXPATH%\%RSRSID2%
mkdir %KPXPATH%\%RSRSID3%
mkdir %KPXPATH%\%RSRSID4%

rem ONM power
mkdir %OMNPATH%\%RSRSID1%
mkdir %OMNPATH%\%RSRSID2%
mkdir %OMNPATH%\%RSRSID3%
mkdir %OMNPATH%\%RSRSID4%

pause