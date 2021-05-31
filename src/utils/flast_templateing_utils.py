from typing import Optional, List

from flask import render_template

from src.models.song import Song


class TemplateError:
    def __init__(self, first: str, second: str):
        self.first = first
        self.second = second

    def toJson(self) -> dict:
        return {"first": self.first, "second": self.second}


def _renderErrorTemplate(
        error: TemplateError,
        exception: Optional[Exception] = None
) -> str:
    if exception is not None: print(exception)
    return render_template("index.html", error=error.toJson())


def renderConnectionErrorTemplate(exception: Exception) -> str:
    return _renderErrorTemplate(
        TemplateError(
            "Connection error",
            " .. try again")
        , exception
    )


def renderEmptySearchErrorTemplate() -> str:
    return _renderErrorTemplate(
        TemplateError(
            "Empty search",
            " .. try again")
    )


def renderEmptyLinkErrorTemplate() -> str:
    return _renderErrorTemplate(
        TemplateError(
            "Empty Link",
            " .. try again")
    )


def renderWrongURLErrorTemplate() -> str:
    return _renderErrorTemplate(
        TemplateError(
            "Wrong URL",
            " .. page not found.")
    )


def renderApiErrorTemplate() -> str:
    return _renderErrorTemplate(
        TemplateError(
            "Api Error",
            ".. contact the developer.")
    )


def renderSearchTemplate(searchQuery: str, songs: List[Song]) -> str:
    return render_template('search.html', songName=searchQuery, songsNumber=len(songs),
                           songs=songs)


def renderLyricsTemplate(songName: str, lyrics: str) -> str:
    return render_template('lyricsPage.html', Song=songName, lyrics=lyrics)
