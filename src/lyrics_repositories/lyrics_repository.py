from abc import ABC, abstractmethod

from myLyrics.src.models.search_result import SearchResult
from myLyrics.src.models.song_lyrics import SongLyrics


class LyricsRepository(ABC):

    @abstractmethod
    def construct_search_url(self, search_string) -> str:
        pass

    @abstractmethod
    def search_song_in_website(self, searched_song_string) -> SearchResult:
        """Return SearchResult Object"""
        pass

    @abstractmethod
    def get_lyrics_from_link(self, link) -> SongLyrics:
        """Return SongLyrics Object"""
        pass
