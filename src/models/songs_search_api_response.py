from __future__ import annotations

from typing import List, Optional

from flask import Response as FlaskResponse

from src.models.song import Song


class SongsSearchApiResponse(dict):
    success: bool = True
    songs: List[Song] = []

    def __init__(self, songs: Optional[List[Song]] = None):
        super().__init__()
        if songs is None:
            self.success = False
        elif songs is not None:
            self.songs = songs

    def toFlaskJsonResponse(self) -> FlaskResponse:
        return FlaskResponse(self, mimetype='application/json')

    @staticmethod
    def Error(exception: Optional[Exception] = None) -> SongsSearchApiResponse:
        if exception is not None: print(exception)
        return SongsSearchApiResponse(None)
