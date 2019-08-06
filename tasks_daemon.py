import pickle
import socket
import sys
import queue
import threading


_tasksInfoQueue = queue.Queue(maxsize=5)

class GTasksThread(threading.Thread):
    def __init__ (self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", self.cAddr)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = 'Thanks'

        data = self.cSocket.recv(2048)
        taskInfo = pickle.loads(data)
#        print("taskInfo recv is: ", taskInfo)

        try:
            _tasksInfoQueue.put(taskInfo)
        except queue.Full:
            print("Unable to add more items.. exiting")
            exit()

        self.cSocket.send(pickle.dumps(msg))
        print("Client at ", self.cAddr , " disconnected...")
        

class ConsumeTasksThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("consumer thread is waiting for data in queue")

    def run(self):
        while True:
            print("checking if data is to be processed")
            try:
                taskInfo = _tasksInfoQueue.get(True, 2)
                print (taskInfo)
            except queue.Empty:
                continue

def Main():
    host = "localhost"

    port = 6264
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)


    # The following consumer thread will wait for data in queue then process
    consumeTasksThread = ConsumeTasksThread()
    consumeTasksThread.start()
    while True:
        s.listen(5)

        clientSock, clientAddr = s.accept()

        # The Producer threads
        thread = GTasksThread(clientAddr, clientSock)
        thread.start()

if __name__ == '__main__': 
    Main() 
