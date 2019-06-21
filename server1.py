import time
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
port=10014

def parse(conn, addr):# обработка соединения в отдельной функции
    
    while True:
        data = b""
        tmp = conn.recv(1024)
        data += tmp
        if not tmp: break
        try:
            url=urllib.request.url2pathname(data.decode("utf-8"))
            disc=dict(urllib.parse.parse_qsl(url))
            print("dict:"+disc['/?task']) 
            try:
                datas = truemess(disc['/?task'])
                b = "“”"
                for char in b:
                    disc[' users'] = disc[' users'].replace(char,'"')
                print(disc[' users'])
                dicc=ast.literal_eval(disc[' users'])
                for it in dicc:
                    it = dict(it)
                    for key, val in it.items():
                        if it[key] == datas["firstName"]:
                            data = it["id"]
            except Exception as err:
                print('Ошибка:\n', traceback.format_exc())
                print(err)
                data = "Eror"
            
            data = data.encode('utf-8')
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
            conn.settimeout(60.0) 
            print("New connection from " + addr[0])
            try:
                start_new_thread(parse, (conn,addr,))
            except Exception as err:
                print('Ошибка:\n', traceback.format_exc())
            #     conn.close()
    finally: sock.close()

if __name__ == '__main__': 
    Main() 