class DataToMat:
	def __init__(self):
		self.matrix = []
		self.numberOfNode = 115
	
	def setNodeNumber(self, _nodeNum):
		self.numberOfNode = _nodeNum
	
	def setMatrialNumber(self, _matrial_type_num):
		self.numberOfMatrialType = _matrial_type_num

	def makeMatrixFrame(self):
		self.rows = []
		
		for i in range(0, self.numberOfNode):
			self._row = []
			for j in range(0, self.numberOfNode):
				self._row.append(0)
			self.rows.append(self._row)
		self.matrix = self.rows
