from .zone import Zone, ColorRGB
from .drone import Drone
import pygame


def graphic_visualization(
        zone_dict: dict[str, Zone],
        drones_lst: list[Drone]
) -> None:
    """
    Circle take: target surface, color, position, radius in px
    """
    pygame.init()
    pygame.display.set_caption("Fly-in Visualization")

    # Graphic scale and centralization 
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width = screen.get_width()
    height = screen.get_height()
    scale = 120
    min_x = min(zone.x for zone in zone_dict.values())
    min_y = min(zone.y for zone in zone_dict.values())
    max_x = max(zone.x for zone in zone_dict.values())
    max_y = max(zone.y for zone in zone_dict.values())
    map_center_x = (min_x + max_x) / 2
    map_center_y = (min_y + max_y) / 2
    screen_center_x = width / 2
    screen_center_y = height / 2
    offset_x = screen_center_x - (map_center_x * scale)
    offset_y = screen_center_y - (map_center_y * scale)

    # Graphic customization
    pygame.font.init()
    font_large = pygame.font.SysFont(None, 28)
    font_small = pygame.font.SysFont(None, 20)

    # Drone visualization
    drone_image = pygame.image.load("drone_icon.png")
    drone_icon = pygame.transform.scale(drone_image, (40, 40))

    current_turn = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_turn += 1
                elif event.key == pygame.K_LEFT:
                    current_turn -= 1
                elif event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((50, 150, 200))

        for zone in zone_dict.values():
            start_x = (zone.x * scale) + offset_x
            start_y = (zone.y * scale) + offset_y

            for connection in zone.connections:
                # zone_dict[connection.target] return all the target
                # -> the "name" of the zone, is the key in the zone_dict
                target_zone = zone_dict[connection.target]
                end_x = (target_zone.x * scale) + offset_x
                end_y = (target_zone.y * scale) + offset_y
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (start_x, start_y), (end_x, end_y),
                    connection.max_link_capacity
                )

                link_center_x = (start_x + end_x) / 2 
                link_center_y = (start_y + end_y) / 2
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (link_center_x, link_center_y),
                    scale / 10
                )
                capacity_text = str(connection.max_link_capacity)
                capacity_label = font_small.render(
                    capacity_text,
                    True,
                    (0, 0, 0),
                )
                screen.blit(
                    capacity_label,
                    (link_center_x - 4, link_center_y - 7)
                )

        # Zone visualization section
        for zone in zone_dict.values():
            center_x = (zone.x * scale) + offset_x
            center_y = (zone.y * scale) + offset_y
            if zone.color is not None:
                try:
                    circle_color = ColorRGB[zone.color.upper()].value
                except KeyError:
                    circle_color = ColorRGB.WHITE.value
            else:
                circle_color = ColorRGB.WHITE.value
            pygame.draw.circle(
                screen,
                circle_color,
                (center_x, center_y),
                scale / 3
            )

            # INFO label
            zone_type_letter = zone.zone_type.name[0]
            drone_text = str(zone.max_drones)
            zone_type_label = font_large.render(
                zone_type_letter,
                True,
                (0, 0, 0)
            )
            drone_label = font_small.render(drone_text, True, (60, 60, 60))
            screen.blit(zone_type_label, (center_x - 30, center_y - 15))
            screen.blit(drone_label, (center_x - 27, center_y + 3))

        # Swarm Effect (Scatter)
        for drone in drones_lst:
            # 1. Find the current zone
            drone_location = drone.current_zone
            for zone_name, turn in drone.path:
                if turn <= current_turn:
                    drone_location = zone_name
                else:
                    break
                    
            # 2. Calculate a deterministic micro-offset based on drone ID
            offset_x_drone = (drone.id * 7) % 25 - 12
            offset_y_drone = (drone.id * 5) % 25 - 12
            
            current_position = zone_dict[drone_location]
            x = (current_position.x * scale) + offset_x + offset_x_drone
            y = (current_position.y * scale) + offset_y + offset_y_drone
            
            # 3. Tint and draw the drone icon
            colored_icon = drone_icon.copy()
            colored_icon.fill(drone.drone_color, special_flags=pygame.BLEND_MULT)
            screen.blit(colored_icon, (x - 15, y - 25))

        # Instantly swaps the hidden "back canvas" with the visible window.
        # We draw everything in the background first, then show it all at
        # once.
        # This prevents the user from seeing partial updates and stops
        # flickering.
        pygame.display.flip()
    pygame.quit()
