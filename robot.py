from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveDifferential, MoveSteering
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
from ev3dev2.wheel import EV3Tire
from enum import Enum
from ev3dev2.sound import Sound
from time import sleep


class EACTION(Enum):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    STOP = "STOP"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class BaseRobot:

    action_map = {
        'w': EACTION.FORWARD,
        's': EACTION.BACKWARD,
        'a': EACTION.LEFT,
        'd': EACTION.RIGHT,
        'x': EACTION.STOP
    }
    
    STUD_MM = 8
    wheel_distance = 0
    default_speed = 250
    mfdiff = None 
    steering = None
    dist_sensor = None
    avoidance_distance = 15
    turn_degrees = 90
    # True for normal configuration, False for inverted configuration
    motor_orientation_forward = True
    use_gyro = False
    gyro_sensor = None
   

    def __init__(self, wheel_distance, avoidance_distance, default_speed, action_map) :
        self.wheel_distance = wheel_distance
        self.avoidance_distance = avoidance_distance
        self.default_speed = default_speed
        self.update_action_map(action_map)
        
        self.sound = Sound()
        
        try:
            print("wheel distance", self.wheel_distance)
            self.mfdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, float(self.STUD_MM) * float(self.wheel_distance))
            self.steering = MoveSteering(OUTPUT_A, OUTPUT_B)
            
        except Exception as e:
            print("Error initializing Motors", e)
            
        try:
            #self.dist_sensor = UltrasonicSensor()
            self.mfdiff.gyro = GyroSensor()
        except Exception as e:
            print("Error initializing Sensors", e)
        
        if self.mfdiff.gyro:
            self.mfdiff.gyro.calibrate()
            self.use_gyro = True
           #self.gyro_sensor = GyroSensor()
            print("Gyro calibrated")
        else:
            print("Gyro not calibrated")
        
        if self.dist_sensor:
            print("Distance sensor initialized")

    def move_forward(self):
        self.steering.on(0, SpeedPercent(100))

    def move_backward(self):
        self.steering.on(0, SpeedPercent(-100))

    def turn_left(self, speed,degrees=90):
        self.mfdiff.turn_left(SpeedPercent(speed), degrees, use_gyro=self.use_gyro)

    def turn_right(self, speed,degrees=90):
        self.mfdiff.turn_right(SpeedPercent(speed), degrees,use_gyro=self.use_gyro)

    def stop(self):
        self.mfdiff.stop()

    def speak(self, message):
        self.sound.speak(message)
        print(message)
        
    def update_action_map(self, new_action_map):
        self.action_map = {**self.action_map, **new_action_map}
    
    
    def interpret_command_from_key(self, command):
        if self.action_map:
            if command in self.action_map:
                action = self.action_map[command]
                if action == EACTION.LEFT:
                    self.turn_left(speed=70)
                elif action == EACTION.RIGHT:
                    self.turn_right(speed=70)
                elif action == EACTION.STOP:
                    self.stop()
        else:
            print("Invalid command")
            
    def get_information(self) -> None:
        print("Robot information")
        print("Max speed", self.steering.max_speed)
        print("Min speed", self.steering.is_running)
        if self.use_gyro: print("Gyro",self.gyro_sensor.angle_and_rate)
        
    def move_from_image_server(self, distance_mm :int, socket, speedPercentage: int) -> None:
        self.mfdiff.on_for_distance(speed = SpeedPercent(speedPercentage), distance_mm = distance_mm,brake=False,block=False)
        print("Moving", distance_mm, "speed", speedPercentage)
        #self.get_information()
        #self.mfdiff.wait_until_not_moving()
        socket.sendall("done".encode())
        
    
    def move_corrected(self, steering: int, speedPercentage: int) -> None:
        print("Moving corrected", steering, "speed", speedPercentage)
        self.steering.on(steering, SpeedPercent(speedPercentage))

        
    
    def turn_from_image_server(self, degrees :float, socket,speedPercentage: int) -> None:
        if degrees is None or degrees == 0 or degrees == 360:
            socket.sendall("done".encode())
            return

        self.mfdiff.turn_degrees(SpeedPercent(speedPercentage), degrees, use_gyro=False,brake=True,block=False)
        print("Turning", degrees, "speed", speedPercentage)

        #self.get_information()
        #self.mfdiff.wait_until_not_moving()
        socket.sendall("done".encode())


    
    def interpret_command_from_image_server(self, command:str, value, socket,speedPercentage = 100):
        if command == "move":
            if value:
                self.move_from_image_server(distance_mm=value, socket=socket, speedPercentage=speedPercentage)
            else:
                print("Invalid distance")
        elif command == "turn":
                self.turn_from_image_server(degrees=value, socket=socket,speedPercentage=speedPercentage)
        elif command == "move-corrected":
                self.move_corrected(steering=value, speedPercentage=speedPercentage)
        elif command == "test-drive":
            self.test_drive()
        elif command == "stop":
            self.stop()
        else:
            print("Invalid command")
        
    
    
    def test_drive(self):
        print("Wheel distance", self.wheel_distance)
        self.mfdiff.on_arc_left(SpeedPercent(50), 128.0, 400)
        # Enable odometry
        self.mfdiff.odometry_start()

        # Use odometry to drive to specific coordinates
        #self.mfdiff.on_to_coordinates(SpeedPercent(-40), 300, 300)

        # Use odometry to go back to where we started
        #self.mfdiff.on_to_coordinates(SpeedPercent(-40), 0, 0)

        # Use odometry to rotate in place to 90 degrees
        #self.mfdiff.turn_to_angle(SpeedPercent(-40), 90)

        # Disable odometry
        self.mfdiff.odometry_stop()
    
    def avoid_obstacle(self):
        if self.dist_sensor:    
            if self.dist_sensor.distance_centimeters < self.avoidance_distance:
                    self.stop()
                    print("Obstacle detected")
                    sleep(1)
                    self.turn_left(speed=70)
                    self.move_forward()
                    
    def robot_information(self):
        print("Robot information")
        print("Max speed", self.steering.max_speed)
        print("Min speed", self.steering.is_running)