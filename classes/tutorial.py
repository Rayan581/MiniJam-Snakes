import pygame
from config import *
from .button import Button
from util import draw_text


class TutorialPage:
    """Tutorial/Instructions screen"""

    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.running = True
        self.next_state = None

        # Fonts
        self.title_font = pygame.font.Font(MINECRAFT_FONT, 48)
        self.heading_font = pygame.font.Font(MINECRAFT_FONT, 28)
        self.text_font = pygame.font.Font(MINECRAFT_FONT, 18)
        self.small_font = pygame.font.Font(MINECRAFT_FONT, 14)

        # Current page
        self.current_page = 0
        self.max_pages = 3  # 0: Overview, 1: Cards, 2: Tips

        # Navigation buttons
        button_y = HEIGHT - 80
        self.back_button = Button(
            x=50, y=button_y, width=120, height=50,
            function=self.go_back,
            text="Back",
            color=(200, 100, 100),
            hover_color=(220, 120, 120),
            click_color=(180, 80, 80),
            font=MINECRAFT_FONT,
            font_size=24,
            text_color=WHITE
        )

        self.prev_button = Button(
            x=WIDTH // 2 - 180, y=button_y, width=150, height=50,
            function=self.prev_page,
            text="< Previous",
            color=(100, 150, 200),
            hover_color=(120, 170, 220),
            click_color=(80, 130, 180),
            font=MINECRAFT_FONT,
            font_size=20,
            text_color=WHITE,
            initially_disabled=True
        )

        self.next_button = Button(
            x=WIDTH // 2 + 30, y=button_y, width=150, height=50,
            function=self.next_page,
            text="Next >",
            color=(100, 150, 200),
            hover_color=(120, 170, 220),
            click_color=(80, 130, 180),
            font=MINECRAFT_FONT,
            font_size=20,
            text_color=WHITE
        )

        self.buttons = [self.back_button, self.prev_button, self.next_button]

        # Tutorial content
        self.pages = self._create_tutorial_content()

    def _create_tutorial_content(self):
        """Create tutorial pages content"""
        return [
            # Page 0: Overview
            {
                'title': 'HOW TO PLAY',
                'sections': [
                    {
                        'heading': 'Game Objective',
                        'text': [
                            'Plan your snake\'s moves to outlast your opponent!',
                            'Use strategy and card selection to win.'
                        ]
                    },
                    {
                        'heading': 'Turn-Based Planning',
                        'text': [
                            '1. Each player selects cards from their hand',
                            '2. Cards determine your snake\'s actions',
                            '3. After both players confirm, watch the simulation!',
                            '4. Snakes execute moves simultaneously'
                        ]
                    },
                    {
                        'heading': 'Winning Conditions',
                        'text': [
                            '• Opponent hits your snake body',
                            '• Both snakes collide = Draw',
                            '• All rounds complete = Draw'
                        ]
                    }
                ]
            },

            # Page 1: Card Types
            {
                'title': 'CARD TYPES',
                'sections': [
                    {
                        'heading': 'Move Cards',
                        'text': [
                            'MOVE LEFT/RIGHT: Turn and move forward',
                            '  Use to navigate around the grid'
                        ],
                        'color': BRIGHT_ORANGE
                    },
                    {
                        'heading': 'Special Actions',
                        'text': [
                            'DOUBLE MOVE: Move forward twice (fast!)',
                            'GROW: Add a segment and move',
                            'SHRINK: Remove tail segment and move',
                            'REVERSE: Flip snake direction',
                            'SKIP: Do nothing this turn'
                        ],
                        'color': BOLD_COBALT
                    },
                    {
                        'heading': 'Card Selection',
                        'text': [
                            '• Click cards to select them',
                            '• Cards move to your action queue',
                            '• Use UNDO to return last card',
                            '• Click CONFIRM when ready',
                            '• Keep your cards hidden from the other player'
                        ]
                    }
                ]
            },

            # Page 2: Strategy Tips
            {
                'title': 'STRATEGY & TIPS',
                'sections': [
                    {
                        'heading': 'Pro Tips',
                        'text': [
                            '✓ Plan ahead: Think multiple moves',
                            '✓ Control space: Use your body to block',
                            '✓ Mind the edges: Grid wraps around',
                            '✓ Watch opponent: Predict their moves',
                            '✓ Length matters: Longer = more threat'
                        ],
                        'color': LIME_GREEN
                    },
                    {
                        'heading': 'Advanced Tactics',
                        'text': [
                            'TRAPPING: Create walls with your body',
                            'BAITING: Lead opponent into mistakes',
                            'REVERSAL: Surprise direction changes',
                            'SPACING: Use SKIP to time attacks'
                        ],
                        'color': WARM_GOLDEN
                    },
                    {
                        'heading': 'Common Mistakes',
                        'text': [
                            '✗ Moving too predictably',
                            '✗ Ignoring the grid wrap',
                            '✗ Not using SKIP strategically',
                            '✗ Growing without space'
                        ],
                        'color': CRIMSON_RED
                    }
                ]
            }
        ]

    def go_back(self):
        self.sound_manager.play_sound('button_click')
        self.next_state = 'menu'
        self.running = False

    def next_page(self):
        if self.current_page < self.max_pages - 1:
            self.sound_manager.play_sound('button_click')
            self.current_page += 1
            self.update_button_states()

    def prev_page(self):
        if self.current_page > 0:
            self.sound_manager.play_sound('button_click')
            self.current_page -= 1
            self.update_button_states()

    def update_button_states(self):
        """Enable/disable prev/next buttons based on current page"""
        self.prev_button.set_disabled(self.current_page == 0)
        self.next_button.set_disabled(self.current_page == self.max_pages - 1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = 'quit'
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.go_back()
                elif event.key == pygame.K_RIGHT:
                    self.next_page()
                elif event.key == pygame.K_LEFT:
                    self.prev_page()

        # Update buttons
        for button in self.buttons:
            old_hover = button.hovered
            button.update(events)
            if button.hovered and not old_hover:
                self.sound_manager.play_sound('button_hover')

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(DARK_GRAY)

        # Draw background pattern
        for x in range(0, WIDTH, 40):
            for y in range(0, HEIGHT, 40):
                color = (50, 50, 50) if (
                    (x // 40) + (y // 40)) % 2 == 0 else (45, 45, 45)
                pygame.draw.rect(self.screen, color, (x, y, 40, 40))

        # Get current page content
        page = self.pages[self.current_page]

        # Draw title
        draw_text(self.screen, page['title'], self.title_font,
                  BRIGHT_ORANGE, (WIDTH // 2, 60))

        # Draw page indicator
        page_text = f"Page {self.current_page + 1} / {self.max_pages}"
        draw_text(self.screen, page_text, self.small_font,
                  LIGHT_GRAY, (WIDTH // 2, 100))

        # Draw sections
        y_offset = 150
        for section in page['sections']:
            # Draw heading
            heading_color = section.get('color', WHITE)
            draw_text(self.screen, section['heading'], self.heading_font,
                      heading_color, (WIDTH // 2, y_offset))
            y_offset += 40

            # Draw text lines
            for line in section['text']:
                draw_text(self.screen, line, self.text_font,
                          LIGHT_GRAY, (WIDTH // 2, y_offset))
                y_offset += 30

            y_offset += 20  # Space between sections

        # Draw controls hint
        controls_text = "Use Arrow Keys or buttons to navigate"
        draw_text(self.screen, controls_text, self.small_font,
                  (150, 150, 150), (WIDTH // 2, HEIGHT - 20))

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def run(self, clock):
        """Run the tutorial loop"""
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)

            dt = clock.tick(FPS) / 1000
            self.update(dt)
            self.draw()

        return self.next_state
