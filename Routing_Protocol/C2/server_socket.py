import socket
import pickle
import os
import time


def check_if_modified(oldtime, filename):

    newtime = os.path.getmtime(filename)
    if newtime - oldtime > 0:
        return True

    return False


# Read weights from the file
def read_weights():
    with open('C2/initial_weights.txt') as rp:
        lines = rp.readlines()

    return lines


def bellman_ford(node, neighbours_dict, sender_node):

    flag = 0
    with open(node+"_dis_vectors.p", "rb") as bfp:
        dis_vector = pickle.load(bfp)

    for key in dis_vector:
        if neighbours_dict[key][0] != 'inf' and dis_vector[sender_node][0] != 'inf':
            if dis_vector[key][0] == 'inf':
                dis_vector[key] = (int(neighbours_dict[key][0]) + int(dis_vector[sender_node][0]), sender_node)
                flag = 1
            elif int(dis_vector[key][0]) > int(dis_vector[sender_node][0]) + int(neighbours_dict[key][0]):
                dis_vector[key] = (int(dis_vector[sender_node][0]) + int(neighbours_dict[key][0]), sender_node)
                flag = 1
    if flag:
        with open(node + "_dis_vectors.p", "wb") as bf:
            pickle.dump(dis_vector, bf)
        return dis_vector


def server_node(node, port, neighbours, oldtime):
    # Create a socket object
    s = socket.socket()
    print("Socket created successfully")

    # Bind the server to specific port
    # First argument 'empty string' so it listens to other computers as well
    s.bind(('', port))
    print("Socket binded to ", port)

    # Puts the server in the listen mode. Argument signifies number of connections that can be kept waiting
    s.listen(20)
    print("Socket is listening...")

    # Accept incoming requests
    while True:
        sender_node = ""
        c, addr = s.accept()
        print("Got connection from ", addr[1])
        bytestream = c.recv(2048)
        neighbours_dict = pickle.loads(bytestream)

        for key in neighbours_dict:
            if neighbours_dict[key][0] == 0:
                sender_node = key

        dis_vector = bellman_ford(node, neighbours_dict, sender_node)

        if check_if_modified(oldtime, "initial_weights.txt"):
            if node == 'r1' or node == 'r3':
                lines = read_weights()
                for line in lines:
                    node1, node2, weight = line.strip().split(',')
                    if node1 == node:
                        neighbours[node2] = (weight, node1)
                    elif node2 == node:
                        neighbours[node1] = (weight, node2)
                neighbours[node] = (0, node)

                with open(node + "_dis_vectors.p", "wb") as wcp:
                    pickle.dump(neighbours, wcp)

                oldtime = os.path.getmtime(node + "_dis_vectors.p")

        else:
            time.sleep(20)

