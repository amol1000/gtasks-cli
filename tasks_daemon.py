import pickle
import socket
import sys
import threading


class GTasksThread(threading.Thread):
    def __init__ (self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddress
        print ("New connection added: ", clientAddress)

    def run(self):
        print ("Connection from : ", self.cAddr)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = 'Thanks'

        data = self.cSocket.recv(2048)
        taskInfo = pickle.loads(data)
        print ("taskInfo recv is: ", taskInfo)
        
        self.cSocket.send(pickle.dumps(msg))
        print ("Client at ", self.cAddr , " disconnected...")
        


def Main():
    host = "localhost"

    port = 6264
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)


    while True:
        s.listen(5)

        clientSock, clientAddr = s.accept()

        # The Producer threads
        thread = GTasksThread(clientAddr, clientSock)
        thread.start()

if __name__ == '__main__': 
    Main() 
