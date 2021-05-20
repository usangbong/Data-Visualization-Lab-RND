@echo off

set YEAR=%date:~6,4%
set MONTH=%date:~0,2%
set DAY=%date:~3,2%
set LOGDAY=%YEAR%%MONTH%%DAY%
set HOUR=%time:~0,2%
set MINUTE=%time:~3,2%


SET HOUR=%time:~0,2%
SET dtStamp9=0%time:~1,1%%time:~3,2%%time:~6,2%
SET dtStamp24=%time:~0,2%%time:~3,2%%time:~6,2%

if "%HOUR:~0,1%" == " " (SET dtStamp=%dtStamp9%) else (SET dtStamp=%dtStamp24%)

echo %dtStamp%

set LOGTIME=%LOGDAY%_%dtStamp%
echo %LOGTIME%

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

set POWPATH=%BASEPATH%\pow
::refresh - 매 5분

curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow?userIdx=%USERIDX1%&key=%KEY%" > %POWPATH%\%USERIDX1%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow?userIdx=%USERIDX2%&key=%KEY%" > %POWPATH%\%USERIDX2%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/usr/pow?userIdx=%USERIDX3%&key=%KEY%" > %POWPATH%\%USERIDX3%\%LOGTIME%.json

set INVNOWPATH=%BASEPATH%\inv_now
::refresh - 매 5분

curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/now?userIdx=%USERIDX1%&key=%KEY%" > %INVNOWPATH%\%USERIDX1%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/now?userIdx=%USERIDX2%&key=%KEY%" > %INVNOWPATH%\%USERIDX2%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/now?userIdx=%USERIDX3%&key=%KEY%" > %INVNOWPATH%\%USERIDX3%\%LOGTIME%.json

set INVACHISTPATH=%BASEPATH%\inv_achist
::refresh - 매 5분

curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID11%&key=%KEY%" > %INVACHISTPATH%\%USERIDX1%\%INVOID11%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID12%&key=%KEY%" > %INVACHISTPATH%\%USERIDX1%\%INVOID12%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID13%&key=%KEY%" > %INVACHISTPATH%\%USERIDX1%\%INVOID13%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID14%&key=%KEY%" > %INVACHISTPATH%\%USERIDX1%\%INVOID14%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID21%&key=%KEY%" > %INVACHISTPATH%\%USERIDX2%\%INVOID21%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID22%&key=%KEY%" > %INVACHISTPATH%\%USERIDX2%\%INVOID22%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID23%&key=%KEY%" > %INVACHISTPATH%\%USERIDX2%\%INVOID23%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID24%&key=%KEY%" > %INVACHISTPATH%\%USERIDX2%\%INVOID24%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID25%&key=%KEY%" > %INVACHISTPATH%\%USERIDX2%\%INVOID25%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID31%&key=%KEY%" > %INVACHISTPATH%\%USERIDX3%\%INVOID31%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID32%&key=%KEY%" > %INVACHISTPATH%\%USERIDX3%\%INVOID32%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID33%&key=%KEY%" > %INVACHISTPATH%\%USERIDX3%\%INVOID33%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/ac_hist?oid=%INVOID34%&key=%KEY%" > %INVACHISTPATH%\%USERIDX3%\%INVOID34%\%LOGTIME%.json

set INVDCHISTPATH=%BASEPATH%\inv_dchist
::refresh - 매 5분

curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID11%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX1%\%INVOID11%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID12%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX1%\%INVOID12%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID13%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX1%\%INVOID13%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID14%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX1%\%INVOID14%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID21%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX2%\%INVOID21%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID22%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX2%\%INVOID22%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID23%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX2%\%INVOID23%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID24%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX2%\%INVOID24%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID25%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX2%\%INVOID25%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID31%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX3%\%INVOID31%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID32%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX3%\%INVOID32%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID33%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX3%\%INVOID33%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/dc_hist?oid=%INVOID34%&key=%KEY%" > %INVDCHISTPATH%\%USERIDX3%\%INVOID34%\%LOGTIME%.json

set INVRSTPATH=%BASEPATH%\inv_rst
::refresh - 매 5분

curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID11%&key=%KEY%" > %INVRSTPATH%\%USERIDX1%\%INVOID11%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID12%&key=%KEY%" > %INVRSTPATH%\%USERIDX1%\%INVOID12%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID13%&key=%KEY%" > %INVRSTPATH%\%USERIDX1%\%INVOID13%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID14%&key=%KEY%" > %INVRSTPATH%\%USERIDX1%\%INVOID14%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID21%&key=%KEY%" > %INVRSTPATH%\%USERIDX2%\%INVOID21%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID22%&key=%KEY%" > %INVRSTPATH%\%USERIDX2%\%INVOID22%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID23%&key=%KEY%" > %INVRSTPATH%\%USERIDX2%\%INVOID23%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID24%&key=%KEY%" > %INVRSTPATH%\%USERIDX2%\%INVOID24%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID25%&key=%KEY%" > %INVRSTPATH%\%USERIDX2%\%INVOID25%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID31%&key=%KEY%" > %INVRSTPATH%\%USERIDX3%\%INVOID31%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID32%&key=%KEY%" > %INVRSTPATH%\%USERIDX3%\%INVOID32%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID33%&key=%KEY%" > %INVRSTPATH%\%USERIDX3%\%INVOID33%\%LOGTIME%.json
curl -X GET --header "Accept: application/json" "http://222.102.213.46:8096/api/inv/rst?oid=%INVOID34%&key=%KEY%" > %INVRSTPATH%\%USERIDX3%\%INVOID34%\%LOGTIME%.json
