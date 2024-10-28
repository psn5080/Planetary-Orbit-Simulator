import pygame
import math
from typing import Tuple

# Initialize Pygame
try:
    pygame.init()
except pygame.error as e:
    print(f"Failed to initialize Pygame: {e}")
    exit(1)

# Constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
LIGHT_GREY = (211, 211, 211)
FONT = pygame.font.SysFont("arial", 16)  # Changed font to Arial

# Set up display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def draw(self, win):
        pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))
        text = FONT.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + (self.width - text.get_width()) / 2, self.y + (self.height - text.get_height()) / 2))

    def is_clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

class Planet:
    AU = 149.6e6 * 1000  # Astronomical Unit in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 200 / AU  # Adjust this value to make planets more visible
    TIMESTEP = 3600 * 24  # 1 day in seconds

    def __init__(self, x: float, y: float, radius: int, color: Tuple[int, int, int], mass: float, name: str):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        self.show_stats = False

    def draw(self, win, state):
        scale = self.SCALE * state['zoom_scale']
        x = (self.x * scale + WIDTH / 2) + state['pan_x']
        y = (self.y * scale + HEIGHT / 2) + state['pan_y']

        if state['show_orbits'] and len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = (x * scale + WIDTH / 2) + state['pan_x']
                y = (y * scale + HEIGHT / 2) + state['pan_y']
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), int(self.radius * state['zoom_scale']))
        
        # Display planet name
        name_text = FONT.render(self.name, 1, WHITE)
        win.blit(name_text, (x - name_text.get_width()/2, y - name_text.get_height()/2 - 20))

        # Display stats if selected
        if self.show_stats and not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            velocity_text = FONT.render(f"Vel: {round(math.sqrt(self.x_vel**2 + self.y_vel**2), 1)} m/s", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2 - 40))
            win.blit(velocity_text, (x - velocity_text.get_width()/2, y - velocity_text.get_height()/2 - 60))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets, time_scale):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP * time_scale
        self.y_vel += total_fy / self.mass * self.TIMESTEP * time_scale

        self.x += self.x_vel * self.TIMESTEP * time_scale
        self.y += self.y_vel * self.TIMESTEP * time_scale
        self.orbit.append((self.x, self.y))

    def kinetic_energy(self):
        return 0.5 * self.mass * (self.x_vel**2 + self.y_vel**2)

    def potential_energy(self, other):
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return -self.G * self.mass * other.mass / distance

    def toggle_stats(self):
        self.show_stats = not self.show_stats

def change_time_scale(factor, state):
    state['time_scale'] *= factor

def change_zoom_scale(factor, state):
    state['zoom_scale'] *= factor

def change_pan(dx, dy, state):
    state['pan_x'] += dx
    state['pan_y'] += dy

def toggle_pause(state):
    state['paused'] = not state['paused']

def reset_view(state):
    state['zoom_scale'] = 1
    state['pan_x'] = 0
    state['pan_y'] = 0

def toggle_orbits(state):
    state['show_orbits'] = not state['show_orbits']

def calculate_total_energy(planets):
    total_kinetic = sum(planet.kinetic_energy() for planet in planets)
    total_potential = sum(planet.potential_energy(other) for i, planet in enumerate(planets) for other in planets[i+1:])
    return total_kinetic + total_potential

def calculate_average_velocity(planets):
    total_velocity = sum(math.sqrt(planet.x_vel**2 + planet.y_vel**2) for planet in planets)
    return total_velocity / len(planets)

def main():
    run = True
    clock = pygame.time.Clock()
    state = {
        'time_scale': 1,
        'zoom_scale': 1,
        'pan_x': 0,
        'pan_y': 0,
        'paused': False,
        'show_orbits': True
    }

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000 

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 18, ORANGE, 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = -13.07 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 16, LIGHT_GREY, 5.683 * 10**26, "Saturn")
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(19.8 * Planet.AU, 0, 14, LIGHT_BLUE, 8.681 * 10**25, "Uranus")
    uranus.y_vel = -6.80 * 1000

    neptune = Planet(30.0 * Planet.AU, 0, 14, DARK_GREY, 1.024 * 10**26, "Neptune")
    neptune.y_vel = -5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    # Calculate initial total energy for accuracy measure
    initial_total_energy = calculate_total_energy(planets)

    buttons = [
        Button(10, 10, 100, 30, "Speed Up", lambda: change_time_scale(2, state)),
        Button(10, 50, 100, 30, "Slow Down", lambda: change_time_scale(0.5, state)),
        Button(10, 90, 100, 30, "Zoom In", lambda: change_zoom_scale(1.1, state)),
        Button(10, 130, 100, 30, "Zoom Out", lambda: change_zoom_scale(0.9, state)),
        Button(10, 170, 100, 30, "Pan Left", lambda: change_pan(-20, 0, state)),
        Button(10, 210, 100, 30, "Pan Right", lambda: change_pan(20, 0, state)),
        Button(10, 250, 100, 30, "Pause/Resume", lambda: toggle_pause(state)),
        Button(10, 290, 100, 30, "Reset View", lambda: reset_view(state)),
        Button(10, 330, 100, 30, "Toggle Orbits", lambda: toggle_orbits(state)),
    ]

    simulation_time = 0
    dragging = False
    last_mouse_pos = None

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Mouse wheel up
                    change_zoom_scale(1.1, state)
                elif event.button == 5:  # Mouse wheel down
                    change_zoom_scale(0.9, state)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    change_pan(dx, dy, state)
                    last_mouse_pos = (mouse_x, mouse_y)

        for button in buttons:
            if event.type == pygame.MOUSEBUTTONDOWN and button.is_clicked(pygame.mouse.get_pos()):
                button.action()

        if not state['paused']:
            for planet in planets:
                planet.update_position(planets, state['time_scale'])

        for planet in planets:
            planet.draw(WIN, state)

        for button in buttons:
            button.draw(WIN)

        # Update simulation time
        if not state['paused']:
            simulation_time += Planet.TIMESTEP * state['time_scale']

        # Calculate total energy and accuracy
        total_energy = calculate_total_energy(planets)
        energy_accuracy = 100-(abs((total_energy - initial_total_energy) / initial_total_energy) * 100)

        # Display time, energy, number of planets, average velocity, and energy accuracy
        time_text = FONT.render(f"Time: {simulation_time / (3600 * 24):.2f} days", 1, WHITE)
        energy_text = FONT.render(f"Energy: {total_energy:.2e} J", 1, WHITE)
        planet_count_text = FONT.render(f"Planets: {len(planets)}", 1, WHITE)
        avg_velocity_text = FONT.render(f"Avg Vel: {calculate_average_velocity(planets):.2f} m/s", 1, WHITE)
        accuracy_text = FONT.render(f"Energy Accuracy: {energy_accuracy:.2f}%", 1, WHITE)

        WIN.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))
        WIN.blit(energy_text, (WIDTH - energy_text.get_width() - 10, 30))
        WIN.blit(planet_count_text, (WIDTH - planet_count_text.get_width() - 10, 50))
        WIN.blit(avg_velocity_text, (WIDTH - avg_velocity_text.get_width() - 10, 70))
        WIN.blit(accuracy_text, (WIDTH - accuracy_text.get_width() - 10, 90))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()