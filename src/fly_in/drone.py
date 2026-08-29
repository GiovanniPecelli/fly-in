from dataclasses import dataclass ,field
from .zone import Zone, ZoneType, ColorRGB
import random


@dataclass
class Drone:
    """
    Represents a single drone in the simulation.
    
    Attributes:
        id (int): The unique identifier of the drone.
        current_zone (str): The name of the zone where the drone is currently located.
    """
    id: int
    current_zone: str
    path: list = field(default_factory=list)
    drone_color: tuple = (255, 255, 255)

def init_drones(zone_dict: dict[str, Zone], nb_drones: int) -> list[Drone]:
    """
    Initializes a list of drones and places them in the starting zone.

    Args:
        zone_dict (dict[str, Zone]): Dictionary of parsed zones to find the start hub.
        nb_drones (int): Total number of drones to initialize.

    Returns:
        list[Drone]: A list containing the initialized Drone objects.
    """
    for zone in zone_dict.values():
        if zone.zone_type == ZoneType.START:
            start_zone_name = zone.name
            break

    color_lst = [color.value for color in ColorRGB]

    drones_lst = []
    for drone_id in range(1, nb_drones + 1):
        color_extracted = random.choice(color_lst)
        new_drone = Drone(
            id=drone_id,
            current_zone=start_zone_name,
            drone_color=color_extracted
        )
        drones_lst.append(new_drone)
    return drones_lst