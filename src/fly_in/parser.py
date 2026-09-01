from .zone import Zone, ZoneType, Connection


def extract_zone(clean_line: str) -> Zone:
    """
    Parses a single line defining a zone and returns a Zone object.
    Args:
        clean_line (str): The raw line from the map file starting
        with a zone prefix.
    Returns:
        Zone: The constructed Zone object with parsed metadata.
    """
    try:
        prefix, data = clean_line.split(":", 1)
    except ValueError:
        raise ValueError(
            "Invalid line format (line need a 'prefix: data' format)"
        )
    metadata_dict = {}

    if "[" in data:
        basic_data, metadata_string = data.split("[", 1)
        metadata_string = metadata_string.replace("]", "").strip()
        for item in metadata_string.split():
            key, value = item.split("=")
            metadata_dict[key] = value

    else:
        basic_data = data

    lst_data = basic_data.split()
    name = str(lst_data[0])
    try:
        x = int(lst_data[1])
        y = int(lst_data[2])
    except ValueError:
        raise ValueError(
            "Invalid value for coordinates "
            f"in line: {clean_line}.\n"
            "Coordinates must be integers"
        )

    # Object "Zone" creation
    new_zone = Zone(name=name, x=x, y=y)

    if prefix.strip() == "start_hub":
        new_zone.zone_type = ZoneType.START
    elif prefix.strip() == "end_hub":
        new_zone.zone_type = ZoneType.END

    if "zone" in metadata_dict:
        zone_type = metadata_dict["zone"].upper()
        if zone_type in ZoneType.__members__:
            new_zone.zone_type = ZoneType[zone_type]
        else:
            raise ValueError(
                f"Invalid zone type '{metadata_dict['zone']}' "
                f"in line: '{clean_line}'."
            )

    if "color" in metadata_dict:
        new_zone.color = metadata_dict["color"]

    if "max_drones" in metadata_dict:
        new_zone.max_drones = int(metadata_dict["max_drones"])

    if new_zone.zone_type in (ZoneType.START, ZoneType.END):
        new_zone.max_drones = float('inf')

    return new_zone


def extract_connection(clean_line: str, zone_dict: dict[str, Zone]) -> None:
    """
    Parses a connection line and updates the respective Zone objects
    in the dictionary.
    Args:
        clean_line (str): The raw line from the map file starting with
        'connection:'.
        zone_dict (dict[str, Zone]): The dictionary containing all
        created zones.
    """
    data = clean_line.split(":", 1)[1].strip()
    metadata_dict = {}

    if "[" in data:
        basic_data, metadata_string = data.split("[", 1)
        metadata_string = metadata_string.replace("]", "").strip()
        for item in metadata_string.split():
            key, value = item.split("=")
            metadata_dict[key] = value

    else:
        basic_data = data

    names = basic_data.split("-")
    if len(names) != 2:
        raise ValueError(
            f"Invalid connection format in line: '{clean_line}'. "
            "Expected 'connection: zoneA-zoneB'."
        )
    name_A = names[0].strip()
    if name_A not in zone_dict:
        raise ValueError(
            f"Unknown zone '{name_A}' in connection: '{clean_line}'."
        )
    name_B = names[1].strip()
    if name_B not in zone_dict:
        raise ValueError(
            f"Unknown zone '{name_B}' in connection: '{clean_line}'."
        )

    for conn in zone_dict[name_A].connections:
        if conn.target == name_B:
            raise ValueError(
                f"Duplicate connection between "
                f"'{name_A}' and '{name_B}'."
            )

    if "max_link_capacity" in metadata_dict:
        try:
            capacity = int(metadata_dict["max_link_capacity"])
        except ValueError:
            raise ValueError(
                "Invalid max_link_capacity "
                f"'{metadata_dict['max_link_capacity']}' "
                f"in line '{clean_line}'."
            )
        if capacity <= 0:
            raise ValueError(
                "max_link_capacity must be a positive integer.\n"
                f"Error in line '{clean_line}'."
            )
        conn_to_B = Connection(target=name_B, max_link_capacity=capacity)
        conn_to_A = Connection(target=name_A, max_link_capacity=capacity)

    else:
        conn_to_B = Connection(target=name_B)
        conn_to_A = Connection(target=name_A)

    zone_dict[name_A].connections.append(conn_to_B)
    zone_dict[name_B].connections.append(conn_to_A)


def parse_map_file(filepath: str) -> tuple[dict[str, Zone], int]:
    """
    Parses a complete drone map file and builds the graph of zones.
    Args:
        filepath (str): The path to the .txt map file.
    Returns:
        tuple[dict[str, Zone], int]: A tuple containing the dictionary of
        parsed zones and the total number of drones.
    """
    zone_dict = {}
    nb_drones = None

    with open(filepath, "r") as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            elif clean_line.startswith("nb_drones"):
                try:
                    nb_drones = int(line.split(":", 1)[1].strip())
                except ValueError:
                    raise ValueError(
                        f"Error in line '{clean_line}'\n"
                        "Number of drones is invalid, "
                        "must be an integers"
                    )
                if nb_drones <= 0:
                    raise ValueError(
                        f"Error in line '{clean_line}'\n"
                        "Invalid value: number of drones must be positive"
                    )
            elif (
                clean_line.startswith("start_hub")
                or clean_line.startswith("end_hub")
                or clean_line.startswith("hub")
            ):
                new_zone = extract_zone(clean_line)
                if new_zone.name in zone_dict:
                    raise ValueError(
                        f"Duplicate zone name '{new_zone.name}' "
                        f"in line '{clean_line}'"
                    )
                zone_dict[new_zone.name] = new_zone
            elif clean_line.startswith("connection"):
                extract_connection(clean_line, zone_dict)
    if nb_drones is None:
        raise ValueError("Missing nb_drones definition")

    # Checks whether at least one element in an iterable is True
    # IF there is at least one element return True
    has_start = sum(
        zone.zone_type == ZoneType.START
        for zone in zone_dict.values()
    )
    has_end = sum(
        zone.zone_type == ZoneType.END
        for zone in zone_dict.values()
    )
    if has_start != 1:
        raise ValueError("Map must contain exactly one start_hub")
    if has_end != 1:
        raise ValueError("Map must contain exactly one end_hub")

    return zone_dict, nb_drones
