def input_query_div(cnt_create, attributes, tasks, visType):
    div = '''
        <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-bottom: 5px; border: 3px solid #74788D;">
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
    return div

def current_div(cnt_create, name, children_node, action, output, output_percent, output_sign):
    div = '''
        <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-bottom: 5px; border: 3px solid #74788D;">
            <div id="node" style="width: 30px; height: 30px; margin: 5px; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">''' + name + '''</div>
            <div id="bar1" style="width: 25%; border-right: 3px solid #F2F2F5;"></div>
            <div id="bar2" style="width: 25%; border-right: 3px solid #F2F2F5;"></div>
            <div id="recommend" style="width: 40%;">
                <div id="recommend1" style="display: flex; width: 100%; height: 20%;">
                    <div id="recommend_node1" style="width: 30px; height: 30px; margin: 5px; color: white; background-color: #47597E; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">''' + children_node[0].name + '''</div>
                    <div id="recommend_list1" style="width: 100%; height: 100%; margin: 5px; background-color: #DBE6FD; text-align: left; border: 2px solid; border-radius: 5px;">
                        ''' + action[0] + '''
                        <div id="issue" style="display: flex;">
                            결측 값 개수
                            <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue1_inner" style="width: ''' + str(output_percent[0][0]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #f37021 0%, #FFCDD2 100%);">''' + str(output[0][0]) + '''</div>
                            </div>
                            '''+ output_sign[0][0] + ''', 극단 값 개수
                            <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue2_inner" style="width: ''' + str(output_percent[0][1]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">''' + str(output[0][1]) + '''</div>
                            </div>
                            '''+ output_sign[0][1] + ''', 통합 개수
                            <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue3_inner" style="width: ''' + str(output_percent[0][2]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">''' + str(output[0][2]) + '''</div>
                            </div>
                            '''+ output_sign[0][2] + '''
                        </div>
                    </div>
                </div>
                <br>
                <div id="recommend2" style="display: flex; width: 100%; height: 20%;">
                    <div id="recommend_node2" style="width: 30px; height: 30px; margin: 5px; background-color: lightgray; text-align: center; border: 2px solid; border-radius: 50%; line-height: 30px;">''' + children_node[1].name + '''</div>
                    <div id="recommend_list2" style="width: 100%; height: 100%; margin: 5px; background-color: lightgray; text-align: left; border: 2px solid; border-radius: 5px;">
                        ''' + action[1] + '''
                        <div id="issue" style="display: flex;">
                            결측 값 개수
                            <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue1_inner" style="width: ''' + str(output_percent[1][0]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #f37021 0%, #FFCDD2 100%);">''' + str(output[1][0]) + '''</div>
                            </div>
                            '''+ output_sign[1][0] + ''', 극단 값 개수
                            <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue2_inner" style="width: ''' + str(output_percent[1][1]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">''' + str(output[1][1]) + '''</div>
                            </div>
                            '''+ output_sign[1][1] + ''', 통합 개수
                            <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue3_inner" style="width: ''' + str(output_percent[1][2]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">''' + str(output[1][2]) + '''</div>
                            </div>
                            '''+ output_sign[1][2] + '''
                        </div>
                    </div>
                </div>
                <br>
                <div id="recommend3" style="display: flex; width: 100%; height: 20%;">
                    <div id="recommend_node3" style="width: 30px; height: 30px; margin: 5px; background-color: lightgray; text-align: center; border: 2px solid; border-radius: 50%; line-height: 30px;">''' + children_node[2].name + '''</div>
                    <div id="recommend_list3" style="width: 100%; height: 100%; margin: 5px; background-color: lightgray; text-align: left; border: 2px solid; border-radius: 5px;">
                        ''' + action[2] + '''
                        <div id="issue" style="display: flex;">
                            결측 값 개수
                            <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue1_inner" style="width: ''' + str(output_percent[2][0]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #f37021 0%, #FFCDD2 100%);">''' + str(output[2][0]) + '''</div>
                            </div>
                            '''+ output_sign[2][0] + ''', 극단 값 개수
                            <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue2_inner" style="width: ''' + str(output_percent[2][1]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">''' + str(output[2][1]) + '''</div>
                            </div>
                            '''+ output_sign[2][1] + ''', 통합 개수
                            <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 2px solid;">
                                <div id="issue3_inner" style="width: ''' + str(output_percent[2][2]) + '''%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">''' + str(output[2][2]) + '''</div>
                            </div>
                            '''+ output_sign[2][2] + '''
                        </div>
                    </div>
                </div>
            </div>
        </div>
    '''
    return div

def recommend_div(cnt_create, name):
    div = '''
        <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-bottom: 5px; border: 3px solid #74788D;">
            <div id="node" style="width: 30px; height: 30px; margin: 5px; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">''' + name + '''</div>
            <div id="heatmap_before" style="width: 25%; border-right: 3px solid #F2F2F5;"></div>
            <div id="heatmap_after" style="width: 25%; border-right: 3px solid #F2F2F5;"></div>
            <div id="histogram_before" style="width: 20%; border-right: 3px solid #F2F2F5;"></div>
            <div id="histogram_after" style="width: 20%;"></div>
        </div>
    '''
    return div