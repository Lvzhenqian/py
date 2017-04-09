#!/usr/bin/env python
# coding=utf-8
from flask import Flask,jsonify,make_response, request,abort

app = Flask(__name__)

tasks = [
    {
        'id':1,
        'title':'BYE.ye',
        'description':'haha',
        'done':False
    },
    {
        'id':2,
        'title':'this is 2',
        'description':'mimi',
        'done':False
    }
]

@app.route('/api/tasks/<int:task_id>',methods=['GET'])
def get_tasks(task_id):
    task = [x for x in tasks if x['id']==task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'tasks':task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}),404)



@app.route('/api/push',methods=['POST'])
def create_task():
    if not request.json or not 'title' in  request.json:
        abort(400)
    task = {
        'id':tasks[-1]['id']+1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False,
        }
    tasks.append(task)
    return jsonify({'task': task,'test':request.json}), 201

@app.route('/group/testpsh',methods=['POST'])
def test_push():
    if request.remote_addr != '127.0.0.1':
        return jsonify({'msg':'error'})
    return jsonify({'testreq':request.remote_addr,'requestpath':request.path}),201



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)
