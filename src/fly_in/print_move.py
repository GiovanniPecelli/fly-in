from .zone import Zone, ZoneType
from .drone import Drone


def get_max_turn(drones_lst: list[Drone]) -> int:
    max_turn: int = 0
    for drone in drones_lst:
        if len(drone.path) > max_turn:
            max_turn = len(drone.path)
    return max_turn


def print_move(zone_dict: dict[str, Zone], drones_lst: list[Drone]) -> None:
    max_turn = get_max_turn(drones_lst)
    for t in range(1, max_turn + 1):
        moves_this_turn = []
        for drone in drones_lst:
            # if turn > drone.path
            # The t loop have a len > then the len(first_drone.path)
            if t >= len(drone.path):
                continue
            current_zone_name = drone.path[t][0]
            prev_zone_name = drone.path[t-1][0]
            if current_zone_name != prev_zone_name:
                current_zone = zone_dict[current_zone_name]
                if current_zone.zone_type == ZoneType.RESTRICTED:
                    connection_name = f"{prev_zone_name}-{current_zone_name}"
                    moves_this_turn.append(
                        f"D{drone.id}-{connection_name}"
                    )
                else:
                    moves_this_turn.append(
                        f"D{drone.id}-{current_zone_name}"
                    )
            elif current_zone_name == prev_zone_name:
                if t >= 2:
                    current_zone = zone_dict[current_zone_name]
                    if (
                        current_zone.zone_type == ZoneType.RESTRICTED
                        and drone.path[t-2][0] != current_zone_name
                    ):
                        moves_this_turn.append(
                            f"D{drone.id}-{current_zone_name}"
                        )
        if len(moves_this_turn) > 0:
            print(" ".join(moves_this_turn))
