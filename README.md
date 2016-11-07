# Elevator Scheduling Coding Challenge

The goal is to design and implement an Elevator Control System.

## Project Requirements and Build Instructions

- The project requires `python3`.
- It is recommended that you use a virtual environment setup the project there.
  An example when using `virtualenvwrapper` is given. 
  However, the project does not have any external libraries as dependencies right now, and one can skip this step.
  * `mkvirtualenv elevator --python=/path/to/python3`
  * `workon elevator`
- Run `make init` before first run.
- Run `make simulate` to run a simulation specified in `simulation.py`
- Run `make clean-pyc` to cleanup any `pyc or pyo` files.

## Project Layout
- The project is modelled like a simple python package `elevatorcontrol`
- There are two important classes `Elevator`, and `ElevatorControlSystem` 
- A simulation is already included in `simulation.py`. 
  It can be easily modified to simulate different number of elevators, and floor combinations

## Scheduling Algorithm
- Each `Elevator` maintains its id, current floor number, goal floors, and the direction it intends to travel in
- The `ElevatorControlSystem` maintains a collection of `Elevator`s.
- When a new pickup request is received, the control system tries to find a target elevator to serve it.
  The search for a target elevator is performed in the following manner:
  * 



