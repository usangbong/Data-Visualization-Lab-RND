**Data collection**
- python
- PyQt5
- local database <mysql>


[2020.08.10] usangbong@gmail.com

**database mysql table**
- id(VARCHAR): user id
- sti(VARCHAR): stimulus (image) file name (ex. categoryname_image file name)
- t(INT): time
- t_order(INT): time order of gaze points in same time
- img_w(INT): stimulus image width
- img_h(INT): stimulus image height
- sti_x(INT): stimulus image x-coordinate position on Painter
- sti_y(INT): stimulus image y-coordinate position on Painter
- left_x(DOUBLE): x-coordinate of gaze point from left eye
- left_y(DOUBLE): y-coordinate of gaze point from left eye
- right_x(DOUBLE): x-coordinate of gaze point from right eye
- right_y(DOUBLE): y-coordinate of gaze point from right eye
- avg_x(DOUBLE): average x-coordinate of both eyes
- avg_y(DOUBLE): average y-coordinate of both eyes
- left_validity(INT): out of range flag (0: stimulus out, 1: stimlus in) from left eye
- right_validity(INT): out of range flag (0: stimulus out, 1: stimlus in) from right eye
- true_validity(INT): gaze point in stimlus (0: stimulus out, 1: stimlus in) from both eyes


[2020.01.20] kimyejin.kr@gmail.com

**python 3.6**
- pip install pyautogui
- pip install PyQt5
- pip install PyMySQL
- pip install tobii-research
