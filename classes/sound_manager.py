import pygame
import os


class SoundManager:
    """Manages all game sounds and music"""

    def __init__(self):
        pygame.mixer.init()

        # Sound effects
        self.sounds = {}
        self.music_tracks = {}
        self.current_music = None
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # Load sounds (with fallback if files don't exist)
        self._load_sounds()

    def _load_sounds(self):
        """Load all sound files with proper error handling"""
        sound_files = {
            'card_select': 'assets/sounds/card_select.wav',
            'card_confirm': 'assets/sounds/card_confirm.wav',
            'collision': 'assets/sounds/collision.wav',
            'button_hover': 'assets/sounds/button_hover.wav',
            'button_click': 'assets/sounds/button_click.wav',
            'undo': 'assets/sounds/undo.wav',
            'win': 'assets/sounds/win.wav',
            'snake_move': 'assets/sounds/snake_move.wav',
        }

        for name, path in sound_files.items():
            try:
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.sfx_volume)
                else:
                    # Generate procedural sound if file doesn't exist
                    self.sounds[name] = self._generate_sound(name)
            except Exception as e:
                print(f"Warning: Could not load sound '{name}': {e}")
                self.sounds[name] = self._generate_sound(name)

        # Music tracks
        self.music_tracks = {
            'planning': 'assets/music/planning.mp3',
            'simulation': 'assets/music/simulation.mp3',
            'menu': 'assets/music/menu.mp3',
        }

    def _generate_sound(self, sound_type):
        """Generate simple procedural sounds using pygame"""
        # Create a simple beep sound as fallback
        sample_rate = 22050
        duration = 0.1
        frequency = 440

        if sound_type == 'card_select':
            frequency = 523  # C5
            duration = 0.05
        elif sound_type == 'card_confirm':
            frequency = 659  # E5
            duration = 0.15
        elif sound_type == 'collision':
            frequency = 220  # A3
            duration = 0.2
        elif sound_type == 'button_hover':
            frequency = 440  # A4
            duration = 0.03
        elif sound_type == 'button_click':
            frequency = 523  # C5
            duration = 0.08
        elif sound_type == 'undo':
            frequency = 392  # G4
            duration = 0.1
        elif sound_type == 'win':
            frequency = 784  # G5
            duration = 0.3
        elif sound_type == 'snake_move':
            frequency = 330  # E4
            duration = 0.04

        # Generate sine wave
        n_samples = int(sample_rate * duration)
        import numpy as np
        import math

        # Create sine wave
        wave = np.array([
            int(4096 * math.sin(2 * math.pi * frequency * i / sample_rate))
            for i in range(n_samples)
        ], dtype=np.int16)

        # Apply envelope (fade in/out)
        envelope = np.linspace(0, 1, n_samples // 10)
        wave[:len(envelope)] = (wave[:len(envelope)]
                                * envelope).astype(np.int16)
        wave[-len(envelope):] = (wave[-len(envelope):]
                                 * envelope[::-1]).astype(np.int16)

        # Create stereo sound
        stereo_wave = np.column_stack((wave, wave))

        sound = pygame.sndarray.make_sound(stereo_wave)
        sound.set_volume(self.sfx_volume)
        return sound

    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound '{sound_name}': {e}")

    def play_music(self, track_name, loop=True, fade_ms=1000):
        """Play background music with optional fade-in"""
        if track_name == self.current_music:
            return  # Already playing

        if track_name in self.music_tracks:
            music_path = self.music_tracks[track_name]

            # Stop current music with fade out
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(fade_ms)

            try:
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)
                    self.current_music = track_name
                else:
                    print(f"Music file not found: {music_path}")
            except Exception as e:
                print(f"Error playing music '{track_name}': {e}")

    def stop_music(self, fade_ms=1000):
        """Stop background music with fade out"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None

    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def pause_music(self):
        """Pause background music"""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """Resume background music"""
        pygame.mixer.music.unpause()
