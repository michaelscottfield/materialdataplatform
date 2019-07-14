from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import timedelta
import ontology
import datetime
from bson import json_util
import json
# from flask_socketio import SocketIO

def compare_date(str1, str2):
    d1 = datetime.datetime.strptime(str1, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(str2, '%Y-%m-%d')
    delta = d1 - d2
    if delta.days < 0:
        return True
    else:
        return False

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
PICTURE_FOLDER = os.path.join('static', 'images')
# app = Flask(__name__, static_url_path='/home/mike/PycharmProjects/materialontology/static')
# app = Flask(__name__, static_folder='static')
# app = Flask(__name__)
app = Flask(__name__,template_folder='./static')
cors = CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# socket_io = SocketIO(app)
app.config['UPLOAD_FOLDER'] = PICTURE_FOLDER

@app.route('/')
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '2018-06-01.jpg')
    # print(full_filename)
    return render_template("index.html", user_image=full_filename)
    # return send_from_directory(root, "index.html")
    # return render_template('root/index.html')
    # return app.send_static_file('static/index.html')
    # return app.send_static_file('index.html', user_image=full_filename)


@app.route('/query', methods=['POST'])
def query():
    # 接受前端发来的数据
    # text = request.form['text']
    method1 = request.form['method1']
    method2 = request.form['method2']
    type1 = request.form['type1']
    self_defined_field1 = request.form['defined_field1']
    self_defined_field2 = request.form['defined_field2']
    self_defined_field3 = request.form['defined_field3']
    self_defined_field4 = request.form['defined_field4']
    self_defined_field5 = request.form['defined_field5']
    system_query_method = request.form['system_query_method']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    choose_pic = request.form['choose_pic']
    query_value1 = request.form['query_value1']
    query_value2 = request.form['query_value2']
    query_value3 = request.form['query_value3']
    query_value4 = request.form['query_value4']
    query_value5 = request.form['query_value5']
    # print(method1)
    if method1 == "true": # system preset query
        if system_query_method == "已选择某种方式进行查询":
            return jsonify({'error1': '查询方式设置错误'})
        elif system_query_method == "已经选择按照日期范围查询":
            if choose_pic == 'true':
                filePath = ontology.getFileRange('steelmaking', 'upload-date', start_time, end_time)
                # data = ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, end_time)
                # data['filepath'] = filePath
                # data = [json.dumps(item, default=json_util.default) for item in data]
                data = [json.dumps(item, default=json_util.default) for item in
                        ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, end_time)]
                data.append(json.dumps({'filePath': filePath}))
                # data['filepath'] = filePath
                # data.append({'filePath': filePath})
                # print(data)
                return jsonify(data=data)
                # result = jsonify(data=data)
            elif start_time == "":
                if end_time == "":
                    return jsonify({'error2': '日期设置错误'})
                data = [json.dumps(item, default=json_util.default) for item in
                        ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', '', end_time)]
                return jsonify(data=data)
                # return jsonify(ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', '', end_time))
            elif end_time == "":
                data = [json.dumps(item, default=json_util.default) for item in
                        ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, '')]
                return jsonify(data=data)
                # return jsonify(ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, ''))
            else:
                data = [json.dumps(item, default=json_util.default) for item in
                        ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, end_time)]
                return jsonify(data=data)
    elif method2 == 'true':
        fields = []
        values = []
        if not self_defined_field1 == '' and not query_value1 == '':
            fields.append(self_defined_field1)
            values.append(query_value1)
        elif not self_defined_field2 == '' and not query_value2 == '':
            fields.append(self_defined_field2)
            values.append(query_value2)
        elif not self_defined_field3 == '' and not query_value3 == '':
            fields.append(self_defined_field3)
            values.append(query_value3)
        elif not self_defined_field4 == '' and not query_value4 == '':
            fields.append(self_defined_field4)
            values.append(query_value4)
        elif not self_defined_field5 == '' and not query_value5 == '':
            fields.append(self_defined_field5)
            values.append(query_value5)
        field_values = {}
        for f in range(0, len(fields)):
            field_values[fields[f]] = values[f]
        if choose_pic == 'true':
            filePath = ontology.getFileRange('steelmaking', 'upload-date', start_time, end_time)
        else:
            data = [json.dumps(item, default=json_util.default) for item in
                    ontology.get_mongo_doc_fields('steelmaking', field_values)]
            # print(data)
            return jsonify(data=data)
            # if choose_pic == True:

                # return json.dumps(ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, end_time))
                # print(ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, end_time))
                # return jsonify(ontology.get_mongo_doc_date_range('steelmaking', 'upload-date', start_time, end_time))
    # print(text)
    # data = json.loads(request.form.get('data'))
    # return jsonify({'success': 'true'})

if __name__ == '__main__':
    # col_list = ontology.mongo_db.list_collection_names()
    # app.run(debug=True, host='127.0.0.1')
    app.run(debug=True, host='127.0.0.1', port=8081)
    # app.run()
    # socket_io.run(app, debug=True, host='127.0.0.1', port=8081)
