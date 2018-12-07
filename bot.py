#/usr/bin/env python
#coding=utf-8
from bottle import route, run,static_file
from bottle import request,view
import os
import sqlite3
import json

@route('/sql', method = 'POST')
def savejson():
    js=request.POST.get('data')
    conn = sqlite3.connect('ddd.db')
    c = conn.cursor()
    js=json.loads(js)
    id=js['firstday']
    count=js['count']
    jso=js['tbs']
    c.execute("""INSERT INTO TBarrange (Week_ID,count,json)
      VALUES (?,?,?)""",(id,count,jso));
    return {"status":"OK"}

@route('/ajax', method = 'GET')
def savejson():
    js=request.POST.get('data')
    with open('data.json', 'w') as f:
        f.write('{"data":'+js+'}')
    return {"status":"OK"}

@route('/<name:re:images|css|js|icons>/<path:path>')
def static_img(name,path):
    return static_file(path,root="./"+name)

@route('/')
def index():
    return static_file('week.html',root="./")
@route('/favicon.ico')
def fav():
    return static_file('favicon.ico',root="./")



run(host='0.0.0.0', port=8080, debug=True)