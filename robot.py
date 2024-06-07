from ev3dev2.motor import (
    OUTPUT_A,
    OUTPUT_B,
    SpeedPercent,
    MoveDifferential,
    MoveSteering,
)
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
from ev3dev2.wheel import EV3Tire
from ev3dev2.sound import Sound

from commmands.autonomous_command import AutonomousRobotCommands
from commmands.server_command import ServerRobotCommands


class BaseRobot:
    STUD_MM = 8
    wheel_distance = 0
    default_speed = 250
    mdiff = None
    steering = None
    dist_sensor = None
    avoidance_distance = 15
    turn_degrees = 90
    motor_orientation_forward = True
    use_gyro = False

    def __init__(self, wheel_distance, avoidance_distance, default_speed, action_map):
        self.wheel_distance = wheel_distance
        self.avoidance_distance = avoidance_distance
        self.default_speed = default_speed
        self.update_action_map(action_map)

        self.sound = Sound()

        try:
            print("wheel distance", self.wheel_distance)
            self.mfdiff = MoveDifferential(
                OUTPUT_A,
                OUTPUT_B,
                EV3Tire,
                float(self.STUD_MM) * float(self.wheel_distance),
            )
            self.steering = MoveSteering(OUTPUT_A, OUTPUT_B)

        except Exception as e:
            print("Error initializing Motors", e)

        try:
            self.dist_sensor = UltrasonicSensor()
            self.mfdiff.gyro = GyroSensor()
        except Exception as e:
            print("Error initializing Sensors", e)

        if self.mfdiff.gyro:
            self.mfdiff.gyro.calibrate()
            self.use_gyro = True
            print("Gyro calibrated")
        else:
            print("Gyro not calibrated")

        if self.dist_sensor:
            print("Distance sensor initialized")

        self.autonomous_commands = AutonomousRobotCommands(self)
        self.server_commands = ServerRobotCommands(self)

    def update_action_map(self, new_action_map):
        self.action_map = {**self.action_map, **new_action_map}

    def test_drive(self):
        print("Wheel distance", self.wheel_distance)
        self.mfdiff.on_arc_left(SpeedPercent(-50), 128.0, 400)

    def robot_information(self):
        print("Robot information")
        print("Max speed", self.steering.max_speed)
        print("Min speed", self.steering.is_running)
