from elevatorcontrol.core import Elevator, ElevatorControlSystem


if __name__ == '__main__':
    # assuming 3 elevators, 10 floors numbered from 1 to 10
    elevators = [Elevator(1, []) for i in range(3)]
    ecs = ElevatorControlSystem(elevators)
    ecs.pickup_request(4, Elevator.DIRECTION_DOWN)

    print(ecs.get_state())
