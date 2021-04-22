set root=C:\Users\rct32\anaconda3
call %root%\Scripts\activate.bat

call conda activate detect

set cctv=%1
set direction=%2
set startPoint=%3

call python detector.py --cctv_id="%cctv%" --news="%direction%" --start="%startPoint%"


EXIT