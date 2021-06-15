from typing import List

from myLyrics.src.models.song import Song


class SearchResult:
    def __init__(self, searched_song, songs):
        self.searched_song: str = searched_song
        self.songs: List[Song] = songs
