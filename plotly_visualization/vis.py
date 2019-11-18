# python version 3.5x
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


G_FILENAME_ARR=[]
class VisFunctions :
	def vistypeDetection(self, _htmlFileName, _d,_m, _vis, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pdDataset):
		self.funcName = "_"+str(_d)+"d"+str(_m)+"m_"+str(_vis)
		self.case = getattr(self, "callVisFunctions", lambda:"default")
		#print(self.funcName)
		return self.case( _htmlFileName, self.funcName, _d,_m, _dimIdxArr, _meaIdxArr, _vis, _arrColumn, _arrData, _pdDataset)

	def callVisFunctions(self, _htmlFileName, _funcName, _d,_m, _dimIdxArr, _meaIdxArr, _vis, _arrColumn, _arrData, _pdDataset) :
		if _d == 0 : #d==0, m>=1 ##only for pandas format  #print(G_FILENAME_ARR, _d,_m, _dimIdxArr, _meaIdxArr, _vis)
			tempArrForFuncCall = []
			tempArrForFuncCall2 = []
			for j in range(len(_meaIdxArr)):
				tempArrForFuncCall.append(_arrColumn[_meaIdxArr[j]])
				tempArrForFuncCall2.append(_arrData[_meaIdxArr[j]])
			t = getattr(self, _funcName, lambda:"default")
			if _m==2 :  
				if _vis=="scatter" :
					t(_htmlFileName, tempArrForFuncCall2[0], tempArrForFuncCall2[1]) 
				else :
					t(_htmlFileName, _pdDataset, tempArrForFuncCall[0], tempArrForFuncCall[1]) 
			elif _m==3 :
				t(_htmlFileName, _pdDataset, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2])
				
		elif _m == 0 : #d=>1, m==0 ##only for pandas format ##disabled for this version #print(G_FILENAME_ARR, _d,_m, _dimIdxArr, _meaIdxArr, _vis)
			for i in range(len(_dimIdxArr)):
				print(_dimIdxArr[i])
				
		elif _d==1 : #d==1 m>=1
			for i in range(len(_dimIdxArr)):
				tempArrForFuncCall = []
				#print(G_FILENAME_ARR, _d,_m, _dimIdxArr, _meaIdxArr, _vis)
				tempArrForFuncCall.append(_arrData[_dimIdxArr[i]])
				for j in range(len(_meaIdxArr)):
					tempArrForFuncCall.append(_arrColumn[_meaIdxArr[j]])
					tempArrForFuncCall.append(_arrData[_meaIdxArr[j]])
			t = getattr(self, _funcName, lambda:"default")
			if _m==1 :
				t(_htmlFileName, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2])
			elif _m==2 : 
				t(_htmlFileName, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2], tempArrForFuncCall[3], tempArrForFuncCall[4])
			elif _m==3 :
				t(_htmlFileName, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2], tempArrForFuncCall[3], tempArrForFuncCall[4], tempArrForFuncCall[5], tempArrForFuncCall[6])
		else : #d>1 m>=1
			print("!!!!!!!!")
			
	
		
