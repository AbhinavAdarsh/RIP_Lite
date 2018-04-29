import socket
import pickle
import os
import time


def check_if_modified(oldtime, filename):

    newtime = os.path.getmtime(filename)

    if newtime - oldtime > 0:
        # print("modified")
        return True

    return False


def client_node(node, ports, neighbours, oldtime):

    with open(node + "_dis_vectors.p", "rb") as fp:
        dis_vector = pickle.load(fp)
    start_time = time.time()
    try:
        for key in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created successfully")
            s.connect(("127.0.0.1", ports[key]))
            bytestream = pickle.dumps(dis_vector)

            print("Node\t Distance\t Next Hop")
            for ele in dis_vector:
                print(str(ele) + "\t\t" + str(dis_vector[ele][0]) + "\t\t" + str(dis_vector[ele][1]))

            s.send(bytestream)
            end_time = time.time()
            s.close()
    except socket.error as err:
        print("Socket creation failed with error", err)

    while True:
        time.sleep(0.2)
        if (time.time() - end_time) > 2.0:
            print("Convergence Time for "+ str(node) + " = " + str((end_time - start_time)*1000) + " milliseconds")

        if check_if_modified(oldtime, node+"_dis_vectors.p"):
            oldtime = os.path.getmtime(node + "_dis_vectors.p")

            with open(node + "_dis_vectors.p", "rb") as f:
                dis_vector = pickle.load(f)

            try:
                for key in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # print("Socket created successfully")
                    s.connect(("127.0.0.1", ports[key]))
                    bytestream = pickle.dumps(dis_vector)
                    end_time = time.time()

                    print("Node\t Distance\t Next Hop")
                    for ele in dis_vector:
                        print(str(ele) + "\t\t" + str(dis_vector[ele][0]) + "\t\t" + str(dis_vector[ele][1]))

                    s.send(bytestream)
                    s.close()
            except socket.error as err:
                print("Socket creation failed with error", err)
        else:
            # Check if modified after 15 seconds, if not modified anytime
            time.sleep(15)






