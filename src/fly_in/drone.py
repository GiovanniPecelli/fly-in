from dataclasses import dataclass
from .zone import Zone, ZoneType


@dataclass
class Drone:
    id: int
    current_zone: str

def init_drones(zone_dict: dict[str, Zone], nb_drones: int) -> list[Drone]:
    for zone in zone_dict.values():
        if zone.zone_type == ZoneType.START:
            start_zone_name = zone.name
            break
    drones_lst = []
    for drone_id in range(1, nb_drones + 1):
        new_drone = Drone(id=drone_id, current_zone=start_zone_name)
        drones_lst.append(new_drone)
    return drones_lst