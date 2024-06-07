from ev3dev2.motor import OUTPUT_C, MediumMotor, SpeedPercent
from enum import Enum
from robot import BaseRobot, AutonomousRobotCommands, ServerRobotCommands


class ETOWER_ACTION(Enum):
    BELT_FORWARD = "BELT_FORWARD"
    BELT_BACKWARD = "BELT_BACKWARD"
    BELT_STOP = "BELT_STOP"


class Tower(BaseRobot):
    wheel_distance = 11
    avoidance_distance = 20
    default_speed = 100
    motor_orientation_forward = False

    action_map = {
        **BaseRobot.action_map,
        "j": ETOWER_ACTION.BELT_FORWARD,
        "k": ETOWER_ACTION.BELT_BACKWARD,
        "l": ETOWER_ACTION.BELT_STOP,
    }

    try:
        belt_motor = MediumMotor(OUTPUT_C)
    except Exception as e:
        print("Error initializing motors", e)

    def __init__(self):
        super().__init__(
            self.wheel_distance,
            self.avoidance_distance,
            self.default_speed,
            self.action_map,
        )
        self.autonomous_commands = AutonomousRobotCommands(self)
        self.server_commands = TowerServerCommands(self)

    def move_forward(self):
        self.steering.on(0, SpeedPercent(-100))

    def move_backward(self):
        self.steering.on(0, SpeedPercent(100))


class TowerServerCommands(ServerRobotCommands):
    def __init__(self, robot: Tower):
        super().__init__(robot)

    def interpret_command_from_image_server(self, command, value, socket):
        super().interpret_command_from_image_server(command, value, socket)

        if command == "belt":
            self.robot.belt_motor.on(SpeedPercent(value))
        elif command == "beltstop":
            self.robot.belt_motor.off()
