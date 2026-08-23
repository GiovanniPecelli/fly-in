from .zone import Zone
import pygame


#TODO - enum for the zone color


def start_visualization(zone_dict: dict[str, Zone]) -> None:
    """
    Circle take: target surface, color, position, radius in px
    """
    pygame.init()

    width = 800
    height = 600
    pygame.display.set_caption("Fly-in Visualization")
    screen = pygame.display.set_mode((width, height))
    scale = 60
    offset_x = 50
    offset_y = 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                    3
                )

                for zone in zone_dict.values():
                    center_x = (zone.x * scale) + offset_x
                    center_y = (zone.y * scale) + offset_y
                    #TODO - customize the zone color
                    pygame.draw.circle(
                        screen,
                        (255, 255, 255),
                        (center_x, center_y),
                        20
                    )
        # Instantly swaps the hidden "back canvas" with the visible window.
        # We draw everything in the background first, then show it all at
        # once.
        # This prevents the user from seeing partial updates and stops
        # flickering.
        pygame.display.flip()
    pygame.quit()
