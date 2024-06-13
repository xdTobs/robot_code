#!/usr/bin/env python3
import select
from time import sleep
from utils.battery import get_battery_status
from robot_factory import RobotFactory
from prototype_enum import Prototypes
import json
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
HOST = s.getsockname()[0]
PORT = 65438  # Port to listen on (non-privileged ports are > 1023)
s.close()


print("HOST", HOST)
print("PORT", PORT)

robot = RobotFactory.create_robot(Prototypes.TOWER)

print("robot", robot)

print("motor orientation forward", robot.motor_orientation_forward)


def connect_to_server():
    print("Ready to connect to server")
    robot.sound.tone([(1000, 500, 500)])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.setblocking(False)
    return conn, addr, s


def handle_connection(conn, addr):
    print("Battery percentage: ", get_battery_status())
    print("motor orientation forward", robot.motor_orientation_forward)
    print("Connected to server by addr:", addr)

    try:
        while True:
            ready = select.select([conn], [], [], 0.1)[0]
            # robot.avoid_obstacle()

            if ready:
                data = conn.recv(4000)
                print("Data received", data)
                data = data.decode()
                data = data.split("}{")
                for i in range(len(data)):
                    if i != 0:
                        data[i] = "{" + data[i]
                    if i != len(data) - 1:
                        data[i] = data[i] + "}"
                    key_value_pair = json.loads(data[i])
                # key_value_pair = json.loads(data)
                try:
                    command = key_value_pair.get("command")
                    value = key_value_pair.get("value")
                    speedPercentage = key_value_pair.get("speedPercentage")
                except Exception as e:
                    print("Could not parse data")
                    continue
                if value is not None:
                    value = float(value)
                robot.interpret_command_from_image_server(
                    command, value, conn, speedPercentage
                )
    except Exception as e:
        print("Exception", e)
        return False


if __name__ == "__main__":
    while True:
        conn, addr, s = connect_to_server()
        try:
            if handle_connection(conn, addr):
                break
        except Exception as e:
            robot.stop()
            robot.belt_motor.on_for_seconds(0, 255, 3, block=False)
            robot.belt_motor.off()
            print("Error occurred: ", e)
            print("Attempting to reconnect...")
            sleep(5)
        finally:
            conn.close()
            s.close()
