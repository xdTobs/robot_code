#!/usr/bin/env python3
import socket
import select
from time import sleep
from utils.battery import get_battery_status
from robot_factory import RobotFactory
from prototype_enum import Prototypes
import json

HOST = "172.20.10.3"  # Standard loopback interface address (localhost)
# HOST = "localhost"
PORT = 65438  # Port to listen on (non-privileged ports are > 1023)


print("HOST", HOST)
print("PORT", PORT)

robot_number = 1 

robot_type = Prototypes.from_int(robot_number)
robot = RobotFactory.create_robot(robot_type)

print("motor orientation forward", robot.motor_orientation_forward)
def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.setblocking(False)
    return conn, addr, s


def handle_connection(conn, addr, s):
    print("Ready to connect to server")
    print("Battery percentage: ", get_battery_status())

    robot_number = 1
    robot_type = Prototypes.from_int(robot_number)
    robot = RobotFactory.create_robot(robot_type)

    print("motor orientation forward", robot.motor_orientation_forward)
    print('Connected to server by addr:', addr)

    try:
        while True:
            ready = select.select([conn], [], [], 0.1)[0]
            robot.avoid_obstacle()

            if ready:
                data = conn.recv(1024)
                if not data:
                    raise ConnectionError("Connection lost")
                key_value_pair = json.loads(data.decode())
                command = key_value_pair.get("command")
                value = key_value_pair.get("value")
                if value is not None:
                    value = float(value)
                robot.interpret_command_from_image_server(command, value, conn)
    except Exception as e:
        print("Error executing command", e)
        s.close()
        return False
    return True
    
if __name__ == '__main__':
    while True:
        conn, addr, s = connect_to_server()
        while not handle_connection(conn, addr, s):
            print("Attempting to reconnect...")
            sleep(5) 
        else:
            break