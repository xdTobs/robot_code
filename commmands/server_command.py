import socket
from ev3dev2.motor import (
    SpeedPercent,
)

from robot import BaseRobot


class ServerRobotCommands:
    def __init__(self, robot: BaseRobot):
        self.robot = robot

    def move_from_image_server(self, distance_mm):
        self.robot.mfdiff.on_for_distance(
            speed=SpeedPercent(-100), distance_mm=distance_mm
        )
        self.robot.mfdiff.wait_until_not_moving()

    def turn_from_image_server(self, degrees):
        if degrees is None or degrees == 0 or degrees == 360:
            return

        self.robot.mfdiff.turn_degrees(SpeedPercent(100), degrees)
        self.robot.mfdiff.wait_until_not_moving()

    def stop(self):
        self.robot.mfdiff.stop()

    def catch_ball(self, distance_mm):
        print("catching ball")
        self.robot.mfdiff.on_for_distance(
            speed=SpeedPercent(-100), distance_mm=distance_mm
        )

    def test_drive(self):
        print("Wheel distance", self.wheel_distance)
        self.robot.mfdiff.on_arc_left(SpeedPercent(-50), 128.0, 400)

    def interpret_command_from_image_server(
        self, command, value, socket: socket.socket
    ):
        if command == "move":
            if value:
                self.move_from_image_server(value)
            else:
                print("Invalid distance")
        elif command == "catch-ball":
            if value:
                self.catch_ball(value)
            else:
                self.catch_ball(200)
        elif command == "turn":
            self.turn_from_image_server(value)
        elif command == "test-drive":
            self.test_drive()
        elif command == "stop":
            self.stop()
        else:
            print("Invalid command")
        socket.sendall("done".encode())
