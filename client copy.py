#!/usr/bin/env python3
import socket
import select
from time import sleep
from battery import get_battery_status
from robot_factory import RobotFactory
from prototype_enum import Prototypes
import json

HOST = "192.168.226.124"  # Standard loopback interface address (localhost)
# HOST = "localhost"
PORT = 65438  # Port to listen on (non-privileged ports are > 1023)

print("HOST", HOST)
print("PORT", PORT)
print("Battery percentage: ", get_battery_status())

robot_number = int(input("Enter the robot number: "))

robot_type = Prototypes.from_int(robot_number)
robot = RobotFactory.create_robot(robot_type)

print("motor orientation forward", robot.motor_orientation_forward)

print("Ready to connect to server")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.setblocking(False)

    with conn:
        print('Connected to server by addr:', addr)
        conn.sendall("done".encode())

        while True:

            ready = select.select([conn], [], [], 0.1)[0]
            
            robot.avoid_obstacle()

            if ready:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    key_value_pair = json.loads(data.decode())
                    command = key_value_pair.get("command")
                    value = key_value_pair.get("value")
                    if value != None:
                        value = float(value)
                    
                    
                    robot.interpret_command_from_image_server(command,value, conn)

                    #command = data.decode("utf-8")
                    #print("Command received:", command)
                    #robot.interpret_command_from_key(command)
                except Exception as e:
                    print("Error executing command", e)
conn.close()
