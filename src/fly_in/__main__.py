from .print_move import print_move, get_max_turn
from .graphics import graphic_visualization
from .pathfinder import cooperative_a_star
from .parser import parse_map_file
from .drone import init_drones
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
    max_turn = get_max_turn(drones_lst) - 1
    print_move(zone_dict, drones_lst)
    print(f"\nTotal turn = {max_turn}")
    # time.sleep: Permits the see the drones movements output
    time.sleep(5)
    graphic_visualization(zone_dict, drones_lst)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("The program accept only one argument")
        print(f"You provided {len(sys.argv) - 1} arguments.")
        sys.exit(1)

    main(sys.argv[1])
