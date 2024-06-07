from enum import Enum
from ev3dev2.motor import OUTPUT_C, SpeedPercent, MediumMotor
from robot import BaseRobot, EACTION, AutonomousRobotCommands, ServerRobotCommands


class EACTIONWATERMILL(Enum):
    HATCH_FORWARD = "HATCH_FORWARD"
    HATCH_BACKWARD = "HATCH_BACKWARD"
    HATCH_STOP = "HATCH_STOP"


class WaterMillServerCommands(ServerRobotCommands):
    def interpret_command_from_image_server(self, command, value, socket):
        super().interpret_command_from_image_server(command, value, socket)

        if command == "hatch_forward":
            self.robot.motor_hatch.on_for_degrees(SpeedPercent(100), 45)
        elif command == "hatch_backward":
            self.robot.motor_hatch.on_for_degrees(SpeedPercent(-100), 45)
        elif command == "hatch_stop":
            self.robot.motor_hatch.off()


class WaterMill(BaseRobot):
    wheel_distance = 16
    avoidance_distance = 20

    try:
        motor_hatch = MediumMotor(OUTPUT_C)
    except Exception as e:
        print("Error initializing Motors", e)

    action_map = {
        **BaseRobot.action_map,
        "j": EACTIONWATERMILL.HATCH_FORWARD,
        "k": EACTIONWATERMILL.HATCH_BACKWARD,
        "l": EACTIONWATERMILL.HATCH_STOP,
    }

    def __init__(self):
        super().__init__(
            self.wheel_distance,
            self.avoidance_distance,
            self.default_speed,
            self.action_map,
        )
        self.autonomous_commands = AutonomousRobotCommands(self)
        self.server_commands = WaterMillServerCommands(self)

    def move_forward(self):
        self.steering.on(0, SpeedPercent(-100))

    def move_backward(self):
        self.steering.on(0, SpeedPercent(100))
