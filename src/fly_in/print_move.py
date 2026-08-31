from .zone import Zone, ZoneType
from .drone import Drone


def get_max_turn(drones_lst: list[Drone]) -> int:
    """Return the maximum number of turns required by all drones.

    Iterate over the list of drones and return the maximum length of the
    `path` attribute found, which represents the number of steps (turns)
    for each drone.

    Parameters
    ----------
    drones_lst : list[Drone]
        List of `Drone` objects to read the `path` attribute from.

    Returns
    -------
    int
        Maximum number of turns (maximum length of the `path` lists).
    """
    max_turn: int = 0
    for drone in drones_lst:
        if len(drone.path) > max_turn:
            max_turn = len(drone.path)
    return max_turn


def print_move(zone_dict: dict[str, Zone], drones_lst: list[Drone]) -> None:
    """Print drone moves per turn to stdout.

    For each turn the function collects movements performed by drones and
    prints them as a single space-separated line. Output formats are:
    - `D{id}-{zone}` for a drone that is located (or stays) in a
        non-restricted zone;
    - `D{id}-{from}-{to}` for a drone that traverses a restricted zone
        (the connection is shown as `prev-current`).

    Parameters
    ----------
    zone_dict : dict[str, Zone]
            Dictionary of zones indexed by name.
    drones_lst : list[Drone]
            List of `Drone` objects from which to read movements.

    Returns
    -------
    None
    """
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
