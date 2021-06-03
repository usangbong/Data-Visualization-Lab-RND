@echo TESTESTESTEST
rem (C):HYEYEON, (D):PROFESSOR(D), (Y):VIS
set BASEPATH=D:\elsys\solar

set SENSORPATH=%BASEPATH%\_SENSOR
set KPXPATH=%BASEPATH%\_KPX
set OMNPATH=%BASEPATH%\_OMN

set RSRSID1=RSRS0000000239
set RSRSID2=RSRS0000000241
set RSRSID3=RSRS0000000247
set RSRSID4=RSRS0000000249

rem Environmental sensor
mkdir %SENSORPATH%\json
mkdir %SENSORPATH%\csv

rem KPX previous day
rem curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_pre?rsrsId=%RSRSID1%" > %KPXPATH%\%RSRSID1%\%LOGDAY%.json

rem KPX power
mkdir %KPXPATH%\json_%RSRSID1%
mkdir %KPXPATH%\json_%RSRSID2%
mkdir %KPXPATH%\json_%RSRSID3%
mkdir %KPXPATH%\json_%RSRSID4%
mkdir %KPXPATH%\csv_%RSRSID1%
mkdir %KPXPATH%\csv_%RSRSID2%
mkdir %KPXPATH%\csv_%RSRSID3%
mkdir %KPXPATH%\csv_%RSRSID4%

rem ONM power
mkdir %OMNPATH%\json_%RSRSID1%
mkdir %OMNPATH%\json_%RSRSID2%
mkdir %OMNPATH%\json_%RSRSID3%
mkdir %OMNPATH%\json_%RSRSID4%
mkdir %OMNPATH%\csv_%RSRSID1%
mkdir %OMNPATH%\csv_%RSRSID2%
mkdir %OMNPATH%\csv_%RSRSID3%
mkdir %OMNPATH%\csv_%RSRSID4%

pause