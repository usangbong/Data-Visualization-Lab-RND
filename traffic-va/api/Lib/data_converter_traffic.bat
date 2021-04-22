set root=C:\Users\rct32\anaconda3
call %root%\Scripts\activate.bat

call conda activate detect

set prev_time=%1

call python data_converter_traffic.py --prev_time="%prev_time%"

EXIT