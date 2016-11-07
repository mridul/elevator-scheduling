import itertools


class Elevator(object):
    new_elevator_id = itertools.count()

    def __init__(self, floor_num, goal_floor):
        self.id = next(Elevator.new_elevator_id)
        self.floor_num = floor_num
        self.goal_floor = goal_floor

    def state(self):
        return self.id, self.floor_num, self.goal_floor


class ElevatorControlSystem(object):
    def __init__(self, elevators):
        self.elevators = elevators

    def get_state(self):
        return [elevator.state for elevator in self.elevators]

    def update_state(self, elevator_id, floor_num, goal_floor):
        pass

    def pickup_request(self, pickup_from, direction):
        pass
