# Define data structures for scraper.
# SONG: Class to store song info.

class Song:
    name = "Untitled_Song"
    artists = []
    spotify_song_ID = "0"

    def __init__(self, name, artists):
        self.name = name
        self.artists = artists

    def get_title(self):
        return self.name

    def get_artists(self):
        return self.artists

    def get_spotify_id(self):
        return self.spotify_song_ID

    def edit_title(self, new_title):
        self.name = new_title

    def add_artist(self, artist):
        self.artists.add(artist)

    def add_spotify_id(self, id):
        if self.spotify_song_ID!=0:
            print("ERROR: Can't add ID to ", self.get_title(), ", ID already generated : ", self.get_spotify_id())
        else:
            self.spotify_song_ID = id




