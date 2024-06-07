from water_mill_small import WaterMill
from tower import Tower
from prototype_enum import Prototypes


class RobotFactory:
    @staticmethod
    def create_robot(robot_type: Prototypes):
        if robot_type == Prototypes.WATER_MILL:
            return WaterMill()
        elif robot_type == Prototypes.TOWER:
            return Tower()
        else:
            print("Invalid robot type")
            return None

    print("Robot created")