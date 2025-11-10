import zmq
import json
import labels
import os
from dotenv import load_dotenv


def main():
    load_dotenv()

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.setsockopt(zmq.IPV4ONLY, 0)
    socket.bind("tcp://*:5555")

    print("Server listening on tcp://*:5555")

    while True:
        msg = socket.recv_string()
        try:
            data = json.loads(msg)
            print("Received JSON:", data)

            try:
                names = []
                type = data["type"]
                if "category" in data:
                    category = data["category"]["name"]
                    names.append((type+"_"+category).lower())
                names.append(type.lower())
                print(names)
                for method_name in names:
                    print(dir(labels))
                    if method_name in dir(labels):
                        func = getattr(labels, method_name)
                        print("Creating label type: ", method_name)
                        func(data)
                        break
                    else:
                        print("Label type ", method_name, " does not exist")
            except Exception as error:
                print("An error occured while creating label: ", error)

        except json.JSONDecodeError:
            print("Received invalid JSON:", msg)


if __name__ == "__main__":
    main()
