from ev3dev2.motor import OUTPUT_C,OUTPUT_D, LargeMotor, SpeedPercent,MoveSteering
from enum import Enum
from robot import EACTION, BaseRobot


class ETOWER_ACTION(Enum):
    BELT_FORWARD = "BELT_FORWARD"
    BELT_BACKWARD = "BELT_BACKWARD"
    BELT_STOP = "BELT_STOP"


class Tower(BaseRobot):
    
    wheel_distance = 25
    avoidance_distance = 20
    default_speed = 100
    motor_orientation_forward = False
    

    action_map = {
        **BaseRobot.action_map,
        "j": ETOWER_ACTION.BELT_FORWARD,
        "k": ETOWER_ACTION.BELT_BACKWARD,
        "l": ETOWER_ACTION.BELT_STOP
    }
 
    try:
        belt_motor = MoveSteering(OUTPUT_C,OUTPUT_D)
        
        
    except Exception as e:
        print("Error initializing motors", e)

    def __init__(self):
        super().__init__(self.wheel_distance, self.avoidance_distance, self.default_speed, self.action_map)

   

# Overwriting base methods from robot:

    def interpret_command_from_image_server(self, command, value, socket,speedPercentage):
        super().interpret_command_from_image_server(command, value, socket,speedPercentage)

        if command == "belt":
            self.belt_motor.on(0,SpeedPercent(speedPercentage))
        elif command == "beltstop":
           self.belt_motor.off()
        
    def move_forward(self):
        self.steering.on(0, SpeedPercent(-100))
    
    def move_backward(self):
        self.steering.on(0, SpeedPercent(100))
        
    # def turn_left(self, speed):
    #     self.mfdiff.turn_right(SpeedPercent(speed), self.turn_degrees, use_gyro=self.use_gyro)

    # def turn_right(self, speed):
    #     self.mfdiff.turn_left(SpeedPercent(speed), self.turn_degrees,use_gyro=self.use_gyro)
        


# Old run method with keypress
        
    def interpret_command_from_key(self, command):
        super().interpret_command_from_key(command)
        self.run_tower(command)

    def run_tower(self, command):
        if command in self.action_map:
            action = self.action_map[command]
            if action == EACTION.FORWARD:
                self.move_forward()
            elif action == EACTION.BACKWARD:
                self.move_backward()
            elif action == ETOWER_ACTION.BELT_FORWARD:
                self.belt_motor.on(SpeedPercent(100))
            elif action == ETOWER_ACTION.BELT_BACKWARD:
                self.belt_motor.on(SpeedPercent(-100))
            elif action == ETOWER_ACTION.BELT_STOP:
                self.belt_motor.off()
        else:
            print("Invalid command")

