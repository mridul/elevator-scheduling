import bisect
import itertools
import ipdb


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

    @property
    def direction_of_travel(self):
        # direction = 0 if no movement would happen at the next time step unit
        # direction > 0 if the elevator would go up at the next time step unit
        # direction < 0 otherwise
        next_floor = self._find_next_floor()
        if next_floor is None:
            return Elevator.DIRECTION_STILL

        if next_floor - self.floor_num > 0:
            return Elevator.DIRECTION_UP
        else:
            return Elevator.DIRECTION_DOWN

    def _find_next_floor(self):
        if len(self.goal_floors) == 0:
            return None

        return self.goal_floors.pop(0)

    def _goto_next_floor(self):
        next_floor = self._find_next_floor()
        if next_floor is not None:
            self.floor_num = next_floor

    def add_goal_floor(self, floor):
        bisect.insort_right(self.goal_floors, floor)

    def step(self):
        self._goto_next_floor()


class ElevatorControlSystem(object):
    elevator_id_map = {}

    def __init__(self, elevators):
        for elevator in elevators:
            self.elevator_id_map[elevator.id] = elevator

    def _find_elevator(self, id):
        if id in self.elevator_id_map:
            return self.elevator_id_map[id]
        else:
            raise Exception('Unknown Elevator')

    def _find_elevator_to_pickup_request(self, pickup_from, direction):
        elevators = []
        for id, elevator in self.elevator_id_map.items():
            elevators.append(
                (abs(pickup_from - elevator.floor_num), elevator.direction_of_travel, elevator)
            )

        elevators_in_direction = [e for e in elevators if e[1] == direction]
        if len(elevators_in_direction) == 0:
            return min(elevators, key=lambda e: e[0])[2]

        elevators_in_direction = sorted(elevators_in_direction, key=lambda e: e[0])
        return min(elevators_in_direction, key=lambda e: e[0])[2]

    def get_state(self):
        return [elevator.state for id, elevator in self.elevator_id_map.items()]

    def update_state(self, elevator_id, floor_num, goal_floor):
        elevator = self._find_elevator(elevator_id)
        elevator.floor_num = floor_num
        elevator.goal_floor = goal_floor

    def pickup_request(self, pickup_from, direction):
        # find the elevator closest to this pickup floor, travelling in the requested direction
        print("Incoming pickup request from floor {}, in direction {}".format(pickup_from, direction))
        target_elevator = self._find_elevator_to_pickup_request(pickup_from, direction)
        print("Elevator {} identified as target for pickup from {} in direction {}".format(
            target_elevator.id, pickup_from, direction))
        print("--Its current state is {}".format(target_elevator.state))
        target_elevator.add_goal_floor(pickup_from)
        print("--Its new state is {}".format(target_elevator.state))

    def step(self):
        print('----Moving a step ahead in time----')
        for id, elevator in self.elevator_id_map.items():
            elevator.step()
