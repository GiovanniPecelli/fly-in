*This project has been created as part of the 42 curriculum by imgio.*

# Fly-in

## Description
**Fly-in** is an autonomous drone routing simulation built in Python. The primary goal of the project is to efficiently navigate a fleet of drones from a central starting base to a target ending location across a network of interconnected zones. The challenge lies in minimizing the total number of simulation turns required for all drones to arrive while strictly adhering to complex zone capacities, variable movement costs, and collision-avoidance rules.

## Instructions
This project requires Python 3.10 or later and is fully type-safe.

### Installation
To install project dependencies (using `uv`):
```bash
make install
```

### Execution
To run the simulation with a specific map file:
```bash
make run MAP=maps/maps/easy/01_linear_path.txt
```
To run the project in debug mode:
```bash
make debug MAP=maps/maps/easy/01_linear_path.txt
```

### Code Quality & Cleanup
To run the linters (`flake8` and `mypy`) to ensure type safety and PEP8 compliance:
```bash
make lint
make lint-strict
```
To clean temporary files and caches:
```bash
make clean
```

## Algorithm Choices & Implementation Strategy
To handle drone collisions and varying zone traversal times (e.g., Restricted zones taking 2 turns), we avoided standard Breadth-First Search (BFS) and implemented **Cooperative A\* (Space-Time Pathfinding)** over a Time-Expanded Graph.
- **State Representation**: Every state in the pathfinder is a temporal-spatial coordinate `(Zone, Turn)`.
- **Traffic Avoidance**: We cross-reference future states with a global `reservation_table`. If a destination zone is full at a specific future turn, the move is discarded.
- **Turn Logging**: For `restricted` zones (which cost 2 turns), the algorithm explicitly reserves the intermediate turn (representing the drone in transit over the connection) and the arrival turn.
- **Priority Queue**: We use Python's `heapq` with a custom `penalty` system (+0 for priority zones and waiting, +1 for normal moves). This natively guides drones toward priority lanes and encourages them to wait patiently when congested, avoiding greedy local traps.

## Visual Representation
The project features a dual-visualization system to enhance user experience:
1. **Terminal Output**: Immediately outputs the step-by-step movements of the drones in compliance with the required formatting `D<ID>-<zone>` (or `D<ID>-<connection>` when in transit).
2. **Graphical Interface (Pygame)**: Renders the graph network visually. We implemented a **Scatter Swarm Effect**, where drones are drawn individually with unique colors and deterministic micro-offsets based on their IDs. When drones enter a multi-turn connection toward a restricted zone, they are visually rendered midway along the connection segment to accurately represent their "in-flight" status.

## Example Input and Expected Output

**Input Map (`01_linear_path.txt`):**
```text
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

**Expected Terminal Output:**
```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

## Resources
- **Cooperative A\***: Inspired by academic papers on Space-Time A* for multi-agent pathfinding (Silver, 2005).
- **Python `heapq` documentation**: Used for implementing the priority queue in A*.
- **AI Usage**: Artificial Intelligence was used as a pair-programming assistant to brainstorm pathfinding edge-cases (specifically handling the mathematical insertion of intermediate turns for restricted zones), to troubleshoot Pygame indexing crashes related to backwards time-travel, and to assist in formatting the terminal output parser cleanly.
