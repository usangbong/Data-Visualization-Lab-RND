from flask import Flask, render_template, request, redirect

from nl4dv import NL4DV
import missingno as msno
import pandas as pd
import json
import os

cnt_create = 0
create_div = ''
create_vlSpec = ''

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", create_div = create_div, create_vlSpec = create_vlSpec, fig = 'fig.png')

@app.route('/input_query', methods=['GET', 'POST'])
def input_query():
    file_name = "movies-w-year.csv"
    data = pd.read_csv(file_name)
    data = data.to_dict('records')

    # Initialize an instance of NL4DV
    # ToDo: verify the path to the source data file. modify accordingly.
    nl4dv_instance = NL4DV(data_url = os.path.join(file_name))

    # using Spacy
    # ToDo: ensure that the below spacy model is installed. if using another model, modify accordingly.
    dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}

    # Set the Dependency Parser
    nl4dv_instance.set_dependency_parser(config = dependency_parser_config)
    
    if request.method == 'POST':
        result = request.form
        query = result['input_query']
        
        # Execute the query
        output = nl4dv_instance.analyze_query(query)

        # attributes, tasks, visType
        attributes = output['visList'][0]['attributes']
        tasks = output['visList'][0]['tasks']
        visType = output['visList'][0]['visType']

        if type(attributes) == list:
            attributes = ",".join(attributes)
        if type(tasks) == list:
            tasks = ",".join(tasks)
        if type(visType) == list:
            visType = ",".join(visType)

        # 예외처리 구현 필요
        # 값이 "으로 시작하지 않으면 키 - 값 삭제
        vlSpec = output['visList'][0]['vlSpec']
        del vlSpec['mark']['tooltip']
        del vlSpec['encoding']['x']['aggregate']
        del vlSpec['encoding']['y']['aggregate']
        del vlSpec['data']['url']
        del vlSpec['data']['format']
        vlSpec['data']['values'] = data
        ##########

        global cnt_create, create_div, create_vlSpec
        create_div = create_div + '''
        <div id="vis''' + str(cnt_create) + '''" style="width: 100%; display: flex; justify-content: space-between; flex-wrap: wrap;">
            <div id="list" style="width: 33%; height: 300px;">
                <p>attributes: ''' + attributes + '''</p>
                <p>tasks: ''' + tasks + '''</p>
                <p>visType: ''' + visType + '''</p>
            </div>
            <div id="vlSpec" style="width: 33%; height: 300px;"></div>
            <div id="recommend" style="width: 33%; height: 300px;">
                <p>attributes: ''' + attributes + '''</p>
                <p>tasks: ''' + tasks + '''</p>
                <p>action: example </p>
                <p>action: example </p>
                <p>action: example </p>
                <br>
            </div>
        </div>
        '''

        create_vlSpec = create_vlSpec + '''
        var vlSpec = ''' + str(vlSpec) + ''';
        vegaEmbed('#vis''' + str(cnt_create) + ''' #vlSpec', vlSpec);
        '''
        cnt_create = cnt_create + 1

    return redirect('/')

@app.route('/node_overview', methods=['GET', 'POST'])
def node_overview():
    file_name = request.get_data()
    file_name = file_name.decode('utf-8')
    data = pd.read_csv(file_name)

    fig = msno.matrix(data).get_figure()
    fig.savefig('static/fig.png')

    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)