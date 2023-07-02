#!/bin/python3

import datetime
import socket
import threading
import os
import random
import colorama
from colorama import Fore, Back, Style

os.system("cls")
colorama.init()
# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("93.183.74.106", 55559))  # здесь ip адрес сервера

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode("utf8")
            if message == "NICK":
                client.send(nickname.encode("utf8"))
            else:
                print(message)            
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write():
    try:
        while True:
            # input message we want to send to the server
            message =  input()
            # a way to exit the program
            if message.lower() == 'q':
                break
            # add the datetime, name & the color of the sender
            date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            message = f"{client_color}[{date_now}] {nickname}: {message}{Fore.RESET}"
            # finally, send the message
            client.send(message.encode("utf8"))

            # message = "{}: {}".format(nickname, input(""))
            # client.send(message.encode("utf8"))
    except EOFError:
        print("Exception handled")

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
