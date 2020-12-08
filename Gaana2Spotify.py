from song_interface import Song
import gaana2spotify.gaana_scraper_implementation as scraper
import spotify_service.spotify_feeder as spotify
import os
from sys import platform
import datetime

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
        assert (isinstance(songs_list[i], Song))
        print(songs_list[i].get_title(), songs_list[i].get_artists())


def wrap_up(successfully_ported, failed_to_port):
    # Store transfer info in log file
    outcome = 'Ported {} songs successfully. {} Failed.'.format(len(successfully_ported), len(failed_to_port))
    print(outcome)
    current_timestamp = datetime.datetime.now()
    filename = current_timestamp.strftime("%Y-%m-%d %H-%M-%S") + '.txt'
    log_file = open(filename, 'w', encoding="utf-8")
    log_file.write(
        'Timestamp: ' + str(current_timestamp) + '\n' + outcome + '\n-----------------------------------\n\n')
    log_file.write('Successfully ported songs:\n')
    for i in range(len(successfully_ported)):
        log_file.write((successfully_ported[i] + '\n'))
    log_file.write('\n\nSongs that failed to transfer:\n')
    for i in range(len(failed_to_port)):
        log_file.write((failed_to_port[i] + '\n'))
    log_file.close()

    print("\nDONE. Please refer to {} for transfer info.".format(filename))


def __main__():
    # Check OS Type
    if get_os_type() != WINDOWS:
        print("Platform Unsupported. This program works on Microsoft Windows")
        exit(1)

    # List of Songs that'll be scraped
    songs = []

    # Get webdriver for selenium queries and get page
    webdriver_path = os.getenv("WEBDRIVER_PATH")
    if webdriver_path is None:
        print("Webdriver Unavailable. Specify path manually: ")
        webdriver_path = input()

    # Ask for Playlist URL
    print("Specify Playlist URL: ")
    gaana_playlist_url = input()

    # Scrap gaana webpage for song
    print('Scraping Page. Please Wait.')
    songs = scraper.gaana_scraper(songs, webdriver_path=webdriver_path, gaana_playlist_url=gaana_playlist_url)

    # List the found songs and confirm
    list_songs(songs)
    print("Continue to add to spotify (Y/N)?")
    response = input()
    if response != 'Y' and response != 'y':
        print("Operation cancelled. Exiting.")
        exit(2)

    # Attempt to Transfer
    successfully_ported = []
    failed_to_port = []
    succeeded, failed = spotify.spotify_push(songs)
    successfully_ported += succeeded
    failed_to_port += failed

    wrap_up(successfully_ported, failed_to_port)
    exit(0)

__main__()
