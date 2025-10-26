import pygame
import math
import random
import os
from config import *
from .grid import Grid
from util import Direction, draw_text
from .player import Player
from .card import Card
from .button import Button
from .sound_manager import SoundManager
from .particle import ParticleSystem, SnakeCelebration


class Game:
    def __init__(self, sound_manager, game_settings):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Template")
        self.clock = pygame.time.Clock()
        # Initialize sound manager
        self.sound_manager = sound_manager
        self.game_settings = game_settings

        # Apply settings
        global MAX_ROUNDS, SNAKE_MOVE_INTERVAL, MAX_HAND_SIZE, GRID_SIZE
        MAX_ROUNDS = game_settings['max_rounds']
        SNAKE_MOVE_INTERVAL = game_settings['snake_speed']
        MAX_HAND_SIZE = game_settings['hand_size']
        GRID_SIZE = game_settings['grid_size']

        # Make the grid in the center of the window
        grid_width = GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * GAP
        grid_height = GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * GAP
        grid_top_left = ((WIDTH - grid_width) // 2,
                         (HEIGHT - grid_height) // 2)
        self.grid = Grid(grid_top_left, CELL_SIZE, GRID_SIZE,
                         GRID_SIZE, color=GRASSY_GREEN, gap=GAP)

        # Start planning music
        self.sound_manager.play_music('planning', loop=True)

        player_one_start = (SNAKE_INIT_LENGTH, 0)  # Top-left corner
        player_one = Player("Player 1", start_pos=player_one_start,
                            grid_top_left=grid_top_left, init_direction=Direction.RIGHT, sound_manager=self.sound_manager)
        player_two_start = (GRID_SIZE - SNAKE_INIT_LENGTH - 1,
                            GRID_SIZE - 1)  # Bottom-right corner
        player_two = Player("Player 2", start_pos=player_two_start,
                            grid_top_left=grid_top_left, init_direction=Direction.LEFT, sound_manager=self.sound_manager)

        self.players = [player_one, player_two]
        self.turn = 0  # Index of current player's turn
        self.run_simulation = False

        # Add these new attributes
        self.particle_system = ParticleSystem()
        self.celebration = None
        self.win_animation_started = False
        self.win_screen_timer = 0
        self.show_win_screen = False

        # Win screen buttons (created when needed)
        self.replay_button = None
        self.menu_button = None

        self.confirm_button = Button(
            x=WIDTH - 100 - 20, y=HEIGHT - 40 - 20, width=100, height=40,
            function=self.confirm_selection,
            text="Confirm",
            color=LIME_GREEN,
            hover_color=PASTEL_GREEN,
            click_color=FOREST_GREEN,
            font_size=24,
            text_color=WHITE,
            tooltip_text="Confirm Selection",
            tooltip_font_size=16,
            initially_disabled=True,
            hide_when_disabled=False,
            key_binding=pygame.K_RETURN
        )

        self.undo_button = Button(
            x=WIDTH - 100 - 20, y=HEIGHT - 40 - 20 - 40 - 20, width=100, height=40,
            function=self.undo_last_move,
            text="Undo",
            color=CRIMSON_RED,
            hover_color=LIGHT_CORAL,
            click_color=DARK_RED,
            font_size=24,
            text_color=WHITE,
            tooltip_text="Undo",
            tooltip_font_size=16,
            initially_disabled=False,
            hide_when_disabled=True
        )

        self.running = True
        self.return_to_menu = False
        self.time = 0
        self.dt = self.clock.get_time() / 1000
        self.winner = None  # "one", "two", "draw"

        # Update button sounds
        self.confirm_button.hover_sound = None
        self.confirm_button.click_sound = None
        self.undo_button.hover_sound = None
        self.undo_button.click_sound = None

    def run(self, clock):
        """Modified run method that returns state"""
        self.clock = clock
        self.sound_manager.play_music('planning', loop=True)

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        if self.return_to_menu:
            self.running = True
            return 'menu'
        else:
            return 'quit'

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            self.players[self.turn].handle_events(event)

        if not self.run_simulation:
            self.undo_button.update(events)
            self.confirm_button.update(events)

            # Manual button sound handling
            if self.undo_button.hovered and not self.undo_button.was_hovered:
                self.sound_manager.play_sound('button_hover')
            if self.confirm_button.hovered and not self.confirm_button.was_hovered:
                self.sound_manager.play_sound('button_hover')

        # Update win screen buttons
        if self.show_win_screen and self.replay_button:
            # Track hover state for sounds
            replay_was_hovered = self.replay_button.hovered
            menu_was_hovered = self.menu_button.hovered

            self.replay_button.update(events)
            if self.menu_button:
                self.menu_button.update(events)

            # Play hover sounds
            if self.replay_button and self.replay_button.hovered and not replay_was_hovered:
                self.sound_manager.play_sound('button_hover')
            if self.menu_button and self.menu_button.hovered and not menu_was_hovered:
                self.sound_manager.play_sound('button_hover')

    def update(self):
        self.dt = self.clock.get_time() / 1000
        self.time += self.dt

        self.particle_system.update(self.dt)

        # Update snake interpolation (always, for smooth movement)
        for player in self.players:
            player.snake.update_interpolation(self.dt)

        if not self.run_simulation and all(p.confirmed for p in self.players):
            self.run_simulation = True
            # Switch to simulation music
            self.sound_manager.play_music('simulation', loop=True, fade_ms=500)

        if self.winner in ("one", "two", "draw", "round_end") and not self.win_animation_started:
            self.start_win_animation()

        # Update win screen timer
        if self.show_win_screen:
            self.win_screen_timer += self.dt

            # Keep emitting confetti
            if self.win_screen_timer < 3.0 and random.random() < 0.3:
                x = random.randint(100, WIDTH - 100)
                self.particle_system.emit_confetti_burst(x, 0, count=5)

            # Update celebration
            if self.celebration:
                self.celebration.update(self.dt)

        if self.run_simulation and not self.winner:
            if self.time > SNAKE_MOVE_INTERVAL:
                for player in self.players:
                    player.update()

                # Play subtle move sound
                self.sound_manager.play_sound('snake_move')
                self.winner = "round_end" if any(
                    p.state == "round_end" for p in self.players) else self.winner
                if not self.winner:
                    self.handle_collisions()
                self.time = 0
        else:
            self.players[self.turn].update()

            # If no cards left in hand, enable confirm button
            if self.players[self.turn].hand_empty():
                self.confirm_button.disabled = False
            else:
                self.confirm_button.disabled = True

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.grid.draw(self.screen)

        if self.run_simulation or self.show_win_screen:
            for player in self.players:
                if self.show_win_screen and self.celebration and player.snake == self.celebration.snake:
                    self.celebration.draw(self.screen)
                else:
                    player.draw(self.screen)
            self.draw_card_execution_highlight()
        else:
            self.players[self.turn].draw(self.screen)

        if not self.run_simulation:
            self.undo_button.draw(self.screen)
            self.confirm_button.draw(self.screen)

        self.draw_game_state_overlay()
        self.draw_snake_length_indicator()

        # Draw particles
        self.particle_system.draw(self.screen)

        # Draw win screen
        if self.show_win_screen:
            self.draw_win_screen(self.screen)

        pygame.display.flip()

    def undo_last_move(self):
        self.sound_manager.play_sound('undo')
        self.players[self.turn].undo_move()

    def confirm_selection(self):
        self.sound_manager.play_sound('card_confirm')
        # Set the confirm flag to True
        self.players[self.turn].confirmed = True
        # Switch turn to the next player
        self.turn = (self.turn + 1) % len(self.players)

    def handle_collisions(self):
        """Enhanced collision detection with particle effects (no self-collision)"""
        snake1 = self.players[0].snake
        snake2 = self.players[1].snake

        # Check head-to-body collisions (only with opponent)
        snake1_head_hit = snake1.segments[0] in snake2.segments
        snake2_head_hit = snake2.segments[0] in snake1.segments

        # Create collision particles
        collision_occurred = False
        collision_positions = []

        if snake1_head_hit:
            collision_occurred = True
            head_pos = snake1.segments[0]
            grid_x, grid_y = snake1.grid_top_left
            screen_x = grid_x + head_pos[0] * \
                (CELL_SIZE + GAP) + CELL_SIZE // 2
            screen_y = grid_y + head_pos[1] * \
                (CELL_SIZE + GAP) + CELL_SIZE // 2
            collision_positions.append(
                (screen_x, screen_y, BRIGHT_ORANGE, BOLD_COBALT))

        if snake2_head_hit:
            collision_occurred = True
            head_pos = snake2.segments[0]
            grid_x, grid_y = snake2.grid_top_left
            screen_x = grid_x + head_pos[0] * \
                (CELL_SIZE + GAP) + CELL_SIZE // 2
            screen_y = grid_y + head_pos[1] * \
                (CELL_SIZE + GAP) + CELL_SIZE // 2
            collision_positions.append(
                (screen_x, screen_y, BOLD_COBALT, BRIGHT_ORANGE))

        # Emit collision particles
        if collision_occurred:
            self.sound_manager.play_sound('collision')
            for x, y, color1, color2 in collision_positions:
                self.particle_system.emit_collision_explosion(
                    x, y, color1, color2, count=25)

        # Determine winner based on collisions (no self-collision)
        if snake1_head_hit and snake2_head_hit:
            self.winner = "draw"
            self.players[0].state = "draw"
            self.players[1].state = "draw"
        elif snake1_head_hit:
            self.winner = "two"
            self.players[0].state = "lose"
            self.players[1].state = "win"
        elif snake2_head_hit:
            self.winner = "one"
            self.players[0].state = "win"
            self.players[1].state = "lose"

    def replay_game(self):
        """Reset game for replay"""
        self.reset()
        self.particle_system.clear()
        self.win_animation_started = False
        self.show_win_screen = False
        self.celebration = None
        self.replay_button = None
        self.menu_button = None

        # Restart planning music
        self.sound_manager.play_music('planning', loop=True, fade_ms=500)

    def goto_menu(self):
        """Return to main menu"""
        self.sound_manager.play_sound('button_click')
        self.return_to_menu = True
        self.running = False

    def reset(self):
        """Enhanced reset that cleans up win screen state"""
        self.turn = 0
        self.run_simulation = False
        self.winner = None
        self.time = 0
        self.win_animation_started = False
        self.show_win_screen = False
        self.win_screen_timer = 0

        player_one_start = (SNAKE_INIT_LENGTH, 0)
        player_one = Player("Player 1", start_pos=player_one_start,
                            grid_top_left=self.grid.top_left, init_direction=Direction.RIGHT, sound_manager=self.sound_manager)
        player_two_start = (GRID_SIZE - SNAKE_INIT_LENGTH - 1,
                            GRID_SIZE - 1)
        player_two = Player("Player 2", start_pos=player_two_start,
                            grid_top_left=self.grid.top_left, init_direction=Direction.LEFT, sound_manager=self.sound_manager)

        self.players = [player_one, player_two]

    def draw_game_state_overlay(self):
        """Draw turn indicator, round counter, and player status"""
        font_small = pygame.font.Font(MINECRAFT_FONT, 20)

        surface = self.screen

        if not self.run_simulation:
            # Show whose turn it is
            turn_text = f"{self.players[self.turn].name}'s Turn"
            if self.turn == 0:
                draw_text(surface, turn_text, font_small, WHITE,
                          (10 + font_small.size(turn_text)[0] // 2, 15))
            else:
                draw_text(surface, turn_text, font_small, WHITE,
                          (WIDTH - 10 - font_small.size(turn_text)[0] // 2, 15))

            # Show cards remaining
            cards_left = len(self.players[self.turn].hand.cards)
            cards_text = f"Cards: {cards_left}/{MAX_HAND_SIZE}"
            draw_text(surface, cards_text, font_small,
                      LIGHT_GRAY, (WIDTH // 2, 15))

        else:
            # Show round counter during simulation
            if self.players[0].card_exec:
                current_round = self.players[0].card_exec.round
                max_rounds = self.players[0].card_exec.max_rounds
                round_text = f"Round {current_round}/{max_rounds}"
                draw_text(surface, round_text, font_small,
                          WHITE, (WIDTH // 2, 15))

    def draw_card_execution_highlight(self):
        """Highlight the card being executed"""
        if not self.run_simulation:
            return

        surface = self.screen

        for player in self.players:
            if player.card_exec and player.card_exec.current_index > 0:
                current_idx = player.card_exec.current_index - 1
                if current_idx < len(player.chosen_cards):
                    card = player.chosen_cards[current_idx]
                    # Draw a glowing effect around the card
                    glow_rect = card.rect.inflate(10, 10)
                    glow_color = WARM_GOLDEN if player.name == "Player 1" else LIGHT_SKY_BLUE
                    pygame.draw.rect(surface, glow_color, glow_rect,
                                     width=4, border_radius=12)

    def draw_win_screen(self, surface):
        """Display winner announcement with animations"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        from util import draw_text
        font_huge = pygame.font.Font(MINECRAFT_FONT, 72)
        font_large = pygame.font.Font(MINECRAFT_FONT, 36)
        font_medium = pygame.font.Font(MINECRAFT_FONT, 24)

        # Determine winner info
        if self.winner == "draw":
            title = "DRAW!"
            subtitle = "Both Snakes Collided"
            color = LIGHT_GRAY
        elif self.winner == "round_end":
            title = "DRAW!"
            subtitle = "Rounds end"
            color = LIGHT_GRAY

        elif self.winner == "one":
            title = "PLAYER 1 WINS!"
            subtitle = "Orange Snake Victorious!"
            color = BRIGHT_ORANGE
        else:
            title = "PLAYER 2 WINS!"
            subtitle = "Blue Snake Victorious!"
            color = BOLD_COBALT

        # Animate title (bounce effect)
        bounce = abs(math.sin(self.win_screen_timer * 3)) * 10
        title_y = HEIGHT // 2 - 80 - bounce

        # Draw title with shadow
        draw_text(surface, title, font_huge, (0, 0, 0),
                  (WIDTH // 2 + 3, title_y + 3))
        draw_text(surface, title, font_huge, color, (WIDTH // 2, title_y))

        # Draw subtitle
        draw_text(surface, subtitle, font_large,
                  WHITE, (WIDTH // 2, HEIGHT // 2))

        # Draw stats
        if self.winner in ("one", "two"):
            winner_idx = 0 if self.winner == "one" else 1
            winner_snake = self.players[winner_idx].snake
            stats = f"Final Length: {len(winner_snake.segments)}"
            draw_text(surface, stats, font_medium, LIGHT_GRAY,
                      (WIDTH // 2, HEIGHT // 2 + 50))

        # Draw buttons
        if self.replay_button and self.menu_button:
            self.replay_button.draw(surface)
            self.menu_button.draw(surface)

    def draw_snake_length_indicator(self):
        """Show snake lengths for both players"""
        if not self.run_simulation:
            return

        font = pygame.font.Font(MINECRAFT_FONT, 18)
        surface = self.screen

        for i, player in enumerate(self.players):
            length = len(player.snake.segments)
            text = f"Length: {length}"

            # Position based on player
            if i == 0:  # Player 1
                x = 10 + font.size(text)[0] // 2
                color = BRIGHT_ORANGE
            else:  # Player 2
                x = WIDTH - 10 - font.size(text)[0] // 2
                color = BOLD_COBALT

            y = 15
            draw_text(surface, text, font, color, (x, y))

    def start_win_animation(self):
        """Initialize win screen animation"""
        if self.win_animation_started:
            return

        # Play win sound and stop music
        self.sound_manager.play_sound('win')
        self.sound_manager.stop_music(fade_ms=1000)

        self.win_animation_started = True
        self.win_screen_timer = 0
        self.show_win_screen = True

        # Create confetti bursts at multiple locations
        for _ in range(5):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(50, 200)
            self.particle_system.emit_confetti_burst(x, y, count=30)

        # Add sparkles around winner
        if self.winner in ("one", "two"):
            winner_idx = 0 if self.winner == "one" else 1
            winner_snake = self.players[winner_idx].snake

            if winner_snake.segments:
                head_pos = winner_snake.segments[0]
                grid_x, grid_y = winner_snake.grid_top_left
                screen_x = grid_x + head_pos[0] * \
                    (CELL_SIZE + GAP) + CELL_SIZE // 2
                screen_y = grid_y + head_pos[1] * \
                    (CELL_SIZE + GAP) + CELL_SIZE // 2

                color = BRIGHT_ORANGE if self.winner == "one" else BOLD_COBALT
                self.particle_system.emit_sparkles(
                    screen_x, screen_y, color, count=20)

            # Start snake celebration
            self.celebration = SnakeCelebration(
                winner_snake,
                winner_snake.grid_top_left,
                CELL_SIZE,
                GAP
            )

        # Create buttons
        self.create_win_screen_buttons()

    def create_win_screen_buttons(self):
        """Create replay and menu buttons"""
        button_y = HEIGHT // 2 + 120

        self.replay_button = Button(
            x=WIDTH // 2 - 120,
            y=button_y,
            width=120,
            height=50,
            function=self.replay_game,
            text="Replay",
            color=LIME_GREEN,
            hover_color=PASTEL_GREEN,
            click_color=FOREST_GREEN,
            font=MINECRAFT_FONT,
            font_size=24,
            text_color=WHITE,
            tooltip_text="Play Again"
        )

        self.menu_button = Button(
            x=WIDTH // 2 + 20,
            y=button_y,
            width=100,
            height=50,
            function=self.goto_menu,
            text="Menu",
            color=BOLD_COBALT,
            hover_color=LIGHT_SKY_BLUE,
            click_color=(0, 50, 200),
            font=MINECRAFT_FONT,
            font_size=24,
            text_color=WHITE,
            tooltip_text="Main Menu"
        )
