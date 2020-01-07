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
	
	def countLinkedNode(self, _data):
		for _r in _data:
			self.i_index = int(_r[2])
			self.j_index = int(_r[3])
			self.getVal = self.matrix[self.i_index][self.j_index]
			self.getVal = int(self.getVal)
			self.getVal += 1
			self.matrix[self.i_index][self.j_index] = self.getVal
