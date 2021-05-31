from __future__ import annotations

from typing import Optional

from flask import Response as FlaskResponse


class LyricsSearchApiResponse(dict):
    title: str = ""
    success: bool = True
    lyrics: str = ""

    def __init__(self, lyrics: Optional[str] = None, title: Optional[str] = None):
        super().__init__()
        if lyrics is None or title is None:
            self.success = False
            self.title = ""
            self.lyrics = ""
        elif lyrics is not None:
            self.success = True
            self.title = title
            self.lyrics = lyrics

    def toFlaskJsonResponse(self) -> FlaskResponse:
        return FlaskResponse(self, mimetype='application/json')

    @staticmethod
    def Error(exception: Optional[Exception] = None) -> LyricsSearchApiResponse:
        if exception is not None: print(exception)
        return LyricsSearchApiResponse(None)
