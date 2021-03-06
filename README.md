# Elevator Scheduling Coding Challenge

The goal is to design and implement an Elevator Control System.

## Project Requirements and Build Instructions

- The project requires `python3`.
- It is recommended that you use a virtual environment setup the project there.
  An example when using `virtualenvwrapper` is given. 
  However, the project does not have any external libraries as dependencies right now, and one can skip this step.
  * `mkvirtualenv elevator --python=/path/to/python3`
  * `workon elevator`
- Clone the repository using `git clone https://github.com/mridul/elevator-scheduling.git`
- Change directory to the project directory. `cd elevator-scheduling`
- Run `make init` before first run.
- Run `make simulate` to run a simulation specified in `simulation.py`
- Run `make clean-pyc` to cleanup any `pyc` or `pyo` files.

## Project Layout
- The project is modelled like a simple python package `elevatorcontrol`
- There are two important classes `Elevator`, and `ElevatorControlSystem` 
- A simulation is already included in `simulation.py`. 
  It can be easily modified to simulate different number of elevators, and floor combinations

## Scheduling Algorithm
- The `ElevatorControlSystem` maintains a collection of `Elevator`s.
- When a new pickup request is received, the control system tries to find a target elevator to serve it.
  The requested pickup floor is added as a goal floor for the target elevator.
  The search for a target elevator is performed in the following manner:
  * Find the closest elevator to the pickup request floor, travelling in the direction requested:
  * If there is no elevator travelling in the current direction, return the closest elevator out of all elevators
- At each time step simulation, all elevators are simulated to visit their next floors. 
- Each `Elevator` has the following additional information apart from the `id` which helps it determine next steps:
  * It maintains a sorted list of goal floors, sorted in increasing order of floor value
  * It also maintains the intended direction it is going to travel in.
- With each time step, an `Elevator` visits the next floor using the following logic:
  * It finds the next floor to visit as the closest floor towards the direction it is already travelling.
  * If it was originally stationary, the elevator will visit the closest floor.
  * It deletes a floor from its goal floors list after visiting it.
- The scheduling and visiting algorithms are based off whatever limited experiences I've had with elevators in my life.
  They improve upon a first come first serve scheduler because:
  * The order in which and Elevator visits its goal floors tries to minimize time to serve all its goal floors in one direction first, followed by the other direction.
    This minimizes the time spent in an elevator to a large extent, but also maintains a sense of continuity in elevator travel - both of which should reduce most people's frustration.
  * The search for a target elevator to serve a pickup request leverages any elevators already travelling in the direction requested.
  * In tandem, both of these above work better than a first come first serve solution.
- A couple of possible future improvements:
  * When an elevator has been idle for a specific time, it could travel to a 'home' floor. One of the ways to choose a home floor could to go to a floor where lot of pickup requests have been seen historically.
  * Another factor we could consider is the capacity of an elevator. It doesn't make a lot of sense to send an already full elevator to pick more people up.
  