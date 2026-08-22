#1. Phase 1 (Terminal Output): Focus entirely on building the parser, the graph logic, and the pathfinding algorithm. Use
#  standard print() statements (maybe with some ANSI colors) to verify that your drones are moving correctly turn-by-turn  
#  without conflicts. This makes debugging much faster because you aren't fighting GUI bugs at the same time as algorithm  
#  bugs.                                                                                                                   
#2. Phase 2 (Pygame): Once the core engine works and outputs the correct text log (e.g., D1-roof1 D2-corridorA), you can 
#  plug pygame into your engine to read those states and animate the drones moving between the (x, y) coordinates smoothly.