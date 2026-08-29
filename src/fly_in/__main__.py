from .graphics import graphic_visualization
from .pathfinder import plan_cooperative_path, Cooperative_A_star
from .parser import parse_map_file
from .drone import init_drones
from .zone import ZoneType
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
    Cooperative_A_star(zone_dict, drones_lst)
    graphic_visualization(zone_dict, drones_lst)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("The program accept only one argument")
        print(f"You provided {len(sys.argv) - 1} arguments.")
        sys.exit(1)

    main(sys.argv[1])