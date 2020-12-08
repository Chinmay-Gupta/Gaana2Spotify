from song_interface import Song
from selenium import webdriver
from bs4 import BeautifulSoup


def gaana_scraper(songs, webdriver_path, gaana_playlist_url):
    # @params
    # songs: list of songs initially supposed to be unpopulated
    # webdriver_path: file path of the chrome webdriver
    # gaana_playlist_url: URL with the https protocol of the playlist webpage
    # @returns songs: list of populated songs with each element as the Song object

    # Get page using Webdriver discreetly without popup browser
    driver_opts = webdriver.ChromeOptions()
    driver_opts.headless = True
    driver = webdriver.Chrome(webdriver_path, options=driver_opts)
    driver.get(gaana_playlist_url)

    # Fetch content and get HTML tags
    playlist_page_content = driver.page_source
    if playlist_page_content is None:
        print("Playlist URL can't be fetched\n")
        exit(3)
    tags_soup = BeautifulSoup(playlist_page_content, features="html.parser")

    # Scrap for songs
    div_of_songs = tags_soup.find('div', class_='s_c')  # Find div of s_c
    contents_list = div_of_songs.find_all('ul')[1]  # Find 2nd list element
    title_list = contents_list.find_all('li', class_="s_title")
    artists_list = contents_list.find_all('li', class_="s_artist")
    number_of_songs = len(title_list)
    number_of_artists = len(artists_list)
    if number_of_songs == number_of_artists:
        print("Found {} songs".format(number_of_songs))
    else:
        print("Can't parse webpage.")
        exit(4)
    for i in range(number_of_songs):
        title = (title_list[i].find('a', class_="sng_c")).get_text()
        artists = (artists_list[i]).get_text()
        new_song = Song(title, artists.split(','))
        songs.append(new_song)

    return songs
