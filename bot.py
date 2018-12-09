#/usr/bin/env python
#coding=utf-8
from bottle import route, run,static_file
from bottle import request,view,response
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
    jso=json.dumps(js['tbs'])
    c.execute("""REPLACE INTO TBarrange (Week_ID,count,json)
      VALUES (?,?,?)""",(id,count,jso))
    conn.commit()
    conn.close()
    return {"status":"OK"}

@route('/ajax', method = 'GET')
def ajax():
    week=request.GET.get('week')
    conn = sqlite3.connect('ddd.db')
    c = conn.cursor()
    r=c.execute('SELECT * FROM TBarrange WHERE Week_ID=?',(week,))    
    if(r):
        rec=r.fetchone()
        ret={}
        ret['firstday']=rec[0]
        ret['count']=rec[1]
        ret['tbs']=json.loads(rec[2])
    else:
        ret = {'status':'notFound'}
    conn.close()
    response.content_type = 'application/json'
    return json.dumps(ret)
    
    

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