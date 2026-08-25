from .zone import Zone, ZoneType, Connection


def get_shortest_path(
        zone_dict: dict[str, Zone],
        start_name: str,
        end_name: str,
) -> list[str]:
    start_zone = zone_dict[start_name]
    end_zone = zone_dict[end_name]
    queue = [start_name]
    came_from = {start_name: None}
    
    while len(queue) > 0:
        current_name = queue.pop(0)
        if current_name == end_name:
            break
        current_zone = zone_dict[current_name]
        for connection in current_zone.connections:
            neighbor_name = connection.target
            neighbor_zone = zone_dict[neighbor_name]
            if (neighbor_zone.zone_type != ZoneType.BLOCKED 
                and neighbor_name not in came_from
            ):
                queue.append(neighbor_name)
                came_from[neighbor_name] = current_name