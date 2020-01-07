class FileLoader:
	def __init__(self):
		self.dataFileName = "./static/1.input"
		self.lineLen = [115, 30, 20, 20]
		self.matrials = []

		self.splitTexts = []
		self.splitTexts.append("! No. type         I         J                   K\n") # type 1 and 2
		#self.splitTexts.append("! No. type         I         J                   K\n") # type 3 (duplicate)
		self.splitTexts.append("       0.5       0.5        50       100        \n") # type 4
		
		self.dataIndex = []
		self.numberOfMatrial = 4
