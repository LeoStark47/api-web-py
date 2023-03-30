
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
from flask_cors import CORS
#from datetime import datetime, timedelta
import json
#import random

app = Flask(__name__)

#CORS(app, resources={r"/*": {"origins": "*"}})

raspberry = []
jsonFile = open('raspberry.json', 'r')
raspberryJson = json.load(jsonFile)
for i in raspberryJson['raspberry']:
    raspberry.append(i)
showState = raspberryJson['show']
jsonFile.close()

def getAll(scope):
    if scope == '':
        return jsonify(raspberry)
    elif scope == 'temperatura' or scope == 'humedad' or scope == 'humo' or scope == 'luz':
        subTiempo = [sub['tiempo'] for sub in raspberry]
        subFeature = [sub[scope] for sub in raspberry]

        feature = []
        for i in range(len(subFeature)):
             feature.append({
                'tiempo': subTiempo[i],
                scope: subFeature[i]
            })
        return jsonify(feature)

def postFeatures(req):
    raspberry.append(req)
    raspberryJson['raspberry'].append(req.json)
    jsonFile = open('raspberry.json', 'w+')
    jsonFile.write(json.dumps(raspberryJson))
    jsonFile.close()
    return 'Se agregó la información correctamente'

def changeShowState(show):
    global showState
    showState = show
    raspberryJson['show'] = show
    jsonFile = open('raspberry.json', 'w+')
    jsonFile.write(json.dumps(raspberryJson))
    jsonFile.close()
    return "Solicitud correcta. Status de Show cambiado."

@app.route('/',methods = ['GET','POST','PUT'])
def hello_world():
    if request.method == 'GET':
        if(showState):
            return getAll('')
        return []
    if request.method == 'POST':
        return postFeatures(request.json('raspberry'))
    if request.method == 'PUT':
        return changeShowState(request.json['show'])

@app.route('/raspberry/features', methods = ['GET','POST','PUT'])
def raspberryFeatures():
    if request.method == 'GET':
        if(showState):
            return getAll('')
        return []
    if request.method == 'POST':
        return postFeatures(request)
    if request.method == 'PUT':
        return changeShowState(request.json['show'])

@app.route('/raspberry/features/temperatura', methods = ['GET'])
def temperaturas():
    global showState
    if(showState):
        return getAll('temperatura')
    return []

@app.route('/raspberry/features/humedad', methods = ['GET'])
def humedades():
    global showState
    if(showState):
        return getAll('humedad')
    return []

@app.route('/raspberry/features/humo', methods = ['GET'])
def humos():
    global showState
    if(showState):
        return getAll('humo')
    return []

@app.route('/raspberry/features/luz', methods = ['GET'])
def luces():
    global showState
    if(showState):
        return getAll('luz')
    return []

