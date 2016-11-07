import itertools


class Elevator(object):
    new_elevator_id = itertools.count()

    def __init__(self, floor_num: int, goal_floors: list):
        self.id = next(Elevator.new_elevator_id)
        self.floor_num = floor_num
        self.goal_floors = goal_floors

    @property
    def state(self):
        return self.id, self.floor_num, self.goal_floors

    def _goto_next_floor(self):
        pass

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

    def get_state(self):
        return [elevator.state for id, elevator in self.elevator_id_map.items()]

    def update_state(self, elevator_id, floor_num, goal_floor):
        elevator = self._find_elevator(elevator_id)
        elevator.floor_num = floor_num
        elevator.goal_floor = goal_floor

    def pickup_request(self, pickup_from, direction):
        pass

    def step(self):
        for id, elevator in self.elevator_id_map:
            elevator.step()
