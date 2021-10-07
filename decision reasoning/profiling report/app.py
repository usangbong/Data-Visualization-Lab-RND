from flask import Flask, render_template, request, redirect, flash

import pandas as pd
import numpy as np
import json
import os

import imp_list.imputation as imputation
import imp_list.statistics as statistics
import imp_list.div as div
import imp_list.svg as svg

from nl4dv import NL4DV
import missingno as msno
import matplotlib.pyplot as plt

init = True
current = ''
treeData = ''

cnt_create = 0
create_div = ''
create_vlSpec = ''
create_bar = ''
create_heatmap = ''
create_histogram = ''
app = Flask(__name__)
app.secret_key = "vislab"

@app.route('/', methods=['GET', 'POST'])
def index():
    global init, current
    init = False
    current = 'static/data/missing.csv'

    return render_template("index.html", create_div = create_div, create_vlSpec = create_vlSpec, create_bar = create_bar, create_heatmap = create_heatmap, create_histogram = create_histogram)

@app.route('/input_query', methods=['GET', 'POST'])
def input_query():
    global current, cnt_create, create_div, create_vlSpec, create_bar
    file_name = current
    nl4dv_df = pd.read_csv(file_name)
    nl4dv_df = nl4dv_df.dropna()

    nl4dv_df = nl4dv_df.to_dict('records')
    nl4dv_instance = NL4DV(data_url = os.path.join(file_name))
    dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}
    nl4dv_instance.set_dependency_parser(config = dependency_parser_config)

    result = request.form
    query = result['input_query']
    output = nl4dv_instance.analyze_query(query)

    # extraction attribute, task, vistype
    try:
        attributes = output['visList'][0]['attributes']
        tasks = output['visList'][0]['tasks']
        visType = output['visList'][0]['visType']
    except:
        if init == False:   
            flash("please writing valid query")
        return redirect('/')

    if type(attributes) == list:
        attributes = ",".join(attributes)
    if type(tasks) == list:
        tasks = ",".join(tasks)
    if type(visType) == list:
        visType = ",".join(visType)

    # extraction vlspec
    vlSpec = output['visList'][0]['vlSpec']
    vlSpec['data']['values'] = nl4dv_df

    vlSpec['width'] = "container"
    vlSpec['height'] = "container"

    # preprocessing vlspec
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
    del vlSpec['data']['format']
    del vlSpec['data']['url']

    # generation div
    try:
        create_div = create_div + div.input_query_div(cnt_ctreate, attributes, tasks, visType)
    except:
        if init == False:   
            flash("please writing valid query")
        return redirect('/')

    # vlSpec
    create_vlSpec = create_vlSpec + svg.svg_vlSpec(cnt_create, vlSpec)

    cnt_create = cnt_create + 1
    return redirect('/')

@app.route('/current', methods=['GET', 'POST'])
def current():
    data = request.get_data().decode('utf-8').split('&')
    file_name = 'static/data/' + data[0][10:] + '.csv'
    name = data[1][5:]

    global current, cnt_create, create_div, create_bar
    current = file_name

    # generation div
    create_div = create_div + div.current_div(cnt_create, name)

    # barchart - each
    df = pd.read_csv(file_name)
    col = list(df)

    missing = df.isnull().sum().tolist()
    extreme = []

    df = df.dropna()
    for column in df:
        q25 = np.quantile(df[column], 0.25)
        q75 = np.quantile(df[column], 0.75)

        iqr = q75 - q25
        cut_off = iqr * 1.5

        lower, upper = q25 - cut_off, q75 + cut_off
        data1 = df[df[column] > upper]     
        data2 = df[df[column] < lower]

        extreme.append(data1.shape[0] + data2.shape[0])
    
    total = [x + y for x, y in zip(missing, extreme)]
    max_value = max(total)

    new_df = pd.DataFrame({x for x in zip(col, missing, extreme)}, columns = ['index', 'missing', 'extreme'])
    new_df.to_csv("static/data/bar_" + str(cnt_create) + ".csv")
    create_bar = create_bar + svg.svg_bar1(cnt_create, max_value)

    # barchart - total
    create_bar = create_bar + svg.svg_bar2(cnt_create, max_value)

    cnt_create = cnt_create + 1
    return redirect('/')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    data = request.get_data().decode('utf-8').split('&')
    file_name = 'static/data/' + data[0][10:] + '.csv'
    name = data[1][5:]

    # generation div
    global current, cnt_create, create_div, create_heatmap, create_histogram
    create_div = create_div + div.recommend_div(cnt_create, name)
    
    # heatmap - before
    df = pd.read_csv(current)
    col = list(df)
    target_col = 'pm10'

    tmp_index, tmp_y, tmp_value = [], [], []
    data = {}
    for i in range(len(col)):
        tmp_df = df[col[i]]
        for j in range(int(len(df)/20)):
            slice_df = tmp_df.iloc[20*j : 20*(j + 1)]
            value = slice_df.isnull().sum()

            tmp_index.append(col[i])
            tmp_y.append(20*(j + 1))
            tmp_value.append(value)

    data['index'] = tmp_index
    data['y'] = tmp_y
    data['value'] = tmp_value
    
    heatmap_df = pd.DataFrame(data)
    heatmap_df.to_csv("static/data/heatmap1_" + str(cnt_create) + ".csv")
    create_heatmap = create_heatmap + svg.svg_heatmap(cnt_create, col, target_col, 1, 'heatmap_before')

    # heatmap - after
    df = pd.read_csv(file_name)

    tmp_index, tmp_y, tmp_value = [], [], []
    data = {}
    for i in range(len(col)):
        tmp_df = df[col[i]]
        for j in range(int(len(df)/20)):
            slice_df = tmp_df.iloc[20*j : 20*(j + 1)]
            value = slice_df.isnull().sum()

            tmp_index.append(col[i])
            tmp_y.append(20*(j + 1))
            tmp_value.append(value)

    data['index'] = tmp_index
    data['y'] = tmp_y
    data['value'] = tmp_value
    
    heatmap_df = pd.DataFrame(data)
    heatmap_df.to_csv("static/data/heatmap2_" + str(cnt_create) + ".csv")
    create_heatmap = create_heatmap + svg.svg_heatmap(cnt_create, col, target_col, 2, 'heatmap_after')

    # histogram - before
    df = pd.read_csv(current)
    histogram_df = df[target_col].dropna()

    q25 = np.quantile(histogram_df, 0.25)
    q75 = np.quantile(histogram_df, 0.75)

    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off

    histogram_df.to_csv("static/data/histogram1_" + str(cnt_create) + ".csv")
    create_histogram = create_histogram + svg.svg_histogram(cnt_create, col, target_col, lower, upper, 1, 'histogram_before')

    # histogram - after
    df = pd.read_csv(file_name)
    histogram_df = df[target_col].dropna()

    q25 = np.quantile(histogram_df, 0.25)
    q75 = np.quantile(histogram_df, 0.75)

    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off

    histogram_df.to_csv("static/data/histogram2_" + str(cnt_create) + ".csv")
    create_histogram = create_histogram + svg.svg_histogram(cnt_create, col, target_col, lower, upper, 2, 'histogram_after')

    cnt_create = cnt_create + 1
    return redirect('/')

@app.route('/update_tree', methods=['GET', 'POST'])
def update_tree():
    def problem(df):
        col = list(df)

        missing = df.isnull().sum().tolist()
        extreme = []

        df = df.dropna()
        for column in df:
            q25 = np.quantile(df[column], 0.25)
            q75 = np.quantile(df[column], 0.75)

            iqr = q75 - q25
            cut_off = iqr * 1.5

            lower, upper = q25 - cut_off, q75 + cut_off
            data1 = df[df[column] > upper]
            data2 = df[df[column] < lower]

            extreme.append(data1.shape[0] + data2.shape[0])

        total = [x + y for x, y in zip(missing, extreme)]
        df = pd.DataFrame({x for x in zip(col, missing, extreme, total)}, columns = ['index', 'missing', 'extreme', 'total'])
        return df



    data = request.get_data().decode('utf-8').split('&')
    file_name = 'static/data/' + data[0][10:] + '.csv'
    name = data[1][5:]

    # count the number of problems per column in origin df
    origin_df = pd.read_csv(file_name)
    origin_problem_df = problem(origin_df)

    # select the column with the most problems
    target_col_name = origin_problem_df.iloc[origin_problem_df['total'].idxmax()]['index']
    target_df = origin_df.loc[:, [target_col_name]]
    remain_df = origin_df.drop([target_col_name], axis = 1)

    # action
    action = ['dropna', 'min', 'max', 'mean', 'median', 'em', 'locf']
    action_df = [target_df.dropna(), imputation.custom_imp_min(target_df), imputation.custom_imp_max(target_df),
                imputation.custom_imp_mean(target_col_name, target_df), imputation.custom_imp_median(target_col_name, target_df),
                imputation.custom_imp_em(target_col_name, target_df), imputation.custom_imp_locf(target_col_name, target_df)]

    # count the number of problems per column in action df
    after_problem_df = pd.DataFrame()
    for i in range(0, 7):
        df = problem(action_df[i])
        after_problem_df = pd.concat([after_problem_df, df])

    after_problem_df = after_problem_df.reset_index(drop = True)
    after_problem_df = after_problem_df.sort_values('total')

    # select the 3 actions with the least problems
    recommend_idx = after_problem_df.head(3)
    recommend_idx = list(recommend_idx.index.values)

    recommend_list = []
    file_name_list = []
    for i in range(3):
        recommend_list.append(action[recommend_idx[i]])
        df = action_df[recommend_idx[i]]
        df = pd.concat([remain_df, df], axis = 1)

        if recommend_list[i] == 'dropna':
            df = df.dropna(subset = [target_col_name], how = 'all')

        df.to_csv('static/data/' + name + '_' + str(i) + '.csv')

    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)
