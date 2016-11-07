import logging
import sys

from elevatorcontrol.core import Elevator, ElevatorControlSystem


def print_state(states):
    for state in states:
        print("Elevator {} is at {}, and has goals {}".format(state[0], state[1], state[2]))
    print()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # assuming 2 elevators, 10 floors numbered from 1 to 10
    elevators = [Elevator(1, []) for i in range(2)]
    ecs = ElevatorControlSystem(elevators)

    ecs.pickup_request(4, Elevator.DIRECTION_DOWN)
    print_state(ecs.get_state())
    ecs.step()

    elevators[0].add_goal_floor(1)
    print_state(ecs.get_state())

    ecs.pickup_request(3, Elevator.DIRECTION_DOWN)
    ecs.pickup_request(2, Elevator.DIRECTION_UP)
    print_state(ecs.get_state())
    ecs.step()
    print_state(ecs.get_state())

    ecs.step()
    print_state(ecs.get_state())
