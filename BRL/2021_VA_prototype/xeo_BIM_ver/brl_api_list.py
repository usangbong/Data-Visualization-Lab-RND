from flask import Flask, request
from flask_restx import Api, Resource, fields
import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_restx import reqparse
import random

parser = reqparse.RequestParser(bundle_errors=True)
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

app = Flask(__name__)
api = Api(app, version='1.0', title=' BRL API',
    description='BRL 시스템 용 API 목록',
)


class DictItem(fields.Raw):
    def output(self, key, obj, *args, **kwargs):
        return obj[key]

history_ns = api.namespace('history', description='히스토리 api <img src="./static/images/hist.png" /> <img src="./static/images/hist2.png" /> ')

history = api.model('History', {
    'id': fields.Integer(readOnly=True, description='히스토리 ID'),
    'datetime': fields.String(readOnly=True, description='히스토리등록 날짜'),
    'img_path': fields.String(readOnly=True, description='히스토리 이미지 경로'),
    'img_file': fields.String(required=True, description='자바스크립트 이미지'),
    'board_param': DictItem(required=True, attribute="board_param", description='{"date": "2021-02-05","Hour": "15:00","sensor_data": "Tension","state_anal": "Anomaly Score","graph_type": "Line","data_pre": "Raw","wind_dir": false,"wind_speed": false,"tempr": true,"humidity": false,"preci": true,"atmos": false,"vehicle_speed": false,"vehicle_loc": false}'),
})

class HistoryDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        todo['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        todo['img_path'] = 'images/'+data['img_file']
        self.todos.append(todo)
        return todo

HistDAO = HistoryDAO()
temp = {
'date':'2021-02-05',
'Hour':'15:00',
'sensor_data':'Tension',
'state_anal':'Anomaly Score',
'graph_type':'Line',
'data_pre':'Raw',
'wind_dir':False,
'wind_speed':False,
'tempr':True,
'humidity':False,
'preci':True,
'atmos':False,
'vehicle_speed':False,
'vehicle_loc':False
}

HistDAO.create({'img_file':'test_1.png','board_param': temp})
HistDAO.create({'img_file':'test_2.png','board_param': temp})
HistDAO.create({'img_file':'test_3.png','board_param': temp})


@history_ns.route('/')
class HistoryList(Resource):
    @history_ns.doc('list_History')
    @history_ns.marshal_list_with(history)
    def get(self):
        return HistDAO.todos

    @history_ns.doc('create_History')
    @history_ns.expect(history)
    @history_ns.marshal_with(history, code=201)
    def post(self):
        return HistDAO.create(api.payload), 201


@history_ns.route('/<int:id>')
@history_ns.response(404, 'History not found')
@history_ns.param('id', 'The History identifier')
class History(Resource):
    @history_ns.doc('get_History')
    def get(self, id):
        return HistDAO.get(id)
############################################################################################################################################


data_ns = api.namespace('data', description='Data Dates api <img src="./static/images/dates.png" />')

datas = api.model('Data', {
    'data_dates': fields.String(readOnly=True, description='하루치 데이터가 있는 날'),
})

class DataDAO(object):
    def __init__(self):
        self.datas = []

    def create(self, data):
        self.datas.append(data)
        return data

DatasDAO = DataDAO()

DatasDAO.create({'data_dates':datetime.datetime.now().strftime("%Y-%m-%d")})
DatasDAO.create({'data_dates':datetime.datetime.now().strftime("%Y-%m-%d")})
DatasDAO.create({'data_dates':datetime.datetime.now().strftime("%Y-%m-%d")})


@data_ns.route('/')
class DatasList(Resource):
    @data_ns.doc('list_Data_dates')
    @data_ns.marshal_list_with(datas)
    def get(self):
        return DatasDAO.datas

static_ns = api.namespace('static', description='Data static api  <img src="./static/images/static.png" />')

static_datas = api.model('Static Data', {
    'datetime': fields.String(readOnly=True, description='스태틱 데이터 eg. 2021-02-01 15:00:00'),
    'date': fields.String(readOnly=True, description='스태틱 데이터 eg. 2021-02-01'),
    'hour': fields.String(readOnly=True, description='스태틱 데이터 eg. 15'),
    'min': fields.String(readOnly=True, description='스태틱 데이터 eg. 00'),
    'sec': fields.String(readOnly=True, description='스태틱 데이터 eg. 00'),
    'sensor_name': fields.String(readOnly=True, description='센서 이름 eg. EXP001'),
    'sensor_type': fields.String(readOnly=True, description='센서 타입 eg. Tenstion'),
    'sensor_val': fields.Float(readOnly=True, description='센서 값'),
})

class StaticDataDAO(object):
    def __init__(self):
        self.datas = []

    def create(self, data):
        todo = data
        tmpNow=datetime.datetime.now()
        todo['datetime'] = tmpNow.replace(second=todo['date']).strftime("%Y-%m-%d %H:%M:%S")
        todo['hour'] = tmpNow.replace(second=todo['date']).strftime("%H")
        todo['min'] = tmpNow.replace(second=todo['date']).strftime("%M")
        todo['sec'] = tmpNow.replace(second=todo['date']).strftime("%S")
        todo['date'] = tmpNow.replace(second=todo['date']).strftime("%Y-%m-%d")
        todo['sensor_val'] = random.random()-0.5
        self.datas.append(todo)
        return todo

StaticDatasDAO = StaticDataDAO()

for i in range(0,60):
    StaticDatasDAO.create({'date':i,'sensor_name':'EXP001','sensor_type':'Tension'})

for i in range(0,60):
    StaticDatasDAO.create({'date':i,'sensor_name':'EXP002','sensor_type':'Tension'})


@static_ns.route('/')
class StaticDatasList(Resource):
    @static_ns.doc('search_data_static')
    @static_ns.expect(api.model('static post', {
    'sensor_name': fields.String(required=True, description='센서 이름 eg. EXP001'),
    'date': fields.String(required=True, description='검색 날짜 eg. '+datetime.datetime.now().strftime("%Y-%m-%d")),
    'hour': fields.String(required=True, description='검색할 시간 eg. '+datetime.datetime.now().strftime("%H")),
    }))
    def post(self):
        tmp_data = request.json
        results = list(filter(lambda x: x['date']==tmp_data['date'], StaticDatasDAO.datas))
        results = list(filter(lambda x: x['hour']==tmp_data['hour'], results))
        results = list(filter(lambda x: x['sensor_name']==tmp_data['sensor_name'], results))
        return results, 201

dynamic_ns = api.namespace('dynamic', description='Data dynamic api <img src="./static/images/dynamic1.png" /> <img src="./static/images/dynamic.png" />')

dynamic_datas = api.model('Dynamic Data', {
    'datetime': fields.String(readOnly=True, description='다이나믹 데이터 eg. 2021-02-01 15:00:00'),
    'date': fields.String(readOnly=True, description='다이나믹 데이터 eg. 2021-02-01'),
    'hour': fields.String(readOnly=True, description='다이나믹 데이터 eg. 15'),
    'min': fields.String(readOnly=True, description='다이나믹 데이터 eg. 00'),
    'sec': fields.String(readOnly=True, description='다이나믹 데이터 eg. 00'),
    'sensor_name': fields.String(readOnly=True, description='센서 이름 eg. EXP001'),
    'sensor_type': fields.String(readOnly=True, description='센서 타입 eg. Tenstion'),
    'sensor_val': fields.Float(readOnly=True, description='센서 값'),
})

class DynamicDataDAO(object):
    def __init__(self):
        self.datas = []

    def create(self, data):
        todo = data
        tmpNow=datetime.datetime.now()
        todo['datetime'] = tmpNow.replace(second=todo['date']).strftime("%Y-%m-%d %H:%M:%S")
        todo['hour'] = tmpNow.replace(second=todo['date']).strftime("%H")
        todo['min'] = tmpNow.replace(second=todo['date']).strftime("%M")
        todo['sec'] = tmpNow.replace(second=todo['date']).strftime("%S")
        todo['date'] = tmpNow.replace(second=todo['date']).strftime("%Y-%m-%d")
        todo['sensor_val'] = random.random()-0.5
        self.datas.append(todo)
        return todo

dynamic_datas = DynamicDataDAO()

for i in range(0,60):
    dynamic_datas.create({'date':i,'sensor_name':'ACC001_X','sensor_type':'Tension'})

for i in range(0,60):
    dynamic_datas.create({'date':i,'sensor_name':'DSG002_2','sensor_type':'Tension'})


@dynamic_ns.route('/')
class DynamicDatasList(Resource):
    @dynamic_ns.doc('search_data_dynamic')
    @data_ns.expect(api.model('dynamic post', {
    'sensor_name': fields.String(required=True, description='센서 이름 eg. ACC001_X'),
    'date': fields.String(required=True, description='검색 날짜 eg. '+datetime.datetime.now().strftime("%Y-%m-%d")),
    'hour': fields.String(required=True, description='검색할 시간 eg. '+datetime.datetime.now().strftime("%H")),
    }))
    def post(self):
        tmp_data = request.json
        results = list(filter(lambda x: x['date']==tmp_data['date'], dynamic_datas.datas))
        results = list(filter(lambda x: x['hour']==tmp_data['hour'], results))
        results = list(filter(lambda x: x['sensor_name']==tmp_data['sensor_name'], results))
        return results, 201

############################################################################################################################################################################################################

if __name__ == '__main__':
    app.run(debug=True, port=9904)