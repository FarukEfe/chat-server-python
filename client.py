import socket
import threading
import select
import keyboard

HOST = "127.0.0.1"
PORT = 3000
SOCKS_VERSION = 5

class Client:

    message = ""
    listening = 0

    def __init__(self):
        u = input("Type in username: ")
        self.username = u

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        threading.Thread(self.cycle(s))
    
    def cycle(self, con):
        while True:
            #receives new data every turn
            data = con.recv(1024).decode()
            if not data:
                continue
            print(f"from server: {str(data)}")

            #listens for message
            if self.listening == 0:
                threading.Thread(self.listen_message())
                self.listening = 1
            
            # Send message if complete
            if self.message != "":
                con.send(self.message.encode())
                self.message = ""
                self.listening = 0
    
    def listen_message(self):
        m = input(" -> ")
        if keyboard.is_pressed("enter"):
            self.message = m

if __name__ == "__main__":
    client = Client()
    client.connect()