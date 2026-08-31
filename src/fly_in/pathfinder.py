from .zone import Zone, ZoneType
from .drone import Drone
import heapq


def plan_cooperative_path(
    zone_dict: dict[str, Zone],
    start_name: str,
    end_name: str,
    reservation_table: dict[str, dict[int, int]]
) -> list[tuple[str, int]]:
    """
    Finds the shortest collision-free path for a drone using Cooperative A*
    (Space-Time Pathfinding).

    Unlike a standard pathfinding algorithm that only searches through spatial
    nodes (X, Y), this algorithm explores a Time-Expanded Graph where each
    state is a combination of (Zone, Turn).

    Algorithm Behavior:
    1.  It evaluates moving to adjacent zones or waiting in the current zone.
    2.  It calculates the temporal cost of the move
        (e.g., restricted zones take 2 turns).
    3.  It cross-references future states with a global `reservation_table`.
        If a destination zone has reached its `max_drones` capacity at that
        specific future turn, the move is discarded (traffic avoidance).
    4.  Upon reaching the target zone, it backtracks through the `came_from`
        dictionary to reconstruct the optimal time-aware path.

    Args:
        zone_dict (dict[str, Zone]): A dictionary of all available zones
        in the map.
        start_name (str): The name of the starting zone.
        end_name (str): The name of the target zone.
        reservation_table (dict): A shared registry tracking drone occupancy
        per zone per turn (format: {zone_name: {turn: count}}).

    Returns:
        list[tuple[str, int]]: The calculated path as a chronological
        sequence of (Zone Name, Turn) states, or an empty list if no
        valid path is found.
    """

    # initialization queue(turn, current_penality, movement, zone_name)
    queue: list[tuple[int, int, int, str]] = [(0, 0, 0, start_name)]
    came_from: dict[
        tuple[str, int], tuple[str, int] | None
        ] = {(start_name, 0): None}

    while len(queue) > 0:
        (
            current_turn,
            current_penality,
            movement,
            current_name
        ) = heapq.heappop(queue)
        if current_name == end_name:
            break
        current_zone = zone_dict[current_name]

        possible_destinations = [current_name]
        for connection in current_zone.connections:
            possible_destinations.append(connection.target)

        for next_name in possible_destinations:
            next_zone = zone_dict[next_name]
            if (
                next_name != current_name
                and next_zone.zone_type == ZoneType.RESTRICTED
            ):
                turn_cost = 2
            else:
                turn_cost = 1
            next_turn = current_turn + turn_cost

            if next_zone.zone_type == ZoneType.BLOCKED:
                continue

            # CHECK TRAFFIC: read the reservation_table in the next_turn
            # We use chained .get() to safely read without raising a KeyError.
            # use of "reservation_table["roof3"]"
            # raise an err. if the parameters are not available
            # .get(..., "default_value") if ... not found -> def.val
            traffic_clear = True
            link_capability = 1
            for c in current_zone.connections:
                if c.target != next_name:
                    continue
                else:
                    link_capability = c.max_link_capacity
            link = f"{current_name}-{next_name}"
            for t in range(current_turn + 1, next_turn + 1):
                if (
                    reservation_table.get(link, {}).get(t, 0)
                    >= link_capability
                ):
                    traffic_clear = False
                    break
                if (
                    reservation_table.get(next_name, {}).get(t, 0)
                    >= next_zone.max_drones
                ):
                    traffic_clear = False
                    break
            if not traffic_clear:
                continue

            if next_zone.zone_type == ZoneType.PRIORITY:
                next_penality = current_penality + 0
            else:
                next_penality = current_penality + 1
            movement = 0 if next_name == current_name else 1
            # es: how data are in "came_from" variable
            # {
            #    ("start", 0): None,
            #    ("corridorA", 1): ("start", 0)
            #    ("corridorA", 2): ("corridorA", 1)
            # }
            # the real next option after the traffic and zone_type check
            if (next_name, next_turn) not in came_from:
                # heappop() extract the element on the top of the tree
                heapq.heappush(queue, (
                    next_turn, next_penality, movement, next_name
                ))

                # ADD intermediate_turn in come_from if is ZoneType.RESTRICTED
                if turn_cost == 2:
                    intermediate_turn = current_turn + 1
                    came_from[(next_name, next_turn)] = (
                        next_name, intermediate_turn)
                    if (next_name, intermediate_turn) not in came_from:
                        came_from[(next_name, intermediate_turn)] = (
                            current_name, current_turn)
                else:
                    came_from[(next_name, next_turn)] = (
                        current_name, current_turn)

    # if the path for the drone have not end -> return []
    if current_name != end_name:
        return []

    # state is the focus point (starting from the end)
    state: tuple[str, int] | None = (current_name, current_turn)

    # add -> add state to the path list
    # ask -> the matched value in come_from
    # (come_from struct from line 45 to 50)
    path = []
    while state is not None:
        path.append(state)
        state = came_from[state]
    path.reverse()

    return path


def cooperative_a_star(
        zone_dict: dict[str, Zone],
        drones_lst: list[Drone]
) -> None:
    for zone in zone_dict.values():
        if zone.zone_type == ZoneType.END:
            end_zone_name = zone.name
            break
    # reservation_table is a dict[
    #     zone_name | link_key: dict[turn: reservation
    # ]
    reservation_table: dict[
        str, dict[int, int]
        ] = {}

    for drone in drones_lst:
        path = plan_cooperative_path(
            zone_dict,
            drone.current_zone,
            end_zone_name,
            reservation_table
        )
        # path: (is a list[tuple[
        # ("start", turn), ("corridorA", turn), ("goal", turn)
        # ]])
        drone.path = path
        for zone_name, turn in path:
            if zone_name not in reservation_table:
                reservation_table[zone_name] = {}
            if turn not in reservation_table[zone_name]:
                reservation_table[zone_name][turn] = 0
            # UPDATE -> reservation_table
            reservation_table[zone_name][turn] += 1
        for i in range(len(path) - 1):
            depar_name, depar_turn = path[i]
            dest_name, dest_turn = path[i + 1]
            if depar_name == dest_name:
                continue
            link_key = f"{depar_name}-{dest_name}"
            for t in range(depar_turn + 1, dest_turn + 1):
                reservation_table.setdefault(link_key, {})[t] = (
                    reservation_table.get(link_key, {}).get(t, 0) + 1
                )
    print(reservation_table)
