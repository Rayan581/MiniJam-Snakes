import pygame
import random
import math


class Particle:
    """Base particle class for visual effects"""

    def __init__(self, x, y, color, lifetime=1.0):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.age = 0
        self.alive = True

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        pass


class Confetti(Particle):
    """Confetti particle that falls and rotates"""

    def __init__(self, x, y):
        colors = [
            (255, 100, 100),  # Red
            (100, 255, 100),  # Green
            (100, 100, 255),  # Blue
            (255, 255, 100),  # Yellow
            (255, 100, 255),  # Magenta
            (100, 255, 255),  # Cyan
        ]
        super().__init__(x, y, random.choice(colors), lifetime=3.0)

        self.vx = random.uniform(-100, 100)
        self.vy = random.uniform(-200, -400)
        self.gravity = 500
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-360, 360)
        self.width = random.randint(6, 12)
        self.height = random.randint(3, 6)

    def update(self, dt):
        super().update(dt)

        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rotation += self.rotation_speed * dt

        # Add some air resistance
        self.vx *= 0.99

    def draw(self, surface):
        if not self.alive:
            return

        # Fade out towards end of lifetime
        alpha = max(0, 255 * (1 - self.age / self.lifetime))

        # Create a surface for the confetti
        confetti_surface = pygame.Surface(
            (self.width * 2, self.height * 2), pygame.SRCALPHA)

        # Draw rotated rectangle
        rect_surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        color_with_alpha = (*self.color, int(alpha))
        rect_surface.fill(color_with_alpha)

        # Rotate
        rotated = pygame.transform.rotate(rect_surface, self.rotation)
        rect = rotated.get_rect(center=(self.width, self.height))
        confetti_surface.blit(rotated, rect)

        surface.blit(confetti_surface, (self.x -
                     self.width, self.y - self.height))


class Sparkle(Particle):
    """Star-like sparkle particle"""

    def __init__(self, x, y, color):
        super().__init__(x, y, color, lifetime=0.8)
        self.max_size = random.randint(3, 8)

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        if not self.alive:
            return

        # Pulse effect
        progress = self.age / self.lifetime
        if progress < 0.5:
            size = self.max_size * (progress * 2)
        else:
            size = self.max_size * (1 - (progress - 0.5) * 2)

        if size < 1:
            return

        # Draw star shape
        points = 5
        outer_radius = size
        inner_radius = size * 0.4

        star_points = []
        for i in range(points * 2):
            angle = math.pi * i / points - math.pi / 2
            if i % 2 == 0:
                r = outer_radius
            else:
                r = inner_radius

            x = self.x + r * math.cos(angle)
            y = self.y + r * math.sin(angle)
            star_points.append((x, y))

        if len(star_points) >= 3:
            pygame.draw.polygon(surface, self.color, star_points)


class SnakeCelebration:
    """Makes the winning snake dance/wiggle"""

    def __init__(self, snake, grid_top_left, cell_size, gap):
        self.snake = snake
        self.grid_top_left = grid_top_left
        self.cell_size = cell_size
        self.gap = gap
        self.time = 0
        self.amplitude = 8  # Pixels of wiggle
        self.frequency = 6  # Speed of wiggle
        self.original_segments = [seg for seg in snake.segments]
        self.wiggle_offsets = [(0, 0) for _ in snake.segments]

    def update(self, dt):
        self.time += dt
        self.calculate_wiggle()

    def calculate_wiggle(self):
        """Calculate wiggle offsets for each segment"""
        for i in range(len(self.original_segments)):
            # Create wave effect that travels along the snake
            offset_x = math.sin(
                self.time * self.frequency + i * 0.5) * self.amplitude
            offset_y = math.cos(
                self.time * self.frequency + i * 0.5) * self.amplitude
            self.wiggle_offsets[i] = (offset_x, offset_y)

    def get_screen_pos(self, grid_x, grid_y, segment_index):
        """Get the screen position with wiggle applied"""
        start_x, start_y = self.grid_top_left

        # Base screen position
        screen_x = start_x + grid_x * (self.cell_size + self.gap)
        screen_y = start_y + grid_y * (self.cell_size + self.gap)

        # Apply wiggle
        if segment_index < len(self.wiggle_offsets):
            offset_x, offset_y = self.wiggle_offsets[segment_index]
            screen_x += offset_x
            screen_y += offset_y

        return screen_x, screen_y

    def draw(self, surface):
        """Draw the snake with wiggle effect applied"""
        for i, (gx, gy) in enumerate(self.snake.segments):
            x, y = self.get_screen_pos(gx, gy, i)
            rect = (x, y, self.cell_size, self.cell_size)

            # Pick color (head vs body)
            color = self.snake.head_color if i == 0 else self.snake.body_color

            pygame.draw.rect(surface, color, rect, border_radius=5)


class CollisionParticle(Particle):
    """Explosion particle when snakes collide"""

    def __init__(self, x, y, color):
        super().__init__(x, y, color, lifetime=0.8)

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(100, 300)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = random.randint(4, 8)
        self.friction = 0.95

    def update(self, dt):
        super().update(dt)

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Apply friction
        self.vx *= self.friction
        self.vy *= self.friction

    def draw(self, surface):
        if not self.alive:
            return

        # Fade out
        alpha = max(0, 255 * (1 - self.age / self.lifetime))

        # Draw circle
        progress = self.age / self.lifetime
        current_size = int(self.size * (1 - progress * 0.5))

        if current_size < 1:
            return

        # Create surface for alpha blending
        particle_surface = pygame.Surface(
            (current_size * 2, current_size * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color, int(alpha))
        pygame.draw.circle(particle_surface, color_with_alpha,
                           (current_size, current_size), current_size)

        surface.blit(particle_surface, (self.x -
                     current_size, self.y - current_size))


class ShockWave(Particle):
    """Expanding ring effect for collisions"""

    def __init__(self, x, y, color):
        super().__init__(x, y, color, lifetime=0.6)
        self.max_radius = 40

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        if not self.alive:
            return

        progress = self.age / self.lifetime
        radius = int(self.max_radius * progress)
        alpha = int(255 * (1 - progress))

        if radius < 2:
            return

        # Draw expanding circle
        ring_surface = pygame.Surface(
            (radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
        color_with_alpha = (*self.color, alpha)
        pygame.draw.circle(ring_surface, color_with_alpha,
                           (radius + 5, radius + 5), radius, width=3)

        surface.blit(ring_surface, (self.x - radius - 5, self.y - radius - 5))


class ParticleSystem:
    """Manages all particles"""

    def __init__(self):
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def emit_confetti_burst(self, x, y, count=50):
        """Create a burst of confetti at position"""
        for _ in range(count):
            self.particles.append(Confetti(x, y))

    def emit_sparkles(self, x, y, color, count=10):
        """Create sparkles at position"""
        for _ in range(count):
            offset_x = random.uniform(-30, 30)
            offset_y = random.uniform(-30, 30)
            self.particles.append(Sparkle(x + offset_x, y + offset_y, color))

    def emit_collision_explosion(self, x, y, color1, color2, count=30):
        """Create explosion effect at collision point"""
        # Add collision particles
        for _ in range(count):
            # Mix both colors
            color = color1 if random.random() < 0.5 else color2
            self.particles.append(CollisionParticle(x, y, color))

        # Add shockwave
        self.particles.append(ShockWave(x, y, (255, 255, 255)))

        # Add extra sparkles
        for _ in range(15):
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            self.particles.append(Sparkle(x + offset_x, y + offset_y, color))

    def update(self, dt):
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

    def clear(self):
        self.particles.clear()
