from flask import Flask, render_template, request, redirect, flash
from nl4dv import NL4DV

import pandas as pd
import numpy as np
import json
import os

import imp_list.imputation as imputation
import imp_list.statistics as statistics
import imp_list.recommend as recommend
import imp_list.tree as tree

import temp_list.div as div
import temp_list.svg as svg

recommend_method = ''
recommend_type = ''

current_file = ''
cnt = 5

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
    with open('static/data/tree_data.json') as json_file:
        tree_data = json.load(json_file)

    root = tree.TreeNode(tree_data['file'], name = tree_data['name'], state = tree_data['state'], action = tree_data['action'])
    root = root.dict_to_tree(tree_data['children'])

    global current_file
    current_node = root.find_state('current')
    current_file = 'static/data/' + str(current_node.file) + '.csv'

    return render_template("index.html", tree_data = tree_data, create_div = create_div, create_vlSpec = create_vlSpec, create_bar = create_bar, create_heatmap = create_heatmap, create_histogram = create_histogram)

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    global recommend_method, recommend_type
    first_radio_name = request.form
    recommend_method = request.form["first_radio_name"]
    recommend_type = request.form["second_radio_name"]

    return redirect('/')

@app.route('/input_query', methods=['GET', 'POST'])
def input_query():
    global current_file, cnt_create, create_div, create_vlSpec, create_bar
    file_name = current_file
    df = pd.read_csv(file_name)

    nl4dv_df = df.dropna()
    nl4dv_df = nl4dv_df.to_dict('records')
    nl4dv_instance = NL4DV(data_url = os.path.join(file_name))
    dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}
    nl4dv_instance.set_dependency_parser(config = dependency_parser_config)

    result = request.form
    query = result['input_query']
    nl4dv_output = nl4dv_instance.analyze_query(query)

    # extraction attribute, task, vistype
    try:
        attributes = nl4dv_output['visList'][0]['attributes']
        tasks = nl4dv_output['visList'][0]['tasks']
        visType = nl4dv_output['visList'][0]['visType']
    except:   
        flash("please writing valid query")
        return redirect('/')

    if type(attributes) == list:
        attributes = ",".join(attributes)
    if type(tasks) == list:
        tasks = ",".join(tasks)
    if type(visType) == list:
        visType = ",".join(visType)

    # extraction vlspec
    vlSpec = nl4dv_output['visList'][0]['vlSpec']
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
    create_div = create_div + div.input_query_div(cnt_create, attributes, tasks, visType)

    # vlSpec
    create_vlSpec = create_vlSpec + svg.svg_vlSpec(cnt_create, vlSpec)

    cnt_create = cnt_create + 1

    return redirect('/')

@app.route('/current', methods=['GET', 'POST'])
def current():
    data = request.get_data().decode('utf-8').split('&')
    file_name = 'static/data/' + data[0][10:] + '.csv'
    name = data[1][5:]

    df = pd.read_csv(file_name)
    df = df[sorted(df.columns)]
    column_list = list(df)

    # tree
    with open('static/data/tree_data.json') as json_file:
        tree_data = json.load(json_file)
    root = tree.TreeNode(file = tree_data['file'], name = tree_data['name'], state = tree_data['state'], action = tree_data['action'])
    root = root.dict_to_tree(tree_data['children'])

    # find children node
    my_node = root.find_name(name)
    children_node = my_node.children

    global recommend_method, cnt_create, create_div, create_bar
    if recommend_method == 'A':
        # current df problem
        missing, extreme, total = recommend.quality_issue(df)
        current_df_problem = pd.DataFrame({x for x in zip(column_list, missing, extreme, total)}, columns = ['index', 'missing', 'extreme', 'total'])
        current_df_problem = current_df_problem.sort_values(by = 'index').reset_index(drop = True)
        current_df_problem = current_df_problem.drop(['index'], axis = 1)
        
        current_df_problem = current_df_problem.sum().tolist()

        # compare current - children problem to generation div
        action = []
        output = [[], [], []]
        output_percent = [[], [], []]
        output_sign = [[], [], []]

        for i in range(0, 3):
            action.append(children_node[i].action)
            
            child_df = pd.read_csv('static/data/' + children_node[i].file + '.csv')
            child_df = child_df[sorted(child_df.columns)]
            
            missing, extreme, total = recommend.quality_issue(child_df)
            child_df_problem = pd.DataFrame({x for x in zip(column_list, missing, extreme, total)}, columns = ['index', 'missing', 'extreme', 'total'])
            child_df_problem = child_df_problem.sort_values(by = 'index').reset_index(drop = True)
            child_df_problem = child_df_problem.drop(['index'], axis = 1)
            
            child_df_problem = child_df_problem.sum().tolist()

            for j in range(len(current_df_problem)):
                diff = current_df_problem[j] - child_df_problem[j]

                if diff > 0:
                    diff_percent = (100 * diff)/current_df_problem[j]
                    output_sign[i].append('감소')
                elif diff == 0:
                    diff_percent = 0
                    output_sign[i].append('감소')
                else:
                    diff = -diff
                    diff_percent = 0
                    output_sign[i].append('증가')

                output[i].append(diff)
                output_percent[i].append(diff_percent)

        # generation div
        create_div = create_div + div.current_div(cnt_create, name, children_node, action, output, output_percent, output_sign)

        # barchart - each
        missing, extreme, total = recommend.quality_issue(df)
        max_value = max(total)

        bar_output_df = pd.DataFrame({x for x in zip(column_list, missing, extreme)}, columns = ['index', 'missing', 'extreme'])
        bar_output_df = bar_output_df.sort_values(by = 'index').reset_index(drop = True)

        bar_output_df.to_csv("static/data/bar_" + str(cnt_create) + ".csv", index = False)
        create_bar = create_bar + svg.svg_bar1(cnt_create, max_value)

        # barchart - total
        create_bar = create_bar + svg.svg_bar2(cnt_create, max_value)

    else:
        print('not a')

    cnt_create = cnt_create + 1

    return redirect('/')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    data = request.get_data().decode('utf-8').split('&')
    file_name = 'static/data/' + data[0][10:] + '.csv'
    name = data[1][5:]

    df = pd.read_csv(file_name)
    df = df[sorted(df.columns)]

    global recommend_method, current_file, cnt_create, create_div, create_heatmap, create_histogram
    if recommend_method == 'A':
        before_df = pd.read_csv(current_file)
        before_df = before_df[sorted(df.columns)]
        column_list = list(before_df)

        # generation div
        create_div = create_div + div.recommend_div(cnt_create, name)

        missing, extreme, total = recommend.quality_issue(before_df)
        df_problem = pd.DataFrame({x for x in zip(column_list, missing, extreme, total)}, columns = ['index', 'missing', 'extreme', 'total'])
        df_problem = df_problem.sort_values(by = 'index').reset_index(drop = True)
        target_column = df_problem.iloc[df_problem['total'].idxmax()]['index']

        # heatmap - before
        heatmap_output_df = svg.make_heatmap_df(column_list, before_df)

        heatmap_output_df.to_csv("static/data/heatmap1_" + str(cnt_create) + ".csv", index = False)
        create_heatmap = create_heatmap + svg.svg_heatmap(cnt_create, column_list, target_column, 1, 'heatmap_before')

        # heatmap - after
        heatmap_output_df = svg.make_heatmap_df(column_list, df)

        heatmap_output_df.to_csv("static/data/heatmap2_" + str(cnt_create) + ".csv", index = False)
        create_heatmap = create_heatmap + svg.svg_heatmap(cnt_create, column_list, target_column, 2, 'heatmap_after')

        # histogram
        before_df = before_df.dropna()
        min_value = before_df[target_column].min()
        max_value = before_df[target_column].max()
        lower, upper = recommend.lower_upper(before_df, target_column)

        before_df.to_csv("static/data/histogram1_" + str(cnt_create) + ".csv", index = False)
        create_histogram = create_histogram + svg.svg_histogram(cnt_create, target_column, min_value, max_value, lower, upper, 1, 'histogram_before')

        df.to_csv("static/data/histogram2_" + str(cnt_create) + ".csv", index = False)
        create_histogram = create_histogram + svg.svg_histogram(cnt_create, target_column, min_value, max_value, lower, upper, 2, 'histogram_after')

    else:
        print('not a')

    cnt_create = cnt_create + 1

    return redirect('/')

@app.route('/update_tree', methods=['GET', 'POST'])
def update_tree():
    data = request.get_data().decode('utf-8').split('&')
    file_name = 'static/data/' + data[0][10:] + '.csv'
    name = data[1][5:]

    df = pd.read_csv(file_name)
    df = df[sorted(df.columns)]
    column_list = list(df)

    with open('static/data/tree_data.json') as json_file:
        tree_data = json.load(json_file)

    root = tree.TreeNode(tree_data['file'], name = tree_data['name'], state = tree_data['state'], action = tree_data['action'])
    root = root.dict_to_tree(tree_data['children'])

    global recommend_method, recommend_type
    if recommend_method == 'A':
        # quality issue per column in current df
        missing, extreme, total = recommend.quality_issue(df)
        df_problem = pd.DataFrame({x for x in zip(column_list, missing, extreme, total)}, columns = ['index', 'missing', 'extreme', 'total'])
        df_problem = df_problem.sort_values(by = 'index').reset_index(drop = True)

        # select the column with the most quality issue
        target_column = df_problem.iloc[df_problem['total'].idxmax()]['index']
        target_df = df.loc[:, [target_column]]
        remain_df = df.drop([target_column], axis = 1)

        print(target_column)

        # action
        action = ['dropna', 'min', 'max', 'mean', 'median', 'em', 'locf']
        action_df = ['dropna', imputation.custom_imp_min(target_df), imputation.custom_imp_max(target_df),
                    imputation.custom_imp_mean(target_column, target_df), imputation.custom_imp_median(target_column, target_df),
                    imputation.custom_imp_em(target_column, target_df), imputation.custom_imp_locf(target_column, target_df)]

        # current df quality issue
        missing, extreme, total = recommend.quality_issue(df)
        current_df_problem = pd.DataFrame({x for x in zip(column_list, total)}, columns = ['index', 'total'])
        current_df_problem = current_df_problem.sort_values(by = 'index').reset_index(drop = True)
        current_df_problem = current_df_problem.drop(['index'], axis = 1)
        
        current_df_problem = current_df_problem.sum().tolist()

        # compare current - action
        output = []

        for i in range(0, 7):
            if action[i] != 'dropna':
                tmp_df = action_df[i]
                tmp_df = pd.concat([remain_df, tmp_df], axis = 1)
            else:
                tmp_df = df.dropna(subset = [target_column], how = 'all')
            
            tmp_df = tmp_df[sorted(df.columns)]

            missing, extreme, total = recommend.quality_issue(tmp_df)
            tmp_df_problem = pd.DataFrame({x for x in zip(column_list, total)}, columns = ['index', 'total'])
            tmp_df_problem = tmp_df_problem.sort_values(by = 'index').reset_index(drop = True)
            tmp_df_problem = tmp_df_problem.drop(['index'], axis = 1)
            
            tmp_df_problem = tmp_df_problem.sum().tolist()

            diff = current_df_problem[0] - tmp_df_problem[0]
            output.append([i, diff])
    
    else:
        drop_df = df.dropna()

        # quality per column in current df
        output = quality_metric_total(drop_df)
        df_problem = pd.DataFrame({x for x in zip(column_list, output[0], output[1], output[2], output[3])}, columns = ['index', 'kstest', 'skewness', 'kurtosis', 'entropy'])
        df_problem = df_problem.sort_values(by = 'index').reset_index(drop = True)

        # select the column with the lowest quality
        # kstest, entropy -> 낮을수록 좋음
        # skewness, kurtosis -> 0 가까울수록 좋음
        if recommend_type == 'skewness' or recommend_type == 'kurtosis':
            df_problem[recommend_type] = df_problem[recommend_type].abs()

        target_column = df_problem.iloc[df_problem[recommend_type].idxmax()]['index']
        target_idx = df.columns.get_loc(target_column)
        target_df = df.loc[:, [target_column]]
        remain_df = df.drop([target_column], axis = 1)

        print(target_column)

        # action
        action = ['dropna', 'min', 'max', 'mean', 'median', 'em', 'locf']
        action_df = ['dropna', imputation.custom_imp_min(target_df), imputation.custom_imp_max(target_df),
                    imputation.custom_imp_mean(target_column, target_df), imputation.custom_imp_median(target_column, target_df),
                    imputation.custom_imp_em(target_column, target_df), imputation.custom_imp_locf(target_column, target_df)]

        # current column quality
        kstest, skewness, kurtosis, entropy = quality_metric(drop_df, target_idx)
        if recommend_type == 'kstest': current_df_quality = kstest
        elif recommend_type == 'skewness': current_df_quality = abs(skewness)
        elif recommend_type == 'kurtosis': current_df_quality = abs(kurtosis)
        elif recommend_type == 'entropy': current_df_quality = entropy

        # compare current - action
        output = []

        for i in range(0, 7):
            if action[i] != 'dropna':
                tmp_df = action_df[i].loc[:, [target_column]]
                kstest, skewness, kurtosis, entropy = quality_metric(tmp_df, 0)

                if recommend_type == 'kstest':
                    tmp_df_quality = kstest
                elif recommend_type == 'skewness':
                    tmp_df_quality = abs(skewness)
                elif recommend_type == 'kurtosis':
                    tmp_df_quality = abs(kurtosis)
                elif recommend_type == 'entropy':
                    tmp_df_quality = kstest
                    
                diff = current_df_quality - tmp_df_quality
                output.append([i, diff])
            else:
                tmp_df = drop_df.loc[:, [target_column]]
                output.append([i, 0])

    output.sort(key = lambda x:-x[1])

    # select the 3 actions with the most quality issue reduction
    recommend_idx = [output[0][0], output[1][0], output[2][0]]
    print(recommend_idx)

    # recommend - children node
    for i in range(0, 3):
        if action[recommend_idx[i]] != 'dropna':
            recommend_df = action_df[recommend_idx[i]]
            recommend_df = pd.concat([remain_df, recommend_df], axis = 1)
        else:
            recommend_df = df.dropna(subset = [target_column], how = 'all')
        
        recommend_df = recommend_df[sorted(df.columns)]

        global cnt
        recommend_df.to_csv('static/data/' + str(cnt) + '.csv', index = False)

        # generation children node
        new_node = tree.TreeNode(file = str(cnt), name = str(cnt), state = '', action = action[recommend_idx[i]])
        root.add_child_to(name, new_node)

        cnt = cnt + 1

    # update state
    root.update_state(name)

    output_data = root.tree_to_dict()
    with open('static/data/tree_data.json', 'w') as f:
        json.dump(output_data, f, indent = 4)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)
