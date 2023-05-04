import socket
import threading
import select
import keyboard

IP_ADRESS = "127.0.0.1"
PORT = 3000
SOCKS_VERSION = 5

USERNAME = "e-server"
PASSWORD = "secureconnection"

class Server:

    message = ""
    listening = 0

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def handle_client(self, connection):
        while True:
            data = connection.recv(1024).decode()
            if not data:
                continue
            print(f"from user: {str(data)}")

            if self.listening == 0:
                threading.Thread(self.listen_message())
                self.listening = 1

            if self.message != "":
                connection.send(self.message.encode())
                self.message = ""
                self.listening = 0

    # Start server
    def run(self, host, port):
        # Socket bind to host from port and start listening
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()

        # Testing
        print("* Socks5 proxy server is running on {}:{}".format(host,port))

        while True:
            conn, addr = s.accept()
            print("* new connection from {}".format(addr))
            # After listening for connection, retrieve client data and handle each client in a different thread
            t = threading.Thread(target=self.handle_client, args=(conn,))
            t.start()

    def listen_message(self):
        m = input(" -> ")
        if keyboard.is_pressed("enter"):
            self.message = m
            
if __name__ == "__main__":
    server = Server(USERNAME, PASSWORD)
    server.run(IP_ADRESS, PORT)