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
			
			
	def _1d1m_bar(self, _FileName, _dim, _name, _data, _color='indianred', _xaxis=None) :
		fig = go.Figure()
		fig.add_trace(go.Bar(
			x=_dim,
			y=_data,
			name=_name,
			marker_color=_color
		))
		if _xaxis==None :
			fig.update_layout(barmode='group', xaxis_tickangle=-45)
		else :
			fig.update_layout(barmode='group', xaxis_tickangle=-45, xaxis=_xaxis)
		flag=True
		try:
			fig.write_html(_FileName+".html", auto_open=False)
			fig.write_image(_FileName+".png")
		except OSError:
			flag=False
		print_str = "[2][bar_1d1m]["+("success" if flag else "fail")+"]["+_FileName+".html]"
		print(print_str)
		#fig.show()
		
		
	def _1d2m_bar(self, _FileName, _dim, _name1, _data1, _name2, _data2, _type='group', _color=['indianred', 'lightsalmon'], _xaxis=None) :
		fig = go.Figure()
		fig.add_trace(go.Bar(
			x=_dim,
			y=_data1,
			name=_name1,
			marker_color=_color[0]
		))
		fig.add_trace(go.Bar(
			x=_dim,
			y=_data2,
			name=_name2,
			marker_color=_color[1]
		))
		if _xaxis==None :
			fig.update_layout(barmode=_type, xaxis_tickangle=-45)
		else :
			fig.update_layout(barmode=_type, xaxis_tickangle=-45, xaxis=_xaxis)
		
		flag=True
		try:
			fig.write_html(_FileName+".html", auto_open=False)
			fig.write_image(_FileName+".png")
		except OSError:
			flag=False
		print_str = "[2][bar_1d2m]["+("success" if flag else "fail")+"]["+_FileName+".html]"
		print(print_str)
		#fig.show()
	
	
	def _1d3m_bar_line(self, _FileName, _dim, _name1, _data1, _name2,_data2, _name3, _data3, _lineMode='lines+markers', _type='group', _color=['mediumturquoise','indianred', 'lightsalmon'], _xaxis=None) :
		fig = go.Figure()
		fig.add_trace(go.Scatter(
			x=_dim,
			y=_data1,
			name=_name1,
			marker_color=_color[0], 
			mode=_lineMode
		))
		fig.add_trace(go.Bar(
			x=_dim,
			y=_data2,
			name=_name2,
			marker_color=_color[1]
		))
		fig.add_trace(go.Bar(
			x=_dim,
			y=_data3,
			name=_name3,
			marker_color=_color[2]
		))
		if _xaxis==None :
			fig.update_layout(barmode=_type, xaxis_tickangle=-45)
		else :
			fig.update_layout(barmode=_type, xaxis_tickangle=-45, xaxis=_xaxis)
		flag=True
		try:
			fig.write_html(_FileName+".html", auto_open=False)
			fig.write_image(_FileName+".png")
		except OSError:
			flag=False
		print_str = "[2][bar_line_1d3m]["+("success" if flag else "fail")+"]["+_FileName+".html]"
		print(print_str)
		#fig.show()		
