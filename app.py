from flask import Flask, json, render_template,jsonify,request
from flask.globals import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_restful import Api, Resource

import json
app = Flask(__name__)
api = Api(app)
#databse connections
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/toastApp")
db = mongodb_client.db

class TableListAPI(Resource):

  def get(self):
    task = db.table.find()
    output = []
    for s in task:
        output.append({'name' : s['name']})
    return jsonify({'result' : output})

  def post(self):
    name = request.json['name']
    task_id = db.table.insert({'name': name})
    new_task = db.table.find_one({'_id': task_id })
    output = {'name' : new_task['name']}
    return jsonify({'result' : output})    


class TableAPI(Resource):
    
  def get(self, task_id):
    task = db.table
    new_task = task.find_one({ '_id': ObjectId(task_id) })
    # print('new_task', new_task)    
    output = {'_id': str(new_task['_id']), 'name' : new_task['name']}
    return jsonify({'result' : output})

  def put(self, task_id):  
    task = db.table
    name = request.json['name']
    data = {'name': name}   
    task.update({'_id': ObjectId(task_id)}, {'$set': data})
    new_task = task.find_one({'_id': ObjectId(task_id) })
    # print('new_task', new_task)   
    output = {'_id': str(new_task['_id']), 'name' : new_task['name']}
    return jsonify({'result' : output})

  def delete(self, task_id):
    db.table.delete_one({ '_id': ObjectId(task_id) })
    return jsonify({'result' : 'task has been deleted'})



class MenuListAPI(Resource):

  def get(self):
    task = db.menu.find()
    output = []
    for s in task:
        output.append({'name' : s['name'], 'type' : s['type'], 'price' : s['price']})
    return jsonify({'result' : output})

  def post(self):
    name = request.json['name']
    type = request.json['type']
    price = request.json['price']
    task_id = db.menu.insert({'name': name, 'type':type, 'price':price})
    new_task = db.menu.find_one({'_id': task_id })
    output = {'name' : new_task['name'], 'type': new_task['type'], 'price': new_task['price']}
    return jsonify({'result' : output})    


class MenuAPI(Resource):
    
  def get(self, task_id):
    task = db.menu
    new_task = task.find_one({ '_id': ObjectId(task_id) })
    # print('new_task', new_task)    
    output = {'_id': str(new_task['_id']), 'name' : new_task['name'], 'type' : new_task['type'], 'price' : new_task['price']}
    return jsonify({'result' : output})

  def put(self, task_id):  
    task = db.menu  
    price = request.json['price']
    data = {'price': price}   
    task.update({'_id': ObjectId(task_id)}, {'$set': data})
    new_task = task.find_one({'_id': ObjectId(task_id) })
    # print('new_task', new_task)   
    output = {'_id': str(new_task['_id']), 'name' : new_task['name'], 'type' : new_task['type'], 'price' : new_task['price']}
    return jsonify({'result' : output})

  def delete(self, task_id):
    db.menu.delete_one({ '_id': ObjectId(task_id) })
    return jsonify({'result' : 'item has been deleted'})




api.add_resource(TableListAPI, '/api/v1/table', endpoint='table')
api.add_resource(TableAPI, '/api/v1/table/<string:task_id>', endpoint='tables')
api.add_resource(MenuListAPI, '/api/v1/menu', endpoint='menu')
api.add_resource(MenuAPI, '/api/v1/menu/<string:task_id>', endpoint='menus')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 