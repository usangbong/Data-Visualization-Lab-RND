@echo off
rem (C):HYEYEON, (D):PROFESSOR(D), (Y):VIS
set BASEPATH=D:\elsys\solar
set VIS_PATH=Y:\elsys\solar

rem 1:sensor, 2:KPX, 3:ONM
set DATA_MODE=1
set VIS_PATH_YN=N
set START_DATE=20210128
set END_DATE=20210530

set SENSORPATH=%BASEPATH%\_SENSOR
set KPXPATH=%BASEPATH%\_KPX
set OMNPATH=%BASEPATH%\_OMN

set RSRSID1=RSRS0000000239
set RSRSID2=RSRS0000000241
set RSRSID3=RSRS0000000247
set RSRSID4=RSRS0000000249

set BASE_DATE=%END_DATE%

:_LOOP

echo ================================================================================
echo                                                            %BASE_DATE%
echo ================================================================================
set BASE_DATE_HYPHEN=%BASE_DATE:~0,4%-%BASE_DATE:~4,2%-%BASE_DATE:~6,2%
rem -------------------------------------------------------
rem                GET ELSYS API
rem -------------------------------------------------------

rem 1. Environmental sensor
if %DATA_MODE%==1 (
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_weather?searchDay=%BASE_DATE_HYPHEN%" > %SENSORPATH%\json\%BASE_DATE%.json

    if %VIS_PATH_YN%==Y (
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_weather?searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_SENSOR\json\%BASE_DATE%.json
    )
)
rem 2. KPX power
if %DATA_MODE%==2 (
    rem curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_pre?rsrsId=%RSRSID1%" > %KPXPATH%\%RSRSID1%\%LOGDAY%.json
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID1%&searchDay=%BASE_DATE_HYPHEN%" > %KPXPATH%\json_%RSRSID1%\%BASE_DATE%.json
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID2%&searchDay=%BASE_DATE_HYPHEN%" > %KPXPATH%\json_%RSRSID2%\%BASE_DATE%.json
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID3%&searchDay=%BASE_DATE_HYPHEN%" > %KPXPATH%\json_%RSRSID3%\%BASE_DATE%.json
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID4%&searchDay=%BASE_DATE_HYPHEN%" > %KPXPATH%\json_%RSRSID4%\%BASE_DATE%.json

    if %VIS_PATH_YN%==Y (
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID1%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_KPX\json_%RSRSID1%\%BASE_DATE%.json
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID2%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_KPX\json_%RSRSID2%\%BASE_DATE%.json
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID3%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_KPX\json_%RSRSID3%\%BASE_DATE%.json
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/kpx_patn_searchDay?rsrsId=%RSRSID4%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_KPX\json_%RSRSID4%\%BASE_DATE%.json
    )
)
rem 3. ONM power
if %DATA_MODE%==3 (
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID1%&searchDay=%BASE_DATE_HYPHEN%" > %OMNPATH%\json_%RSRSID1%\%BASE_DATE%.json
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID2%&searchDay=%BASE_DATE_HYPHEN%" > %OMNPATH%\json_%RSRSID2%\%BASE_DATE%.json
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID3%&searchDay=%BASE_DATE_HYPHEN%" > %OMNPATH%\json_%RSRSID3%\%BASE_DATE%.json
    curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID4%&searchDay=%BASE_DATE_HYPHEN%" > %OMNPATH%\json_%RSRSID4%\%BASE_DATE%.json
        
    if %VIS_PATH_YN%==Y (
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID1%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_OMN\json_%RSRSID1%\%BASE_DATE%.json
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID2%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_OMN\json_%RSRSID2%\%BASE_DATE%.json
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID3%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_OMN\json_%RSRSID3%\%BASE_DATE%.json
        curl -X GET --header "Accept: application/json" "http://222.102.213.48:8099/onm_patn_searchDay?rsrsId=%RSRSID4%&searchDay=%BASE_DATE_HYPHEN%" > %VIS_PATH%\_OMN\json_%RSRSID4%\%BASE_DATE%.json
    )
)

rem -------------------------------------------------------
rem                CALCULATE PREVIOUS DATE
rem -------------------------------------------------------
set yest_yyyy=%BASE_DATE:~0,4%
set yest_mm=%BASE_DATE:~4,2%
set yest_dd=%BASE_DATE:~6,2%
if %yest_mm% lss 10 set yest_mm=%yest_mm:~-1,1%
if %yest_dd% lss 10 set yest_dd=%yest_dd:~-1,1%

rem Not the first of the month, just decrement day.
if not %yest_dd%==1 (
set /a yest_dd = yest_dd - 1
goto :done
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
rem if (%yest_mm% lss 10)&&(%yest_mm:~0,1% != 0) set yest_mm=0%yest_mm%
if %yest_mm% lss 10 set yest_mm=0%yest_mm%
if %yest_dd% lss 10 set yest_dd=0%yest_dd%

set YESTERDAY=%yest_yyyy%%yest_mm%%yest_dd%
set YESTERDAY_HYPHEN=%yest_yyyy%-%yest_mm%-%yest_dd%
set BASE_DATE=%YESTERDAY%
if %YESTERDAY% LSS %START_DATE% goto _BREAK

goto _LOOP

:_BREAK

echo ================================================================================
echo                              DATE: %START_DATE% ~ %END_DATE% 
echo ================================================================================

pause