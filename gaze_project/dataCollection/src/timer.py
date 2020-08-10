from PyQt5.QtCore import QThread, QTimer, QEventLoop, QTime

class CollectingTimer(QThread):
    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.in_process)
        self.time = QTime(0, 0, 0)
        self.duration = 1000

    def in_process(self):
        self.time = self.time.addMSecs(1)
        if self.time.msecsSinceStartOfDay() >= self.duration:
            self.terminate()
            
    def run(self):
        self.timer.start(1)
        loop = QEventLoop()
        loop.exec_()