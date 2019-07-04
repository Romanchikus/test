import socket
import urllib.parse
import json
import ast

# from datetime import datetime
# stit = '2019-06-27T12:00:00+03:00'
# stit = stit[:10]
# now = datetime.now()
# then = datetime.strptime(stit, '%Y-%m-%d')
# delta =  then-now
# print(now)
# print(delta.days+1)



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=10011
client.connect(('localhost', port))
# пусть тарас уберет в комнате завтра
# I want john Johnson to prepare food tomorrow
# 6
# I want john smith to prepare food tomorrow
# пусть пылевая сделает задание до завтра до 18 часов  

# "task=set task to John Smith make a cake until may the first 2012&users=[{\"id\":\"1234\", \"firstName\":\"John\", \"lastName\":\"Smith\"}]&apiKey=aaaabbbbccccddddeeeeffffhhhhllll" 
while True: # ждём первую строку
    dud=input()
    ded = 'task=Поставить задачу для виталика на завтра&amp; users=[{"id":"1","firstName":"John","lastName":"Smith"},{"id":"4","firstName":"Ольга","lastName":"Пылева"},{"id":"10","firstName":"Тарас","lastName":"Сагайдачний"},{"id":"12","firstName":"Влад","lastName":"Сидорчук"}]&amp; apiKey=AIzaSyDa-3reugkWAvksex60RKzTGkk80AXqolI&amp; languageCode=en HTTP/1.1'
    dud = 'task=' + dud
    dud = dud + '&users=[{"id":"1","firstName":"John","lastName":"Smith"},{"id":"6","firstName":"John","lastName":"Johnson"},{"id":"4","firstName":"Ольга","lastName":"Пылева"},{"id":"10","firstName":"Тарас","lastName":"Сагайдачний"},{"id":"12","firstName":"Влад","lastName":"Сидорчук"}]&amp; apiKey=AIzaSyDa-3reugkWAvksex60RKzTGkk80AXqolI&amp; languageCode=en HTTP/1.1'
    # dud=urllib.parse.quote(dud)
    client.sendall(dud.encode('utf-8'))
    data = b""
    tmp = client.recv(1024)
    if not tmp: break
    data += tmp
    data=data.decode("utf-8")
    json_string = json.dumps(data)
    data = ast.literal_eval(json.loads(json_string))
    # data["query"] = data["query"].decode('utf-8', 'ignore')
    print(data)
    # print(duda)
client.close()


