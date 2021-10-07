def input_query_div(cnt_create, attributes, tasks, visType):
    div = '''
        <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-top: 5px; background-color: white; border: 1px solid #D8D8D8;">
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
            <div id="add"></div>
        </div>
        '''
    return div

def current_div(cnt_create, name):
    div = '''
        <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-top: 5px; background-color: white; border: 1px solid #D8D8D8;">
            <div id="node" style="width: 30px; height: 30px; margin: 5px; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">''' + name + '''</div>
            <div id="bar1" style="width: 25%; border-right: 1px solid #D8D8D8;"></div>
            <div id="bar2" style="width: 25%; border-right: 1px solid #D8D8D8;"></div>
            <div id="recommend" style="width: 40%;">
                <div id="recommend1" style="display: flex; width: 100%; height: 20%;">
                    <div id="recommend_node1" style="width: 30px; height: 30px; margin: 5px; background-color: lightgray; text-align: center; border: 2px dotted black; border-radius: 50%; line-height: 30px;">18</div>
                    <div id="recommend_list1" style="width: 100%; height: 100%; margin: 5px; background-color: lightgray; text-align: left; border: 1px solid; border-radius: 5px;">
                        결측 값 최대 값으로 대체
                        <div id="issue" style="display: flex;">
                            결측 값 개수
                            <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue1_inner" style="width: 16%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">16</div>
                            </div>
                            감소, 극단 값 개수
                            <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue2_inner" style="width: 18%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">18</div>
                            </div>
                            감소, 통합 개수
                            <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue3_inner" style="width: 36%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">36</div>
                            </div>
                            감소
                        </div>
                    </div>
                </div>
                <br>
                <div id="recommend2" style="display: flex; width: 100%; height: 20%;">
                    <div id="recommend_node2" style="width: 30px; height: 30px; margin: 5px; background-color: lightgray; text-align: center; border: 2px dotted black; border-radius: 50%; line-height: 30px;">17</div>
                    <div id="recommend_list2" style="width: 100%; height: 100%; margin: 5px; background-color: lightgray; text-align: left; border: 1px solid; border-radius: 5px;">
                        결측 값 최소 값으로 대체
                        <div id="issue" style="display: flex;">
                            결측 값 개수
                            <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue1_inner" style="width: 16%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">16</div>
                            </div>
                            감소, 극단 값 개수
                            <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue2_inner" style="width: 28%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">28</div>
                            </div>
                            감소, 통합 개수
                            <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue3_inner" style="width: 11%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">11</div>
                            </div>
                            감소
                        </div>
                    </div>
                </div>
                <br>
                <div id="recommend3" style="display: flex; width: 100%; height: 20%;">
                    <div id="recommend_node3" style="width: 30px; height: 30px; margin: 5px; color: white; background-color: #0D47A1; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">7</div>
                    <div id="recommend_list3" style="width: 100%; height: 100%; margin: 5px; background-color: #BBDEFB; text-align: left; border: 1px solid; border-radius: 5px;">
                        결측 값 평균으로 대체
                        <div id="issue" style="display: flex;">
                            결측 값 개수
                            <div id="issue1" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue1_inner" style="width: 33%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #F44336 0%, #FFCDD2 100%);">33</div>
                            </div>
                            감소, 극단 값 개수
                            <div id="issue2" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue2_inner" style="width: 29%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #4CAF50 0%, #C8E6C9 100%);">29</div>
                            </div>
                            감소, 통합 개수
                            <div id="issue3" style="width: 10%; height: 20px; background-color: white; border: 1px solid;">
                                <div id="issue3_inner" style="width: 35%; height: 20px; background-size: 100%''' + ''' 100%; text-align: center; background-image: linear-gradient(90deg, #2196F3 0%, #BBDEFB 100%);">35</div>
                            </div>
                            감소
                        </div>
                    </div>
                </div>
            </div>
        </div>
    '''
    return div

def recommend_div(cnt_create, name):
    div = '''
        <div id="vis''' + str(cnt_create) + '''" style="display: flex; height: 250px; margin-top: 5px; background-color: white; border: 1px solid #D8D8D8;">
            <div id="node" style="width: 30px; height: 30px; margin: 5px; text-align: center; border: 2px solid black; border-radius: 50%; line-height: 30px;">''' + name + '''</div>
            <div id="heatmap_before" style="width: 25%; border-right: 1px solid #D8D8D8;"></div>
            <div id="heatmap_after" style="width: 25%; border-right: 1px solid #D8D8D8;"></div>
            <div id="histogram_before" style="width: 20%; border-right: 1px solid #D8D8D8;"></div>
            <div id="histogram_after" style="width: 20%;"></div>
        </div>
    '''
    return div