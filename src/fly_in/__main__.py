from .graphics import graphic_visualization
from .parser import parse_map_file
from .drone import init_drones
import sys


def main(filepath: str) -> None:
    zone_dict, nb_drones = parse_map_file(filepath)
    drones_lst = init_drones(zone_dict, nb_drones)
    graphic_visualization(zone_dict, drones_lst)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("The program accept only one argument")
        print(f"You provided {len(sys.argv) - 1} arguments.")
        sys.exit(1)

    main(sys.argv[1])