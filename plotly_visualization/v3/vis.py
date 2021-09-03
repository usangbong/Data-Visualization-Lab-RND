# python version 3.5x
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

G_FILENAME_ARR=[]

class VisFunctions :
	def __init__(self):
		self.dummyarray = []
		
	def write_html_png_and_print_log(self, _FileName, _fig, _FunctionName):
		flag=True
		try:
			_fig.write_html(_FileName+".html", auto_open=False)
			_fig.write_image(_FileName+".png")
		except OSError:
			flag=False
		print_str = "[2]["+_FunctionName+"]["+("success" if flag else "fail")+"]["+_FileName+".html]"
		print(print_str)
		
	def vistypeDetection(self, _htmlFileName, _d,_m, _vis, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pdDataset):
		self.funcName = "_"+str(_d)+"d"+str(_m)+"m_"+str(_vis)
		self.case = getattr(self, "callVisFunctions", lambda:"default")
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
				t(_htmlFileName, tempArrForFuncCall2[0], tempArrForFuncCall2[1], _pdDataset) 
			elif _m==3 :
				t(_htmlFileName, _pdDataset, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2], _pdDataset)
				
		elif _m == 0 : 
			self.dummyarray.append(_htmlFileName.split('/')[2])
			
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
				t(_htmlFileName, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2], _pdDataset)
			elif _m==2 : 
				t(_htmlFileName, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2], tempArrForFuncCall[3], tempArrForFuncCall[4], _pdDataset)
			elif _m==3 :
				t(_htmlFileName, tempArrForFuncCall[0], tempArrForFuncCall[1], tempArrForFuncCall[2], tempArrForFuncCall[3], tempArrForFuncCall[4], tempArrForFuncCall[5], tempArrForFuncCall[6], _pdDataset)
				
		elif _d == -1 : #geo
			longIdx = _dimIdxArr
			latIdx = _meaIdxArr
			_funcName = '_'+_funcName.split('_')[2]
			t = getattr(self, _funcName, lambda:"default")
			t(_htmlFileName, latIdx, longIdx, _pdDataset)
			
		elif _d == -2 : #geo_with_measure
			longIdx = _dimIdxArr
			latIdx = _meaIdxArr
			_funcName = '_'+_funcName.split('_')[2]
			t = getattr(self, _funcName, lambda:"default")
			t(_htmlFileName, _m, latIdx, longIdx, _pdDataset)
			
			#print(self, _htmlFileName, _funcName, _d,_m, _dimIdxArr, _meaIdxArr, _vis, _arrColumn, _arrData, _pdDataset)
		elif _d == -3 : #staticsVis
			_funcName = '_'+_funcName.split('_')[2]
			t = getattr(self, _funcName, lambda:"default")
			t(_htmlFileName, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pdDataset)
			
		else :
			print("Error!!!!!!!!")
	
	def _pcaView(self, _FileName, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pandasDataset):
		arrays = []
		for i in range(len(_meaIdxArr[1])):
			arrays.append(_meaIdxArr[1][i][0])
		features = [];
		for idx in arrays :
			features.append(_arrColumn[idx])
			
		pca = PCA()
		components = pca.fit_transform(_pandasDataset[features])
		labels = {str(i): f"PC {i+1} ({var:.1f}%)"	for i, var in enumerate(pca.explained_variance_ratio_ * 100)	}
		fig = px.scatter_matrix(components, labels=labels, dimensions=range(len(arrays)))
		fig.update_traces(diagonal_visible=False)
		fig.update_layout(title_text = "pcaView")
		self.write_html_png_and_print_log(_FileName, fig, "pcaView")
		
	def _parrallelCoord(self, _FileName, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pandasDataset):
		fig = px.parallel_coordinates(_pandasDataset)
		fig.update_layout(title_text = "parrallelCoord")
		self.write_html_png_and_print_log(_FileName, fig, "parrallelCoord")
		
			
	def _statisticalSplitViolin(self, _FileName, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pandasDataset):
		arrays = []
		for i in range(len(_meaIdxArr[1])):
			arrays.append(_meaIdxArr[1][i][0])
		
		
		tx = [];		ty = [];		tpe = [];		tme = []
		tempdata = _pandasDataset.copy()
		
		for idx in arrays :
			tx.append(_arrColumn[idx])
			tempmean = _pandasDataset[_arrColumn[idx]].mean()
			temparr = []
			for data in _pandasDataset[_arrColumn[idx]] : 
				if data>tempmean :
					temparr.append("high")
				else :
					temparr.append("low")
			tempdata[(_arrColumn[idx]+"mean")] = temparr
			ty.append(tempmean)
		#print(tempdata)
		#tempdata = _pandasDataset.copy()
		
		fig = make_subplots(rows=1, cols=len(arrays))
		for idx in arrays :
			fig.add_trace(	
				go.Violin(
					y=tempdata[_arrColumn[idx]][tempdata[(_arrColumn[idx]+"mean")] == "high"], 
					legendgroup='High', scalegroup='High', name='High',
					meanline_visible=True,
					side='negative', 
					line_color = 'blue',
					x0=_arrColumn[idx]
				), 
				row=1, 
				col=idx
			)
			fig.add_trace(	go.Violin(y=tempdata[_arrColumn[idx]][tempdata[(_arrColumn[idx]+"mean")] == "low"], x0=_arrColumn[idx], legendgroup='Low', scalegroup='Low', name='Low', meanline_visible=True, side='positive', line_color = 'orange'), row=1, col=idx)
		fig.update_layout(title_text = "statisticalSplitViolin")
		fig.update_layout(violingap=0, violinmode='overlay')
		self.write_html_png_and_print_log(_FileName, fig, "statisticalSplitViolin")
		
	def _statisticalViolin(self, _FileName, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pandasDataset):
		arrays = []
		for i in range(len(_meaIdxArr[1])):
			arrays.append(_meaIdxArr[1][i][0])
		tx = [];		ty = [];		tpe = [];		tme = []
		for idx in arrays :
			tx.append(_arrColumn[idx])
			ty.append(_pandasDataset[_arrColumn[idx]].mean())
			tempstd = _pandasDataset[_arrColumn[idx]].std()
			tpe.append(tempstd)
			tme.append(-tempstd)
		fig = make_subplots(rows=1, cols=len(arrays))
		for idx in arrays :
			fig.add_trace(	go.Violin(y=_pandasDataset[_arrColumn[idx]], box_visible=True, line_color='black', meanline_visible=True, fillcolor='lightseagreen', opacity=0.6, x0=_arrColumn[idx]), row=1, col=idx)
		fig.update_layout(title_text = "statisticalViolin")
		self.write_html_png_and_print_log(_FileName, fig, "statisticalViolin")
		
	
	def _0d2m_1dhistogram(self,  _FileName, _name1, _data1, _pandasDataset, _type='group', _color=['indianred', 'lightsalmon'], _xaxis=None) :
		fig = px.histogram(_pandasDataset, x=_name1, marginal="violin", title="1d_histogram")
		self.write_html_png_and_print_log(_FileName, fig, "1d_histogram ")
		
	def _0d2m_cumulate_histogram(self,  _FileName, _name1, _data1, _pandasDataset, _type='group', _color=['indianred', 'lightsalmon'], _xaxis=None) :
		fig = go.Figure(data=[go.Histogram(x=_data1, cumulative_enabled=True, marker_color='#330C73')])
		fig.update_layout(title="cumulate_histogram")
		self.write_html_png_and_print_log(_FileName, fig, "cumulate_histogram ")
		
	def _1d2m_overlay_histogram(self, _FileName, _dim, _name1, _data1, _name2, _data2, _pandasDataset, _type='group', _color=['indianred', 'lightsalmon'], _xaxis=None) :
		fig = go.Figure()
		fig.add_trace(go.Histogram(x=_data1, name=_name1))
		fig.add_trace(go.Histogram(x=_data2, name=_name2))
		fig.update_layout(barmode='overlay', title="overlay_histogram")
		fig.update_traces(opacity=0.75)
		self.write_html_png_and_print_log(_FileName, fig, "overlay_histogram")
		
	def _1d3m_md_histogram(self, _FileName, _dim, _name1, _data1, _name2, _data2, _name3, _data3, _pandasDataset, _type='group', _color=['indianred', 'lightsalmon'], _xaxis=None) :
		fig = px.histogram(_pandasDataset, x=_name1, y=_name2, color=_dim, marginal="violin", hover_data=[_name3], title="mdhistogram")
		self.write_html_png_and_print_log(_FileName, fig, "mdhistogram")
		
	def _geoHexBin(self, _FileName, _latIdx, _longIdx, _pandasDataset) :
		fig = ff.create_hexbin_mapbox(
			    data_frame=_pandasDataset, lat=_pandasDataset.columns[_latIdx-1], lon=_pandasDataset.columns[_longIdx-1],
			    nx_hexagon=10, opacity=0.5, labels={"color": "Point Count"},
			    min_count=1, color_continuous_scale="Viridis",
			    show_original_data=True,
			    original_data_marker=dict(size=4, opacity=0.6, color="deeppink")
			)
			
		fig.update_layout(mapbox_style="dark", mapbox_accesstoken='pk.eyJ1Ijoia3N5MDU4NiIsImEiOiJja2c1ZjR6ZTQwZjdkMnNxdHFpbnB2NWs3In0.6w1J8FFi0BCIto0vfp6l1w')
		fig.update_layout(title="geoHexBin")
		self.write_html_png_and_print_log(_FileName, fig, "geoHexBin")
		
	def _basicGeo(self, _FileName, _latIdx, _longIdx, _pandasDataset):
		fig = px.scatter_mapbox(_pandasDataset, lat=_pandasDataset.columns[_latIdx-1], lon=_pandasDataset.columns[_longIdx-1], color_discrete_sequence=["fuchsia"], zoom=4)
		fig.update_layout(mapbox_style="open-street-map")
		fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
		fig.update_layout(mapbox_accesstoken='pk.eyJ1Ijoia3N5MDU4NiIsImEiOiJja2c1ZjR6ZTQwZjdkMnNxdHFpbnB2NWs3In0.6w1J8FFi0BCIto0vfp6l1w')
		fig.update_layout(title="basicGeo")
		self.write_html_png_and_print_log(_FileName, fig, "basicGeo")
		
	def _densityMap(self, _FileName, _latIdx, _longIdx, _pandasDataset):
		fig = px.density_mapbox(_pandasDataset, lat=_pandasDataset.columns[_latIdx-1], lon=_pandasDataset.columns[_longIdx-1], radius=15, zoom=4)
		fig.update_layout(mapbox_style="stamen-terrain")
		fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
		fig.update_layout(mapbox_accesstoken='pk.eyJ1Ijoia3N5MDU4NiIsImEiOiJja2c1ZjR6ZTQwZjdkMnNxdHFpbnB2NWs3In0.6w1J8FFi0BCIto0vfp6l1w')
		fig.update_layout(title="densityMap")
		self.write_html_png_and_print_log(_FileName, fig, "densityMap")
		
	def _geoBubbleMapWorld(self, _FileName, _mIdx, _latIdx, _longIdx, _pandasDataset) :
		_centerlat=_pandasDataset.mean(axis = 0)[_latIdx-1]
		_centerlon = _pandasDataset.mean(axis = 0)[_longIdx-1]
		fig = px.scatter_geo(_pandasDataset,  lat=_pandasDataset.columns[_latIdx-1], lon=_pandasDataset.columns[_longIdx-1],
                     size=_pandasDataset.columns[_mIdx-1],
                     color =_pandasDataset.columns[_mIdx-1], title="geoBubbleMapWorld")
		self.write_html_png_and_print_log(_FileName, fig, "geoBubbleMapWorld")
		
	def _geoMapLoc(self, _FileName, _mIdx, _latIdx, _longIdx, _pandasDataset) :
		_centerlat=_pandasDataset.mean(axis = 0)[_latIdx-1]
		_centerlon = _pandasDataset.mean(axis = 0)[_longIdx-1]
		fig = px.scatter_geo(_pandasDataset,  lat=_pandasDataset.columns[_latIdx-1], lon=_pandasDataset.columns[_longIdx-1],
                     center = dict(lon=_centerlon, lat=_centerlat), 
                     size=_pandasDataset.columns[_mIdx-1],
                     color =_pandasDataset.columns[_mIdx-1])
		fig.update_geos(fitbounds="locations", showlakes=True, lakecolor="Blue", showrivers=True, rivercolor="Blue", showcountries=True, countrycolor="RebeccaPurple", showland=True, landcolor="LightGreen", showocean=True, oceancolor="LightBlue")
		fig.update_layout(title="geoMapLoc")
		self.write_html_png_and_print_log(_FileName, fig, "geoMapLoc")
		
	def _1d1m_bar(self, _FileName, _dim, _name, _data, _pandasDataset, _color='indianred', _xaxis=None) :
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
		
		fig.update_layout(title="bar_1d1m")
		self.write_html_png_and_print_log(_FileName, fig, "bar_1d1m")
		
	def _1d2m_bar(self, _FileName, _dim, _name1, _data1, _name2, _data2, _pandasDataset, _type='group', _color=['indianred', 'lightsalmon'], _xaxis=None) :
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
		
		fig.update_layout(title="bar_1d2m")
		self.write_html_png_and_print_log(_FileName, fig, "bar_1d2m")
		
	def _getNormalizeList(self, data):
		temp=data
		datamin, datamax = min(data), max(data)
		for i, val in enumerate(data):
			temp[i] = (val-datamin) / (datamax-datamin)
		return temp
		
	def _1d3m_bar_line(self, _FileName, _dim, _name1, _data1, _name2,_data2, _name3, _data3, _pandasDataset, _lineMode='lines+markers', _type='group', _color=['mediumturquoise','indianred', 'lightsalmon'], _xaxis=None) :
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
		fig.update_layout(title="bar_line_1d3m")
		
		if _xaxis==None :
			fig.update_layout(barmode=_type, xaxis_tickangle=-45)
		else :
			fig.update_layout(barmode=_type, xaxis_tickangle=-45, xaxis=_xaxis)
		self.write_html_png_and_print_log(_FileName, fig, "bar_line_1d3m")
		
	def _1d1m_pie(self, _FileName, _dim, _name1, _data, _pandasDataset) :
		_color=['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)', 'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)', 'rgb(217,217,217)', 'rgb(188,128,189)', 'rgb(204,235,197)', 'rgb(255,237,111)']
		fig = go.Figure()
		fig.add_trace(go.Pie(
			labels=_dim,
			values=_data,
			text = _data,
			textposition='auto'
		))
		
		fig.update_traces(hoverinfo='label+percent+name', textinfo='none')
		fig.update_layout(title="pie_1d1m")
		self.write_html_png_and_print_log(_FileName, fig, "pie_1d1m")
		
	def _0d2m_scatter(self, _FileName, _data1, _data2, _pandasDataset) :
		fig = go.Figure(data=go.Scatter(x=_data1, y=_data2, mode='markers'))
		fig.update_layout(title="scatter_0d2m")
		self.write_html_png_and_print_log(_FileName, fig, "scatter_0d2m")
		
	def _0d2m_pandas_scatter(self, _FileName, _xaxis, _yaxis, _pandasDataset) :
		fig = px.scatter(_pandasDataset, x=_xaxis, y=_yaxis, title="scatter_0d2m")
		self.write_html_png_and_print_log(_FileName, fig, "scatter_0d2m")
		
	def _2d0m_pandas_scatter(self, _FileName, _xaxis, _yaxis, _pandasDataset) :
		fig = px.scatter(_pandasDataset, x=_xaxis, y=_yaxis, title="scatter_2d0m")
		self.write_html_png_and_print_log(_FileName, fig, "scatter_2d0m")
		
	def _2d1m_pandas_scatter(self, _FileName, _xaxis, _yaxis, _coloraxis, _pandasDataset) :
		fig = px.scatter(_pandasDataset, x=_xaxis, y=_yaxis, color=_coloraxis, marginal_y="histogram", marginal_x="histogram", title="scatter_2d1m")
		self.write_html_png_and_print_log(_FileName, fig, "scatter_2d1m")
		
	def _all_pandas_scatter(self, _FileName, _pandasDataset) :
		fig = px.scatter_matrix(_pandasDataset, title="scatter_all")
		self.write_html_png_and_print_log(_FileName, fig, "scatter_all")
		
	def _0d2m_heatmap(self, _FileName, _xaxis, _yaxis, _pandasDataset) :
		fig = px.density_heatmap(_pandasDataset, x=_xaxis, y=_yaxis, marginal_y="histogram", marginal_x="histogram", title="heatmap_0d2m")
		self.write_html_png_and_print_log(_FileName, fig, "heatmap_0d2m")
		
	def _2d0m_heatmap(self, _FileName, _xaxis, _yaxis, _pandasDataset) :
		fig = px.density_heatmap(_pandasDataset, x=_xaxis, y=_yaxis, marginal_y="histogram", marginal_x="histogram", title="heatmap_2d0m")
		self.write_html_png_and_print_log(_FileName, fig, "heatmap_2d0m")
