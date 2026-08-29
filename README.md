# Fly-in

A Python project to simulate a fleet of drones navigating a space-time graph using Cooperative A* pathfinding.

## Graphics Evolution
Throughout the development, we tested two different approaches for visualizing drone traffic in congested zones:
1. **Grouped Counter (First iteration)**: Drones occupying the same zone were merged into a single neutral-colored icon displaying a numerical counter. This kept the UI clean but hid individual drone colors in crowded areas.
2. **Scatter Swarm Effect (Current)**: Drones are rendered individually with their unique colors and a deterministic micro-offset based on their IDs. This creates a realistic "swarm" effect around nodes, allowing all individual drones to be seen simultaneously.
