#!/bin/python3

import socket
import threading

# Connection Date
host = '93.183.74.106' # IP адресс удаленного сервера (myserverspace.ru)
port = 55555 # Порт можно выбирать любой, главное, чтобы он не был занят (65235 - 16 байт)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET - сокет ipv4
# SOCK_STREAM - тип сокета - TCP
server.bind((host, port)) # привязываем к серверу хост и порт
server.listen()

# Lists For Clients and Their Nicknams
clients = [] # массив клиентов
nicknames = [] # массив ников

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handing Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf8'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        #Request And Store Nickname
        client.send('NICK'.encode('utf8'))
        nickname = client.recv(1024).decode('utf8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf8'))
        client.send('Connected to server!'.encode('utf8'))

        # Start Handing Thread Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Closing Socket Clients And Server
def closAll():
    for client in clients:
        client.close()
    server.close()

print("Server if listening...")
receive()
closAll()

