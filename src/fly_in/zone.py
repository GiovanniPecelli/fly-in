from dataclasses import dataclass, field
from enum import Enum


class ZoneType(Enum):
    """
    Enum representing the different types of zones and their movement cost in
    turns. Blocked is "-1" just to rapresent an impossible action
    """
    NORMAL = 1
    PRIORITY = 1
    RESTRICTED = 2
    BLOCKED = -1
    START = 0
    END = 0


@dataclass
class Connection:
    """
    Represents a directional edge between two zones.
    Attributes:
        target (str): The name of the connected zone.
        max_link_capacity (int): Maximum drones that can traverse this
        connection simultaneously. Defaults to 1.
    """
    target: str
    max_link_capacity: int = field(default=1)


@dataclass
class Zone:
    """
    Represents a single zone (node) in the drone navigation map.
    Attributes:
        name (str): The unique identifier for the zone.
        x (int): The X coordinate on the grid.
        y (int): The Y coordinate on the grid.
        zone_type (ZoneType): The type of zone, which dictates movement cost.
        Defaults to NORMAL.
        color (str | None): Optional color for visual representation.
        max_drones (int): Maximum number of drones that can occupy this zone
        simultaneously. Defaults to 1.
        connections (list[Connection]): A list of outgoing connections to
        other zones.
    """
    name: str
    x: int
    y: int
    zone_type: ZoneType = field(default=ZoneType.NORMAL)
    color: str | None = None
    max_drones: int = field(default=1)
    connections: list[Connection] = field(default_factory=list)
