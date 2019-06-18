import time
import socket
import json
import urllib.request
import re
from servrom import truemess
import traceback
port=10012
##sdf
def send_answer(conn, data="32423"):
    # conn.send(data.encode("utf-8"))
    try:
        data = truemess(data)
    except Exception as err:
        print('Ошибка:\n', traceback.format_exc())
        print(err)
    
    data = data.encode('utf-8')
    # datas = json.dumps('{"id": 2, "name": "abc"}').encode('utf-8')

    conn.send(data)
    # conn.send(datas)                
    # print( 'send')    


def parse(conn, addr):# обработка соединения в отдельной функции
    
    while True:
        data = b""
        tmp = conn.recv(1024)
        data += tmp
        if not tmp: break
        try:
            url=urllib.request.url2pathname(data.decode("utf-8"))
                # print('url'+url)
            # fragment = urllib.parse.urlparse(url).fragment
            # print('fragment'+fragment)
            disc=dict(urllib.parse.parse_qsl(url))
            # print(disc)
            # b = "[]"
            # for char in b:
            #     disc[' users'] = disc[' users'].replace(char,"")
                # print(disc)
            print("dict:"+disc['/?task'])
            datas = disc['/?task']
            send_answer(conn, data=datas)
        except:
            pass
            

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind( ("localhost", port) )
sock.listen(1)
sock.settimeout(60.0)
try:
    while 1: # работаем постоянно
        conn, addr = sock.accept()
        conn.settimeout(60.0) 
        print("New connection from " + addr[0])
        try:
            parse(conn, addr)
        except Exception as err:
            print('Ошибка:\n', traceback.format_exc())
            # print('Connect dis')
            # send_answer(conn, data="Ошибка")
        # finally:
        #     conn.close()
finally: sock.close()
