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
	
	def setFileName(self, _filename):
		self.dataFileName = _filename

	def setDataParameters(self, _linelen, _numberofmatrial):
		self.leneLen = _linelen
		self.numberOfMatrial = _numberofmatrial

	def removeSpace(self):
		for _mat in self.matrials:
			for _r in _mat:
				for i in range(0, len(_r)):
					if _r[i] == '':
						_r.remove('')
						
	def getDataFromInputFile(self):
		with open(self.dataFileName, "r") as file:
			self.data = file.readlines()

		self._strIdx = 0	
		for line in self.data:
			self._strIdx = self._strIdx+1
			if line == self.splitTexts[0]:
				# matrial type 1, 2, and 3
				self.dataIndex.append([self._strIdx, self.lineLen[len(self.dataIndex)]+1])
				continue
			if line == self.splitTexts[1]:
				# matrial type 4
				self.dataIndex.append([self._strIdx, self.lineLen[len(self.dataIndex)]+1])	# matrial type 4-1 (before "! Second layer")
				self.dataIndex.append([self._strIdx+21, self.lineLen[len(self.dataIndex)]+1])	# matrial type 4-2 (after "! Second layer")
				break
		#print(self.dataIndex)

		self._matrials = []
		for matIdx in range(0, self.numberOfMatrial):
			if matIdx == 0 or matIdx == 1:
				self.matData = []
				for i in range(self.dataIndex[matIdx][0], self.dataIndex[matIdx][0]+self.dataIndex[matIdx][1]-1):
					self.matData.append(self.data[i])
				self._matrials.append(self.matData)
			elif matIdx == 2:
				self.matData = []
				for j in range(self.dataIndex[matIdx][0], self.dataIndex[matIdx+1][0]+self.dataIndex[matIdx][1]-1):
					if j == self.dataIndex[matIdx][0] + self.lineLen[matIdx]:
						continue
					self.matData.append(self.data[j])
				self._matrials.append(self.matData)

		# seprate matrial 1 & 2
		#! No. type         I         J                   K
		# remove " " and "\n"
		self._rows = []
		for _m in self._matrials[0]:
			self._row = self.refineRow(_m)
			self._rows.append(self._row)	
		self._m1Rows = []
		self._m2Rows = []
		for _r in self._rows:
			if _r[1] == '1':
				self._m1Rows.append(_r)
			elif _r[1] == '2':
				self._m2Rows.append(_r)
		# matrial 1: append data in matials[0]
		self.matrials.append(self._m1Rows)
		# matrial 2: append data in matials[1]
		self.matrials.append(self._m2Rows)

		# matrial 3
		# remove " " and "\n"
		self._rows = []
		for _m in self._matrials[1]:
			self._row = self.refineRow(_m)
			self._rows.append(self._row)
		# matrial 3: append data in matials[2]
		self.matrials.append(self._rows)

		# matrial 4
		# remove " " and "\n"
		self._rows = []
		for _m in self._matrials[2]:
			self._row = self.refineRow(_m)
			self._rows.append(self._row)
		# matrial 4: append data in matials[3]
		self.matrials.append(self._rows)
		self.removeSpace()

		return self.matrials					
	
