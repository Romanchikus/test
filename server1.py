# import time
import socket
import json
import urllib.request
import re
import sys
from servrom1 import truemess
import traceback
from _thread import *
import threading
import ast
port=10011
# from datetime import datetime


def parse(conn, addr):
    
    while True:
        data = b""
        tmp = conn.recv(1024)
        data += tmp
        if not tmp: break
        try:
            url=urllib.request.url2pathname(data.decode("utf-8"))
            disc=dict(urllib.parse.parse_qsl(url))
            try:
                lang = disc[' languageCode'][:2]
                datas = truemess(disc['task'],lang)
                
                dicc=ast.literal_eval(disc['users'])
                data = []
                for it in dicc:
                    it = dict(it)
                    if it["firstName"] == datas["firstName"]:
                        data.append(it["id"])
                # print(len(data))   
                if len(data)== 0:
                    for it in dicc:
                        it = dict(it)
                        if it["lastName"] == datas["lastName"]:
                            data = it["id"]
                            
                elif len(data) > 1:
                    for it in dicc:
                        it = dict(it)
                        if it["lastName"] == datas["lastName"] and it["firstName"] == datas["firstName"]:
                            data = it["id"]
                else:
                    data = data[0]
            except Exception as err:
                print('Ошибка:\n', traceback.format_exc())
                print(err)
                data = "null"
            try:
                stit = datas["date"]
                stit = stit[:10]
                datas["date"] = stit
                # then = datetime.strptime(stit, '%Y-%m-%d')
                # now = datetime.now()
                # delta =  then-now 
                # if delta.days == -1:
                #     datas["date"] = "сьогодні"
                # if delta.days == 0:
                #     datas["date"] = "завтра"
                # if delta.days == -2:
                #     datas["date"] = "вчора"
                # print("delta",delta.days)
            except:
                # print('Ошибка:\n', traceback.format_exc())
                pass
            objectiveTimeAlias = datas["until"] +" "+datas["dateuntil"]
            if objectiveTimeAlias == " ":
                objectiveTimeAlias = "null"
            if not datas["time"]:
                datas["time"] = "null"
            else:
                datas["time"] = datas["time"][11:19]
            if not datas["firstName"]:
                datas["firstName"] = "null"
            if not datas["lastName"]:
                datas["lastName"] = "null"
            if not datas["query"]:
                datas["query"] = "null"
            if not datas["date"]:
                datas["date"] = "null"
            


            data = {'id':data, "firstName":  datas["firstName"], "lastName":  datas["lastName"], "objective":  datas["query"], "objectiveDate":  datas["date"], "objectiveTime":  datas["time"], "objectiveTimeAlias": objectiveTimeAlias }
            data = json.dumps(data).encode('utf-8')
            # data = data.encode('utf-8')
            # datas = json.dumps('{"id": 2, "name": "abc"}').encode('utf-8')
            conn.send(data)
        except:
            pass
    conn.close()
            
def Main(): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind( ("localhost", port) )
    print("socket binded to post", port)
    sock.listen(1)
    try:
        while 1: # работаем постоянно
            conn, addr = sock.accept()
            # conn.settimeout(60.0) 
            print("New connection from " + addr[0])
            try:
                start_new_thread(parse, (conn,addr,))
            except Exception as err:
                print('Ошибка:\n', traceback.format_exc())
            #     conn.close()
    finally: sock.close()

if __name__ == '__main__': 
    Main() 