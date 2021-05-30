import requests
from bs4 import BeautifulSoup

from models.search_result import SearchResult
from models.song import Song
from models.song_lyrics import SongLyrics

BASE_URL = "https://www.lyricsmode.com/"
SEARCH_URL = BASE_URL + "search.php?search="


def construct_search_url(search_string):
    return SEARCH_URL + search_string


def search_song(searched_song_string):
    """Return SearchResult Object"""
    searched_song_string = searched_song_string.strip()
    if searched_song_string == "":
        return

    search_url = construct_search_url(searched_song_string)
    response = requests.get(search_url)

    if response.status_code != requests.codes.ok:
        return

    html_text = response.text
    soup = BeautifulSoup(html_text, 'html.parser')

    result_list = soup.find_all("div", {"class": "lm-list"})

    # Result list must be only one
    if len(result_list) != 1:
        print("ERROR")
        return

    songs_rows = result_list[0].findChildren("div", recursive=False)

    if len(songs_rows) == 1:
        # Check if there are no more
        div = songs_rows[0]
        if len(div.find_all("div")) == 1:
            # No songs found
            result = SearchResult(searched_song_string, [])
            return result

    count = len(songs_rows)
    if count == 0:
        print("NO SONGS")
        return

    all_songs = []
    for i in range(0, count):
        song = songs_rows[i]
        singer = (song.select(".lm-link--secondary")[0])['title']
        song_name_link_tag = (song.select(".lm-link--primary")[0])

        link = song_name_link_tag['href']
        if link[0] == "/":
            link = link[1:]
        link = BASE_URL + link

        name = song_name_link_tag['title']

        song = Song(name, singer, link)
        all_songs.append(song)

    result = SearchResult(searched_song_string, all_songs)
    return result


def get_lyrics_from_link(link):
    """Return SongLyrics Object"""
    request = requests.get(link)
    if request.status_code != requests.codes.ok:
        return

    soup = BeautifulSoup(request.text, 'html.parser')
    article_info = soup.find("div", {"class": "article_info"})
    h1 = article_info.find("h1")

    song_title = h1.text
    song_title = " ".join(song_title.split()).strip()

    lyrics_section = soup.find("div", {"id": "lyrics_text"})
    for div in lyrics_section.find_all("div"):
        div.decompose()

    lyrics_text = lyrics_section.text.strip()
    song_lyrics = SongLyrics(song_title, lyrics_text)
    return song_lyrics
