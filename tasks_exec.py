#This executable will add tasks in the given list

import argparse
import pickle
import socket
import sys

server_address = ('localhost', 6264)


def Usage():
    print(" task -a <task name> -dd <due date> -l <task list>")
    print(" at least task name and due date should be given ")

parser = argparse.ArgumentParser("Flags for Tasks")

parser.add_argument("taskName", help="task to be added")
parser.add_argument("taskDueDate", help="task due date of task to be added")
parser.add_argument("tasksList", help="taskList in which task is to be added.")


args = parser.parse_args()



if args.taskName and args.taskDueDate:
    taskInfo = { "action" : "addTask", "taskName" : args.taskName, "taskDueDate" : args.taskDueDate}

    if args.tasksList:
        # if task list is not specified 
        # add task to "My List" by default
        taskInfo["tasksList"] = args.tasksList
        print("This will add task to  ", args.tasksList)
    else:
        taskInfo["tasksList"] = "My List"
        
else:
        Usage()


#print (taskInfo)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Connect the socket to the port where the server is listening
#print >>sys.stderr, 'connecting to %s port %s' % server_address

try:
    sock.connect(server_address)

except socket.timeout:
    print(" Unable to connect to tasks daemon")
    exit()
    
message = pickle.dumps(taskInfo)
sock.sendall(message)

data = sock.recv(1024)
print ("recv is:", pickle.loads(data))
sock.close()
