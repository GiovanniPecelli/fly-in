# Fly-in

A Python project to simulate a fleet of drones navigating a space-time graph using Cooperative A* pathfinding.

## Development Journey & Discoveries

Throughout the development of this project, we encountered and solved several fascinating algorithmic challenges:

### 1. From BFS to Cooperative A* (Space-Time Pathfinding)
Initially, we considered a standard Breadth-First Search (BFS) to find the shortest path. However, to handle drone collisions and varying zone traversal times (e.g., Restricted zones taking 2 turns), we implemented a **Time-Expanded Graph**. Every state in our pathfinder is not just a spatial coordinate `(Zone)`, but a temporal one `(Zone, Turn)`. We cross-reference these states with a global `reservation_table` to avoid traffic dynamically.

### 2. Priority Queue (Dijkstra/A*) & Penalty System
To handle `Priority` zones (which cost 1 turn but are preferred), we upgraded the queue to a Priority Queue using Python's `heapq`. We introduced a `penalty` system: 
- Moving to a Priority zone: `+0 penalty`
- Waiting in place: `+0 penalty`
- Moving to other zones: `+1 penalty`
This allows the algorithm to gracefully break ties between routes of identical time length, natively preferring the priority lanes without falling into greedy local traps.

### 3. The Python "Alphabet Bug"
We discovered a fascinating edge case in Python's `heapq` when comparing tuples like `(Turn, Penalty, ZoneName)`. When two paths tied on both Turn and Penalty, Python fell back to comparing the ZoneName alphabetically. This caused drones to occasionally prefer moving into a dead-end (e.g., "b_corridor") rather than waiting ("start_hub") simply because 'b' comes before 's'. We solved this by treating "waiting" as a 0-penalty action, ensuring the algorithm mathematically prefers staying still over unnecessary detours.

### 4. Emergent Behavior: "Dodging"
By observing the simulation, we noticed drones occasionally stepping into dead-ends and then returning to the main path. Rather than a bug, this is an advanced emergent behavior called **Sidestepping** or **Dodging**. When a main corridor is congested and the drone is forced to move (pushed by traffic behind it), it temporarily hides in a side-pocket to let another drone pass, preventing gridlock.

### 5. Graphics Evolution
We tested two different approaches for visualizing drone traffic in congested zones:
- **Grouped Counter (First iteration)**: Drones occupying the same zone were merged into a single neutral-colored icon displaying a numerical counter. This kept the UI clean but hid individual drone colors in crowded areas.
- **Scatter Swarm Effect (Current)**: Drones are rendered individually with their unique colors (assigned via `ColorRGB`) and a deterministic micro-offset based on their IDs. This creates a realistic "swarm" effect around nodes, allowing all individual drones to be seen simultaneously without Z-fighting.
