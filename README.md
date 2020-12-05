# Gaana2Spotify
This project aims to transfer user songs from all playlists in Gaana to a new playlist in Spotify.
It works by asking the user for input link, which is the Gaana playlist URL. The tool will scrap the playlist for list of songs.
The list consists of <Name, Artists> and is printed on the console screen.

Once the scraping is done, Spotify user credentials are asked and API creates a new playlist "From Gaana".
Each item in the scraped list is used to search for a song ID using Spotify APIs. If found, the song is added to "From Gaana".

Classes:
1. Song: 
    @attributes
        name
        artists
        spotify_song_ID
    @methods
        constructor(name, artists[])
        int get_title(): returns name
        int get_artists(): returns artists[]
        int get_spotify_id(): returns spotify_song_ID
        
        