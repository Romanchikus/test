import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=10008
client.connect(('localhost', port))
sendi1="%2F%3Ftask%3D%D0%9F%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D1%83%20%D0%B4%D0%BB%D1%8F%20%D0%B2%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D0%BA%D0%B0%20%D0%BD%D0%B0%20%D0%B7%D0%B0%D0%B2%D1%82%D1%80%D0%B0%26amp%3B%20users%3D%5B%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C1%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9CJohn%E2%80%9D%2C%E2%80%9ClastName%E2%80%9D%3A%E2%80%9CSmith%E2%80%9D%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C4%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%9E%D0%BB%D1%8C%D0%B3%D0%B0%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%9F%D1%8B%D0%BB%D0%B5%D0%B2%D0%B0%E2%80%9C%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C10%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%A2%D0%B0%D1%80%D0%B0%D1%81%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%A1%D0%B0%D0%B3%D0%B0%D0%B9%D0%B4%D0%B0%D1%87%D0%BD%D0%B8%D0%B9%E2%80%9C%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C12%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%92%D0%BB%D0%B0%D0%B4%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%A1%D0%B8%D0%B4%D0%BE%D1%80%D1%87%D1%83%D0%BA%E2%80%9C%7D%5D%26amp%3B%20apiKey%3DAIzaSyDa-3reugkWAvksex60RKzTGkk80AXqolI%26amp%3B%20languageCode%3Den%20HTTP%2F1.1%0A"
sendi2="%2F%3Ftask%3D%D0%B2%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D0%BA%26amp%3B%20users%3D%5B%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C1%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9CJohn%E2%80%9D%2C%E2%80%9ClastName%E2%80%9D%3A%E2%80%9CSmith%E2%80%9D%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C4%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%9E%D0%BB%D1%8C%D0%B3%D0%B0%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%9F%D1%8B%D0%BB%D0%B5%D0%B2%D0%B0%E2%80%9C%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C10%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%A2%D0%B0%D1%80%D0%B0%D1%81%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%A1%D0%B0%D0%B3%D0%B0%D0%B9%D0%B4%D0%B0%D1%87%D0%BD%D0%B8%D0%B9%E2%80%9C%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C12%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%92%D0%BB%D0%B0%D0%B4%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%A1%D0%B8%D0%B4%D0%BE%D1%80%D1%87%D1%83%D0%BA%E2%80%9C%7D%5D%26amp%3B%20apiKey%3DAIzaSyDa-3reugkWAvksex60RKzTGkk80AXqolI%26amp%3B%20languageCode%3Den%20HTTP%2F1.1%0A"
sendi3="%2F%3Ftask%3D%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D1%83%20%D0%BD%D0%B0%D1%82%D0%B0%D0%BB%D0%B8%D0%B8%26amp%3B%20users%3D%5B%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C1%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9CJohn%E2%80%9D%2C%E2%80%9ClastName%E2%80%9D%3A%E2%80%9CSmith%E2%80%9D%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C4%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%9E%D0%BB%D1%8C%D0%B3%D0%B0%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%9F%D1%8B%D0%BB%D0%B5%D0%B2%D0%B0%E2%80%9C%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C10%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%A2%D0%B0%D1%80%D0%B0%D1%81%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%A1%D0%B0%D0%B3%D0%B0%D0%B9%D0%B4%D0%B0%D1%87%D0%BD%D0%B8%D0%B9%E2%80%9C%7D%2C%7B%E2%80%9Cid%E2%80%9D%3A%E2%80%9C12%22%2C%E2%80%9CfirstName%E2%80%9D%3A%E2%80%9C%D0%92%D0%BB%D0%B0%D0%B4%E2%80%9C%2C%E2%80%9DlastName%E2%80%9D%3A%E2%80%9C%D0%A1%D0%B8%D0%B4%D0%BE%D1%80%D1%87%D1%83%D0%BA%E2%80%9C%7D%5D%26amp%3B%20apiKey%3DAIzaSyDa-3reugkWAvksex60RKzTGkk80AXqolI%26amp%3B%20languageCode%3Den%20HTTP%2F1.1"
client.send(sendi2.encode('utf-8'))
data = b""
while True: # ждём первую строку
    tmp = client.recv(1024)
    if not tmp: break
    data += tmp
    print(data.decode("utf-8"))
client.close()
