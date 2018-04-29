from server_socket import server_node
from client_socket import client_node
import pickle
import sys
import os

# Allocate different port for each node
ports = {'h1': 51001, 'r1': 51002, 'r2': 51003, 'r3': 51004, 'r4': 51005, 'h2': 51006}

# Initialize distance vector for each node
node_neighbours = {'h1': ('inf', '-'), 'r1': ('inf', '-'), 'r2': ('inf', '-'), 'r3': ('inf', '-'), 'r4': ('inf', '-'),
                   'h2': ('inf', '-')}


# Read weights from the file
def read_weights():
    with open('C2/initial_weights.txt') as rp:
        lines = rp.readlines()

    return lines


# Initialize the distance vectors as per the topology (Initial weights)
def initial_dist_vectors(node, port, lines):

    for line in lines:
        node1, node2, weight = line.strip().split(',')
        if node1 == node:
            node_neighbours[node2] = (weight, node1)
        elif node2 == node:
            node_neighbours[node1] = (weight, node2)

    node_neighbours[node] = (0, node)
    for key in node_neighbours:
        print(key, node_neighbours[key])

    with open(node+"_dis_vectors.p", "wb") as dvp:
        pickle.dump(node_neighbours, dvp)

    mod_time = os.path.getmtime(node + "_dis_vectors.p")

    return mod_time


def main():

    # c_s = eval(input("Run Server(Press 1) or Client(Press 2) in the current window : "))
    c_s = int(sys.argv[1])
    node = sys.argv[2]
    port = ports[node]

    init_weights = read_weights()
    mod_time = initial_dist_vectors(node, port, init_weights)
    oldtime = mod_time

    if c_s == 1:
        print("Server")
        print("Node = ", node)
        print("Port = ", port)
        server_node(node, port, node_neighbours, mod_time)
    else:
        print("Client")
        print("Node = ", node)
        print("Port = ", port)
        client_node(node, ports, node_neighbours, mod_time)


if __name__ == '__main__':
    main()
