from gaana2spotify.gaana_scraper_interface import Song
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from sys import platform

# Declare Constants
LINUX = 0
WINDOWS = 1


# Get system details
def get_os_type():
    if platform == "linux" or platform == "linux2":
        return LINUX
    if platform == "win32":
        return WINDOWS
    return None

def list_songs(songs_list):
    for i in range(len(songs_list)):
        assert(songs_list[i], Song)
        print(songs_list[i].get_title(), songs_list[i].get_artists())

def __main__():
    # Check OS Type
    if get_os_type() != WINDOWS:
        print("Platform Unsupported. This program works on Windows")
        exit()

    # Get webdriver for selenium queries and get page
    webdriver_path = os.getenv("WEBDRIVER_PATH")
    if webdriver_path is None:
        print("Webdriver Unavailable. Specify path manually: ")
        webdriver_path = input()
    driver_opts = webdriver.ChromeOptions()
    driver_opts.headless=True
    driver = webdriver.Chrome(webdriver_path, options=driver_opts)

    # Ask for Playlist URL
    print("Specify Playlist URL:\n")
    gaana_playlist_url = "https://gaana.com/playlist/chinmaygupta-ywgzd-hindi-d3xln5jq3g"
    driver.get(gaana_playlist_url)

    # List of Songs that'll be scraped
    songs = []

    # Fetch content and get HTML tags
    playlist_page_content = driver.page_source
    if playlist_page_content is None:
        print("Playlist URL can't be fetched\n")
        exit()
    tags_soup = BeautifulSoup(playlist_page_content, features="html.parser")

    # Scrap for songs
    div_of_songs = tags_soup.find('div', class_='s_c')  # Find div of s_c
    contents_list = div_of_songs.find_all('ul')[1]      # Find 2nd list element
    title_list = contents_list.find_all('li', class_="s_title")
    artists_list = contents_list.find_all('li', class_="s_artist")
    number_of_songs = len(title_list)
    number_of_artists = len(artists_list)
    if number_of_songs == number_of_artists:
        print("Found {} songs".format(number_of_songs))
    else:
        print("Can't parse webpage.")
        exit()
    for i in range(number_of_songs):
        title = (title_list[i].find('a', class_="sng_c")).get_text()
        artists = (artists_list[i]).get_text()
        new_song = Song(title, artists.split(','))
        songs.append(new_song)

    # List the found songs and confirm
    list_songs(songs)
    print("Continue to add to spotify (Y/N)?")
    response = input()
    if response != 'Y' or response != 'y':
        exit()



__main__()