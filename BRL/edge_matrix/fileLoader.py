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
	
	def refineRow(self, _rawRow):
		_strs = _rawRow.split(' ')
		_row = []
		for _d in _strs:
			if _d != "":
				_row.append(_d)
		_l = len(_row)
		_td = _row[_l-1].split('\n')
		_row[_l-1] = _td[0]

		_refinedRow = _row
		return _refinedRow
	
