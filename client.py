import socket 
import requests
import json
from threadwithreturn import ThreadWithReturn as RetThread
from threading import Thread

portStart = 8005

def login(username_ : str, password : str):
    url = "http://127.0.0.1:5000/acc"

    payload = json.dumps({"username": username_,"password": password, "IP": socket.gethostbyname(socket.gethostname()), "port": portStart})
    
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return username_

def recv_input_stream(conn, addr):
    #  Grand grandchild thread
    #  Handle the input stream
    try:
        data = conn.recv(1024).decode()
        if data.lower().strip() == 'bye':
            # if data is not received break
            print("Say goodbye from client " + str(addr) + '\n')
            conn.close()
            return -1
        print("from connected user: " + str(data) + '\n')
    except:
        return -1

def accept_connection(connection, address):
    #  Grandchild thread
    #  Create new thread for each input stream
    while True:
        input_stream = RetThread(target=recv_input_stream, args=(connection, address,))
        input_stream.start()
        val = input_stream.join()
        if val == -1:
            return

def init():
    hostname = socket.gethostname()
    ipAddr = socket.gethostbyname(hostname)
    server = socket.socket()
    server.bind((ipAddr,portStart))
    server.listen(10)
    while True:
        conn, addr = server.accept()
        print("Connection from: " + str(addr) + '\n')
        client_conn = Thread(target=accept_connection, args=(conn, addr, ))
        client_conn.start()
    
def client_program(username):
    url = "http://127.0.0.1:5000/getIP"

    payload = json.dumps({"username": username})
    headers = {'Content-Type': 'application/json'}

    response = requests.request("GET", url, headers=headers, data=payload)

    host = response.json()[0]['IP']
    port = response.json()[0]['port']

    client_socket = socket.socket()
    print("Connected to " + str(host) + ':' + str(port) + '\n')
    client_socket.connect((host,port))

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message

        message = input(" -> ")  # again take input

    client_socket.send(message.encode())  # send bye message
    client_socket.close()
        

username = login("test1", "test1")
temp = Thread(target= init, args=())
temp.start()
client_program("test")



    
    


