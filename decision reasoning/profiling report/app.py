from flask import Flask, render_template, request, redirect, flash

import pandas as pd
import numpy as np
import json
import os

from nl4dv import NL4DV
import missingno as msno
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

init = True
cnt_create = 0
create_div = ''
create_overview = ''
create_vlSpec = ''

app = Flask(__name__)
app.secret_key = "vislab"

@app.route('/', methods=['GET', 'POST'])
def index():
    global init
    init = False

    return render_template("index.html", create_div = create_div, create_overview = create_overview, create_vlSpec = create_vlSpec)

@app.route('/input_query', methods=['GET', 'POST'])
def input_query():
    file_name = "movies-w-year.csv"
    data = pd.read_csv(file_name)
    data = data.to_dict('records')

    nl4dv_instance = NL4DV(data_url = os.path.join(file_name))
    dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}
    nl4dv_instance.set_dependency_parser(config = dependency_parser_config)

    result = request.form
    query = result['input_query']
    output = nl4dv_instance.analyze_query(query)

    # exceptions when writing invalid query
    try:
        attributes = output['visList'][0]['attributes']
        tasks = output['visList'][0]['tasks']
        visType = output['visList'][0]['visType']
    except:
        if init == False:   
            flash("please writing valid query")
        return redirect('/')

    # attribute, task, vistype
    if type(attributes) == list:
        attributes = ",".join(attributes)
    if type(tasks) == list:
        tasks = ",".join(tasks)
    if type(visType) == list:
        visType = ",".join(visType)

    # vlspec
    vlSpec = output['visList'][0]['vlSpec']
    vlSpec['data']['values'] = data

    vlSpec['width'] = "container"
    vlSpec['height'] = "container"

    # data without '' del
    if 'encoding' in vlSpec:
        if 'x' in vlSpec['encoding']:
            if 'aggregate' in vlSpec['encoding']['x']:
                del vlSpec['encoding']['x']['aggregate']
    if 'encoding' in vlSpec:
        if 'y' in vlSpec['encoding']:
            if 'aggregate' in vlSpec['encoding']['y']:
                del vlSpec['encoding']['y']['aggregate']
    if 'encoding' in vlSpec:
        if 'x' in vlSpec['encoding']:
            if 'bin' in vlSpec['encoding']['x']:
                del vlSpec['encoding']['x']['bin']
    if 'encoding' in vlSpec:
        if 'color' in vlSpec['encoding']:
            if 'aggregate' in vlSpec['encoding']['color']:
                del vlSpec['encoding']['color']['aggregate']
    del vlSpec['mark']['tooltip']
    del vlSpec['data']['url']

    # exceptions when writing invalid query
    try:
        ##### create div
        global cnt_create, create_div, create_overview, create_vlSpec
        create_div = create_div + '''
        <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-top: 5px; background-color: white; border: 1px solid #D8D8D8;">
            <div id="overview"></div>
            <div id="list">
                <table>
                    <tr>
                        <th>attributes</th>
                        <td>''' + attributes + '''</td>
                    </tr>
                    <tr>
                        <th>tasks</th>
                        <td>''' + tasks + '''</td>
                    </tr>
                    <tr>
                        <th>visType</th>
                        <td>''' + visType + '''</td>
                    </tr>
                </table>
            </div>
            <div id="vlSpec"></div>
        </div>
        '''

    except:
        if init == False:   
            flash("please writing valid query")
        return redirect('/')

    ##### t-sne
    file_name = "static/data/2.2.csv" # current file
    df = pd.read_csv(file_name)
    df = df.fillna(0)
    df_col = list(df.columns)

    # str column del
    for i in range(len(df_col)):
        if df[df_col[i]].dtypes != 'int64' and df[df_col[i]].dtypes != 'float64':
            df = df.drop(df_col[i], axis = 1)

    df = StandardScaler().fit_transform(df)
    df = pd.DataFrame(df)

    tsne = TSNE(random_state = 42)
    tsne_results = tsne.fit_transform(df)
    tsne_results = pd.DataFrame(tsne_results, columns = ['tsne1', 'tsne2'])
    tsne_results.to_csv("static/data/tsne_" + str(cnt_create) + ".csv")

    ##### scatter plot
    create_overview = create_overview + '''
    var margin = {''' + '''top: 10, right: 30, bottom: 30, left: 60},
        width = 300 - margin.left - margin.right,
        height = 250 - margin.top - margin.bottom;

    var svg''' + str(cnt_create) + ''' = d3v4.select("#vis''' + str(cnt_create) + ''' #overview")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    d3v4.csv("static/data/tsne_''' + str(cnt_create) + '''.csv", function(data) {
    var x = d3v4.scaleLinear()
        .domain([-10, 10])
        .range([ 0, width ]);
    svg''' + str(cnt_create) + '''.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3v4.axisBottom(x));

    var y = d3v4.scaleLinear()
        .domain([-10, 10])
        .range([ height, 0]);
    svg''' + str(cnt_create) + '''.append("g")
        .call(d3v4.axisLeft(y));

    svg''' + str(cnt_create) + '''.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d.tsne1); } )
        .attr("cy", function (d) { return y(d.tsne2); } )
        .attr("r", 1.5)
        .style("fill", "#0069D9")
    })
    '''

    ##### vega-embed
    create_vlSpec = create_vlSpec + '''
    var vlSpec = ''' + str(vlSpec) + ''';
    vegaEmbed('#vis''' + str(cnt_create) + ''' #vlSpec', vlSpec, {"actions": false});
    '''

    cnt_create = cnt_create + 1

    return redirect('/')

@app.route('/current_node', methods=['GET', 'POST'])
def current_node():
    data = request.get_data()
    data = data.decode('utf-8')

    data = data.split('&')
    file_name = 'static/data/' + data[0].lstrip('file_name=') + '.csv'
    name = data[1].lstrip('name=')

    ##### create div
    global cnt_create, create_div, create_overview, create_vlSpec
    create_div = create_div + '''
    <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-top: 5px; background-color: white; border: 1px solid #D8D8D8;">
        <div id="node" style="width: 30px; height: 30px; margin: 5px; color: white; background-color: #1B5E20; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">''' + name + '''</div>
        <div id="overview"></div>
        <div id="recommend">
            <div id="recommend1" style="display: flex; width: 100%; height: 20%;">
                <div id="recommend_node1" style="width: 30px; height: 30px; margin: 5px; background-color: lightgray; text-align: center; border: 2px dotted black; border-radius: 50%; line-height: 30px;">0</div>
                <div id="recommend_list1" style="width: 100%; height: 100%; margin: 5px; background-color: lightgray; text-align: left; border: 1px solid; border-radius: 5px;">
                    결측 값 0으로 대체
                    <div id="issue" style="display: flex;">
                        issue 1
                        <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue1_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">30%</div>
                        </div>
                        감소, issue 2
                        <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue2_inner" style="width: 50%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">50%</div>
                        </div>
                        감소, issue 3
                        <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue3_inner" style="width: 80%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">80%</div>
                        </div>
                        감소
                    </div>
                </div>
            </div>
            <br>
            <div id="recommend2" style="display: flex; width: 100%; height: 20%;">
                <div id="recommend_node2" style="width: 30px; height: 30px; margin: 5px; background-color: lightgray; text-align: center; border: 2px dotted black; border-radius: 50%; line-height: 30px;">0</div>
                <div id="recommend_list2" style="width: 100%; height: 100%; margin: 5px; background-color: lightgray; text-align: left; border: 1px solid; border-radius: 5px;">
                    결측 값 평균으로 대체
                    <div id="issue" style="display: flex;">
                        issue 1
                        <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue1_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">30%</div>
                        </div>
                        감소, issue 2
                        <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue2_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">30%</div>
                        </div>
                        감소, issue 3
                        <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue3_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">30%</div>
                        </div>
                        감소
                    </div>
                </div>
            </div>
            <br>
            <div id="recommend3" style="display: flex; width: 100%; height: 20%;">
                <div id="recommend_node3" style="width: 30px; height: 30px; margin: 5px; color: white; background-color: #0D47A1; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">0</div>
                <div id="recommend_list3" style="width: 100%; height: 100%; margin: 5px; background-color: #BBDEFB; text-align: left; border: 1px solid; border-radius: 5px;">
                    결측 행 삭제
                    <div id="issue" style="display: flex;">
                        issue 1
                        <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue1_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">30%</div>
                        </div>
                        감소, issue 2
                        <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue2_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">30%</div>
                        </div>
                        감소, issue 3
                        <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue3_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">30%</div>
                        </div>
                        감소
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''

    ##### t-sne
    df = pd.read_csv(file_name)
    df = df.fillna(0)
    df_col = list(df.columns)

    # str column del
    for i in range(len(df_col)):
        if df[df_col[i]].dtypes != 'int64' and df[df_col[i]].dtypes != 'float64':
            df = df.drop(df_col[i], axis = 1)

    df = StandardScaler().fit_transform(df)
    df = pd.DataFrame(df)

    tsne = TSNE(random_state = 42)
    tsne_results = tsne.fit_transform(df)
    tsne_results = pd.DataFrame(tsne_results, columns = ['tsne1', 'tsne2'])
    tsne_results.to_csv("static/data/tsne_" + str(cnt_create) + ".csv")

    ##### scatter plot
    create_overview = create_overview + '''
    var margin = {''' + '''top: 10, right: 30, bottom: 30, left: 60},
        width = 300 - margin.left - margin.right,
        height = 250 - margin.top - margin.bottom;

    var svg''' + str(cnt_create) + ''' = d3v4.select("#vis''' + str(cnt_create) + ''' #overview")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    d3v4.csv("static/data/tsne_''' + str(cnt_create) + '''.csv", function(data) {
    var x = d3v4.scaleLinear()
        .domain([-10, 10])
        .range([ 0, width ]);
    svg''' + str(cnt_create) + '''.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3v4.axisBottom(x));

    var y = d3v4.scaleLinear()
        .domain([-10, 10])
        .range([ height, 0]);
    svg''' + str(cnt_create) + '''.append("g")
        .call(d3v4.axisLeft(y));

    svg''' + str(cnt_create) + '''.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d.tsne1); } )
        .attr("cy", function (d) { return y(d.tsne2); } )
        .attr("r", 1.5)
        .style("fill", "#0069D9")
    })
    '''

    cnt_create = cnt_create + 1

    return redirect('/')

@app.route('/before_node', methods=['GET', 'POST'])
def before_node():
    data = request.get_data()
    data = data.decode('utf-8')

    data = data.split('&')
    file_name = 'static/data/' + data[0].lstrip('file_name=') + '.csv'
    name = data[1].lstrip('name=')
    state = data[2].lstrip('state=')

    global background_color, border, cnt_create, create_div, create_overview, create_vlSpec
    if state == 'init':
        background_color = '#B71C1C'
        border = '2px solid black'
        color = 'white'
    elif state == 'false':
        background_color = 'white'
        border = '2px dotted black'
        color = 'black'
    else:
        background_color = 'white'
        border = '2px solid black'
        color = 'black'

    ##### create div
    create_div = create_div + '''
    <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-top: 5px; background-color: white; border: 1px solid #D8D8D8;">
        <div id="node" style="width: 30px; height: 30px; margin: 5px; text-align: center; color: ''' + color + '''; background-color: ''' + background_color + '''; border: ''' + border + '''; border-radius: 50%; line-height: 30px;">''' + name + '''</div>
        <div id="overview"></div>
        <div id="recommend">
            <div id="recommend1" style="display: flex; width: 100%; height: 20%;">
                <div id="recommend_node1" style="width: 30px; height: 30px; margin: 5px; color: white; background-color: #B71C1C; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">0</div>
                <div id="recommend_list1" style="width: 100%; height: 100%; margin: 5px; background-color: #FFCDD2; text-align: left; border: 1px solid; border-radius: 5px;">
                    <div id="issue" style="display: flex;">
                        issue 1
                        <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue1_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">30%</div>
                        </div>
                        감소, issue 2
                        <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue2_inner" style="width: 50%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">50%</div>
                        </div>
                        감소, issue 3
                        <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue3_inner" style="width: 80%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">80%</div>
                        </div>
                        감소
                    </div>
                </div>
            </div>
            <br>
            <div id="recommend2" style="display: flex; width: 100%; height: 20%;">
                <div id="recommend_node2" style="width: 30px; height: 30px; margin: 5px; color: white; background-color: #1B5E20; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">0</div>
                <div id="recommend_list2" style="width: 100%; height: 100%; margin: 5px; background-color: #C8E6C9; text-align: left; border: 1px solid; border-radius: 5px;">
                    <div id="issue" style="display: flex;">
                        issue 1
                        <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue1_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">30%</div>
                        </div>
                        감소, issue 2
                        <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue2_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">30%</div>
                        </div>
                        감소, issue 3
                        <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue3_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">30%</div>
                        </div>
                        감소
                    </div>
                </div>
            </div>
            <br>
            <div id="recommend3" style="display: flex; width: 100%; height: 20%;">
                <div id="recommend_node3" style="width: 30px; height: 30px; margin: 5px; color: white; background-color: #0D47A1; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">0</div>
                <div id="recommend_list3" style="width: 100%; height: 100%; margin: 5px; background-color: #BBDEFB; text-align: left; border: 1px solid; border-radius: 5px;">
                    <div id="issue" style="display: flex;">
                        issue 1
                        <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue1_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">30%</div>
                        </div>
                        감소, issue 2
                        <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue2_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">30%</div>
                        </div>
                        감소, issue 3
                        <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                            <div id="issue3_inner" style="width: 30%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">30%</div>
                        </div>
                        감소
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''

    ##### t-sne
    df = pd.read_csv(file_name)
    df = df.fillna(0)
    df_col = list(df.columns)

    # str column del
    for i in range(len(df_col)):
        if df[df_col[i]].dtypes != 'int64' and df[df_col[i]].dtypes != 'float64':
            df = df.drop(df_col[i], axis = 1)

    df = StandardScaler().fit_transform(df)
    df = pd.DataFrame(df)

    tsne = TSNE(random_state = 42)
    tsne_results = tsne.fit_transform(df)
    tsne_results = pd.DataFrame(tsne_results, columns = ['tsne1', 'tsne2'])
    tsne_results.to_csv("static/data/tsne_" + str(cnt_create) + ".csv")

    ##### scatter plot
    create_overview = create_overview + '''
    var margin = {''' + '''top: 10, right: 30, bottom: 30, left: 60},
        width = 300 - margin.left - margin.right,
        height = 250 - margin.top - margin.bottom;

    var svg''' + str(cnt_create) + ''' = d3v4.select("#vis''' + str(cnt_create) + ''' #overview")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    d3v4.csv("static/data/tsne_''' + str(cnt_create) + '''.csv", function(data) {
    var x = d3v4.scaleLinear()
        .domain([-10, 10])
        .range([ 0, width ]);
    svg''' + str(cnt_create) + '''.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3v4.axisBottom(x));

    var y = d3v4.scaleLinear()
        .domain([-10, 10])
        .range([ height, 0]);
    svg''' + str(cnt_create) + '''.append("g")
        .call(d3v4.axisLeft(y));

    svg''' + str(cnt_create) + '''.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d.tsne1); } )
        .attr("cy", function (d) { return y(d.tsne2); } )
        .attr("r", 1.5)
        .style("fill", "#0069D9")
    })
    '''

    cnt_create = cnt_create + 1

    return redirect('/')

@app.route('/recommend_node', methods=['GET', 'POST'])
def recommend_node():
    data = request.get_data()
    data = data.decode('utf-8')

    data = data.split('&')
    file_name = 'static/data/' + data[0].lstrip('file_name=') + '.csv'
    name = data[1].lstrip('name=')
    state = data[2].lstrip('state=')

    global background_color, border, cnt_create, create_div, create_overview, create_vlSpec
    if state == 'recommend':
        background_color = '#0D47A1'
        border = '2px solid black'
        color = 'white'
    else:
        background_color = '#D3D3D3'
        border = '2px dotted black'
        color = 'black'

    ##### create div
    create_div = create_div + '''
    <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-top: 5px; background-color: white; border: 1px solid #D8D8D8;">
        <div id="node" style="width: 30px; height: 30px; margin: 5px; text-align: center; color: ''' + color + '''; background-color: ''' + background_color + '''; border: ''' + border + '''; border-radius: 50%; line-height: 30px;">''' + name + '''</div>
        <div id="missingno"></div>
        <div id="density"></div>
        <div id="ks_test"></div>
    </div>
    '''

    cnt_create = cnt_create + 1

    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)
