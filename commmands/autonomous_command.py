from ev3dev2.motor import (
    SpeedPercent,
)
from time import sleep
from enum import Enum

from robot import BaseRobot


class EACTION(Enum):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    STOP = "STOP"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class AutonomousRobotCommands:
    def __init__(self, robot: BaseRobot):
        self.robot = robot

    def __move_forward(self):
        self.robot.steering.on(0, SpeedPercent(100))

    def __move_backward(self):
        self.robot.steering.on(0, SpeedPercent(-100))

    def __turn_left(self, speed):
        self.robot.mfdiff.turn_left(
            SpeedPercent(speed), self.robot.turn_degrees, use_gyro=self.robot.use_gyro
        )

    def __turn_right(self, speed):
        self.robot.mfdiff.turn_right(
            SpeedPercent(speed), self.robot.turn_degrees, use_gyro=self.robot.use_gyro
        )

    def __stop(self):
        self.robot.mfdiff.stop()

    def __speak(self, message):
        self.robot.sound.speak(message)
        print(message)

    def avoid_obstacle(self):
        if (
            self.robot.dist_sensor
            and self.robot.dist_sensor.distance_centimeters
            < self.robot.avoidance_distance
        ):
            self.stop()
            print("Obstacle detected, turning left")
            sleep(1)
            self.turn_left(speed=70)
            self.move_forward()
