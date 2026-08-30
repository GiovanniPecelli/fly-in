from .graphics import graphic_visualization
from .pathfinder import plan_cooperative_path, cooperative_a_star
from .parser import parse_map_file
from .print_move import print_move
from .drone import init_drones
from .zone import ZoneType
import time
import sys


def main(filepath: str) -> None:
    """
    Main entry point for the Fly-in simulation.
    
    Parses the map file, initializes drones, coordinates pathfinding 
    using a global reservation table, and starts the graphical visualization.

    Args:
        filepath (str): The path to the map file.
    """
    zone_dict, nb_drones = parse_map_file(filepath)
    drones_lst = init_drones(zone_dict, nb_drones)
    cooperative_a_star(zone_dict, drones_lst)
    print_move(zone_dict, drones_lst)
    # time.sleep: Permits the visualizzation of the terminal output
    time.sleep(5)
    graphic_visualization(zone_dict, drones_lst)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("The program accept only one argument")
        print(f"You provided {len(sys.argv) - 1} arguments.")
        sys.exit(1)

    main(sys.argv[1])