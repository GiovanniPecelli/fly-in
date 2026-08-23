from .graphics import start_visualization
from .parser import parse_map_file
import sys


def main(filepath: str) -> None:
    zone_dict, nb_drones = parse_map_file(filepath)
    start_visualization(zone_dict)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("The program accept only one argument")
        print(f"You provided {len(sys.argv) - 1} arguments.")
        sys.exit(1)

    main(sys.argv[1])