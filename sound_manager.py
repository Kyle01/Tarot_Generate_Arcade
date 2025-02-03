import arcade

class SoundManager:
    def __init__(self, music_file_path):
        self.music_file_path = music_file_path
        self.music = None
        self.music_player = None
        self.sfx_sounds={}
        

    def load_music(self):
        """Load the music file."""
     
        self.music = arcade.load_sound(self.music_file_path)

    def play_music(self, volume=0.5, loop=True):
        """Play the loaded music at specified volume, optionally looping."""
        if not self.music:
            print("Music not loaded yet. Call load_music() first.")
            return
        
        # Note: arcade 3.0 introduced a new Sound API
        # If using older versions, the code might differ slightly.
        # `play_sound` returns a player object in arcade 3.0+
        self.music_player = arcade.play_sound(self.music, volume=volume, looping=loop)

    def stop_music(self):
        """Stop the music."""
        if self.music_player:
            self.music_player.stop()
            self.music_player = None
    
    def load_sfx(self, sfx_name, file_path):
        """
        Load an SFX sound into the dictionary.
        sfx_name (str): A key, e.g. 'card_draw'
        file_path (str): Path to the audio file, e.g. 'assets/sfx/card_draw.wav'
        """
        try:
            sfx_sound = arcade.load_sound(file_path)
            self.sfx_sounds[sfx_name] = sfx_sound
        except Exception as e:
            print(f"Failed to load SFX '{sfx_name}': {e}")

    def play_sfx(self, sfx_name, volume=1.0, speed=1.0):
        """Play a loaded SFX by name."""
        if sfx_name in self.sfx_sounds:
            arcade.play_sound(self.sfx_sounds[sfx_name], volume=volume, speed=speed)
        else:
            print(f"SFX '{sfx_name}' not found. Make sure you've loaded it.")