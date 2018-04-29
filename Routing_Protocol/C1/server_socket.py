import socket
import pickle


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

