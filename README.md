# Gaana2Spotify
This project aims to transfer user's songs from any of their public playlists in Gaana to a playlist in Spotify.
It works by asking the user for input link, which is the Gaana playlist URL. The tool will scrap the playlist for list of songs.
The list consists of <Name, Artists> and is printed on the console screen.

Once the scraping is done, Spotify user credentials are asked and API creates a new playlist "From Gaana".
Each item in the scraped list is used to search for a song ID using Spotify APIs. If found, the song is added to "From Gaana".
The success rate of transfer in my trials is about 95% and it might vary upon user's playlists. All songs are not transferred because Spotify may have an incomplete collection or search algorithms might be inefficient. Particularly, if you have uncommon songs with titles in a non-latin script or titles with redundant information, Spotify's search APIs tend to fail.

The program uses 'Spotipy 2.16.1' by Plamere - https://github.com/plamere/spotipy in the backend to simplify API calls to the Spotify servers.
Uses 'Selenium 3.141.1' to execute the webdriver. https://www.selenium.dev/
Uses 'BeautifulSoup4 3.9.4' to parse Gaana playlist page. https://pypi.org/project/beautifulsoup4/
Developed and tested on Microsoft Windows 10 20H2 with Python 3.7.3

Disclaimer:
I do not own any of Gaana, Spotify, Spotipy, Selenium or BeautifulSoup. 
'Gaana' music streaming service is a copyright property of Gamma Gaana Ltd.
'Spotify' music streaming service is a copyright property of Spotify AB.

Installation:
1. Install Chrome Webdriver and have its path in the system environment variable $WEBDRIVER_PATH
    Make sure your webdriver and Chrome browser versions are compatible. For downloads and info, check https://chromedriver.chromium.org/downloads
2. Specify your Spotify Developer Client ID, Client Secret and Redirect URI in system variables $SPOTIPY_CLIENT_ID, $SPOTIPY_CLIENT_SECRET and $SPOTIPY_REDIRECT_URI respectively.
    If you don't have these, generate them at https://developer.spotify.com/ . Without these, the spotify client will not work. 
    In case you don't want to add these to global env variables, see and change the source code at /spotify_service/spotify_feeder.py in lines 11-14

Usage:
1. Run on terminal : py Gaana2Spotify.py
2. Enter path to chrome webdriver, if you don't have its path set up as an environment variable $WEBDRIVER_PATH
3. Specify Gaana playlist URL
4. The program will list all songs that it can parse on the Gaana webpage. Confirm with Y/N.
5. Enter your username so that it will generate a public playlist "From Gaana" in your account.

After this, the program will list all the matched song equivalents in Spotify. You can find a playlist, "From Gaana" in your spotify account with all these songs added. 
    
Error Codes:
0 - normal termination
1 - unsupported OS type
2 - operation interrupted by user
3 - playlist URL unreachable
4 - playlist page in unsupported format
5 - Spotify playlists creation error
