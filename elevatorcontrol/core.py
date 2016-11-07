import bisect
import itertools
import ipdb
import logging


logger = logging.getLogger(__name__)


class Elevator(object):
    DIRECTION_STILL = 0
    DIRECTION_UP = +1
    DIRECTION_DOWN = -1
    new_elevator_id = itertools.count()

    def __init__(self, floor_num: int, goal_floors: list):
        self.id = next(Elevator.new_elevator_id)
        self.floor_num = floor_num
        self.goal_floors = goal_floors
        self.current_direction = Elevator.DIRECTION_STILL

    @property
    def state(self):
        return self.id, self.floor_num, self.goal_floors

    def _find_next_floor(self):
        if len(self.goal_floors) == 0:
            return None

        # if we're going down, find the closest floor less than current floor,
        # otherwise, find the closest floor above current floor.
        if self.current_direction == Elevator.DIRECTION_DOWN:
            index_closest_less_than_current = bisect.bisect_right(self.goal_floors, self.floor_num) - 1
            return self.goal_floors[index_closest_less_than_current]
        elif self.current_direction == Elevator.DIRECTION_UP:
            index_closest_greater_than_current = bisect.bisect_left(self.goal_floors, self.floor_num)
            return self.goal_floors[index_closest_greater_than_current]
        else:
            return min(self.goal_floors, key=lambda g: abs(g - self.floor_num))

    def _update_travel_direction(self):
        next_floor = self._find_next_floor()
        if next_floor is not None:
            if next_floor > self.floor_num:
                self.current_direction = Elevator.DIRECTION_UP
            else:
                self.current_direction = Elevator.DIRECTION_DOWN
        else:
            self.current_direction = Elevator.DIRECTION_STILL

    def _goto_next_floor(self):
        next_floor = self._find_next_floor()
        if next_floor is not None:
            logger.info("Elevator {} is going to floor {}, from floor {}".format(
                self.id, next_floor, self.floor_num))
            self.goal_floors.remove(next_floor)
            self._update_travel_direction()
            self.floor_num = next_floor
            logger.info("Elevator {} has reached floor {}".format(self.id, self.floor_num))

    def add_goal_floor(self, floor):
        bisect.insort_right(self.goal_floors, floor)
        logger.info("New goal floors for Elevator {} are {}".format(self.id, self.goal_floors))
        self._update_travel_direction()

    def step(self):
        self._goto_next_floor()


class ElevatorControlSystem(object):
    elevators_map = {}

    def __init__(self, elevators):
        for elevator in elevators:
            self.elevators_map[elevator.id] = elevator

    def _find_elevator(self, id):
        if id in self.elevators_map:
            return self.elevators_map[id]
        else:
            raise Exception('Unknown Elevator')

    def _find_elevator_to_pickup_request(self, pickup_from, direction):
        elevators = []
        for id, elevator in self.elevators_map.items():
            elevators.append(
                (abs(pickup_from - elevator.floor_num), elevator.current_direction, elevator)
            )

        elevators_in_direction = [e for e in elevators if e[1] == direction]
        if len(elevators_in_direction) == 0:
            return min(elevators, key=lambda e: e[0])[2]

        elevators_in_direction = sorted(elevators_in_direction, key=lambda e: e[0])
        return min(elevators_in_direction, key=lambda e: e[0])[2]

    def get_state(self):
        return [elevator.state for id, elevator in self.elevators_map.items()]

    def update_state(self, elevator_id, floor_num, goal_floor):
        elevator = self._find_elevator(elevator_id)
        elevator.floor_num = floor_num
        elevator.goal_floor = goal_floor

    def pickup_request(self, pickup_from, direction):
        # find the elevator closest to this pickup floor, travelling in the requested direction
        logger.info("Incoming pickup request from floor {}, in direction {}".format(pickup_from, direction))
        target_elevator = self._find_elevator_to_pickup_request(pickup_from, direction)
        logger.info("Elevator {} identified as target for pickup from {} in direction {}".format(
            target_elevator.id, pickup_from, direction))
        logger.info("--Its current state is {}".format(target_elevator.state))
        target_elevator.add_goal_floor(pickup_from)
        logger.info("--Its new state is {}".format(target_elevator.state))

    def step(self):
        logger.info('----Moving a step ahead in time----')
        for id, elevator in self.elevators_map.items():
            elevator.step()
