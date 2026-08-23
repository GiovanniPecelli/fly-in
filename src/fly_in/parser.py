from .zone import Zone, ZoneType, Connection


def extract_zone(clean_line: str) -> Zone:
    """
    Parses a single line defining a zone and returns a Zone object.
    
    Args:
        clean_line (str): The raw line from the map file starting with a zone prefix.
        
    Returns:
        Zone: The constructed Zone object with parsed metadata.
    """
    prefix, data = clean_line.split(":", 1)
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
    name = lst_data[0]
    x = int(lst_data[1])
    y = int(lst_data[2])

    # Object "Zone" creation
    new_zone = Zone(name=name, x=x, y=y)

    if prefix.strip() == "start_hub":
        new_zone.zone_type = ZoneType.START
    elif prefix.strip() == "end_hub":
        new_zone.zone_type = ZoneType.END

    if "zone" in metadata_dict:
        new_zone.zone_type = ZoneType[metadata_dict["zone"].upper()]

    if "color" in metadata_dict:
        new_zone.color = metadata_dict["color"]

    if "max_drones" in metadata_dict:
        new_zone.max_drones = int(metadata_dict["max_drones"])

    return new_zone


def extract_connection(clean_line: str, zone_dict: dict[str, Zone]) -> None:
    """
    Parses a connection line and updates the respective Zone objects in the dictionary.
    
    Args:
        clean_line (str): The raw line from the map file starting with 'connection:'.
        zone_dict (dict[str, Zone]): The dictionary containing all created zones.
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
    name_A = names[0].strip()
    name_B = names[1].strip()

    if "max_link_capacity" in metadata_dict:
        capacity = int(metadata_dict["max_link_capacity"])
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
        tuple[dict[str, Zone], int]: A tuple containing the dictionary of parsed zones 
                                     and the total number of drones.
    """
    zone_dict = {}
    nb_drones = 0

    with open(filepath, "r") as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            elif clean_line.startswith("nb_drones"):
                #TODO maybe need a try - except
                nb_drones = int(line.split(":", 1)[1].strip())
            elif (clean_line.startswith("start_hub")
                or clean_line.startswith("end_hub")
                or clean_line.startswith("hub")
            ):
                new_zone = extract_zone(clean_line)
                zone_dict[new_zone.name] = new_zone
            elif clean_line.startswith("connection"):
                extract_connection(clean_line, zone_dict)
                
    return zone_dict, nb_drones