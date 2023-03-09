import pygame
import math

pygame.init()

# Set display
WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')

# Set general font
FONT_DISTANCE = pygame.font.SysFont('comicsans', 16)
FONT_MAPPING = pygame.font.SysFont('comicsans', 30)


# Set color alias
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SIZE_SCALE = 250
    SCALE = SIZE_SCALE / AU    # 1 AU = 100 pixels
    TIMESTEP = 3600  # 1 day

    def __init__(self, x_, y_, radius, color, mass, y_start_velocity, sun=False):
        self.x = x_
        self.y = y_
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = sun
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = y_start_velocity

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT_DISTANCE.render(f'{format(self.distance_to_sun / 1000, ",.1f")}km', True, WHITE)
            win.blit(
                distance_text,
                (
                    x - distance_text.get_width() / 2,
                    y + distance_text.get_height() + self.radius / 2
                )
            )

    # Calculation forces witch are moving planets
    def attraction(self, other):
        other_x = other.x
        other_y = other.y

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

    # Calculation geometry to display planets on screen
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))


def main():
    # Frames per seconds
    fps = 60

    size_scale_text = FONT_MAPPING.render(f'Size scale: 1 / {Planet.SIZE_SCALE} * Astronomical Unit', True, WHITE)
    au_text = FONT_MAPPING.render(f'Astronomical Unit: {format(Planet.AU/10**3, ",.1f")}km', True, WHITE)
    time_scale_text = FONT_MAPPING.render(f'Time scale: {Planet.TIMESTEP/3600/24*fps} days per second', True, WHITE)

    # Setting up Planet instances
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 0, True)

    # Ok, ok... Sun isn't a Planet! Don't yell at me.
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23, -47.4 * 1000)
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, -35.02 * 1000)
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, 29.783 * 1000)
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, 24.077 * 1000)

    planets = [sun, mercury, venus, earth, mars]

    # Clock instance to set up FPS
    clock = pygame.time.Clock()
    run = True
    while run:
        # Setting up the FPS
        clock.tick(fps)

        WIN.fill(BLACK)
        WIN.blit(size_scale_text, (10, 10))
        WIN.blit(au_text, (10, 10 + size_scale_text.get_height() + 10))
        WIN.blit(time_scale_text, (10, 10 + size_scale_text.get_height() + 10 + au_text.get_height() + 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(win=WIN)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
