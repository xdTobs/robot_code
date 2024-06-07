from enum import Enum
from ev3dev2.motor import OUTPUT_C, SpeedPercent, LargeMotor
from robot import BaseRobot,EACTION

class EACTIONWATERMILL(Enum):
    HATCH_FORWARD = "HATCH_FORWARD"
    HATCH_BACKWARD = "HATCH_BACKWARD"
    HATCH_STOP = "HATCH_STOP"


class WaterMill(BaseRobot):
    wheel_distance = 16
    avoidance_distance = 20

    try:
        motor_hatch = LargeMotor(OUTPUT_C)
    except Exception as e:
        print("Error initializing Motors", e)
    
    action_map = {
        **BaseRobot.action_map,
        'j': EACTIONWATERMILL.HATCH_FORWARD,
        'k': EACTIONWATERMILL.HATCH_BACKWARD,
        'l': EACTIONWATERMILL.HATCH_STOP
    }

    def __init__(self):
        super().__init__(self.wheel_distance,self.avoidance_distance, self.default_speed,self.action_map)
   
    def move_forward(self):
        self.steering.on(0, SpeedPercent(-100))

    def move_backward(self):
        self.steering.on(0, SpeedPercent(100))

    def turn_left(self, speed):
        self.mfdiff.turn_left(SpeedPercent(speed), self.turn_degrees, use_gyro=self.use_gyro)

    def turn_right(self, speed):
        self.mfdiff.turn_right(SpeedPercent(speed), self.turn_degrees,use_gyro=self.use_gyro)

   
    def interpret_command_from_key(self, command):
        super().interpret_command_from_key(command)
        self.run_hatch_motor(command)
    
  

    def run_hatch_motor(self, command):
        if command in self.action_map:
            action = self.action_map[command]
            if action == EACTION.FORWARD:
                self.move_forward()
            elif action == EACTION.BACKWARD:
                self.move_backward()
            elif action == EACTIONWATERMILL.HATCH_FORWARD:
                self.motor_hatch.on_for_degrees(SpeedPercent(100), 45)
            elif action == EACTIONWATERMILL.HATCH_BACKWARD:
                self.motor_hatch.on_for_degrees(SpeedPercent(-100), 45)
            elif action == EACTIONWATERMILL.HATCH_STOP:
                self.motor_hatch.off()
        else:
            print("Invalid command")
