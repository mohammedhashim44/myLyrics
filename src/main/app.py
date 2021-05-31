import json

from flask import Flask, render_template, request, Response

from src.main.lyrics import *
from src.models.lyrics_search_api_response import LyricsSearchApiResponse
from src.models.songs_search_api_response import SongsSearchApiResponse
from src.utils.flast_templateing_utils import renderConnectionErrorTemplate, renderEmptySearchErrorTemplate, \
    renderEmptyLinkErrorTemplate, renderWrongURLErrorTemplate, renderSearchTemplate, renderApiErrorTemplate, \
    renderLyricsTemplate
from src.utils.string_utils import isEmptyOrNone, isBlankOrNone

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/search_page', methods=['GET'])
def search_page():
    songName = request.args.get('song')
    if isBlankOrNone(songName):
        return renderEmptySearchErrorTemplate()
    try:
        songsOrNone = findSongsByNameOrNone(songName)
        if songsOrNone is None: return renderApiErrorTemplate()
        return renderSearchTemplate(searchQuery=songName, songs=songsOrNone)
    except Exception as e:
        return renderConnectionErrorTemplate(e)


@app.route('/get_song_from_link', methods=['GET'])
def get_song_from_link():
    link = request.args.get('link')
    if isEmptyOrNone(link): return renderEmptyLinkErrorTemplate()

    try:
        lyricsOrNone = getLyricsOrNone(link)
        if lyricsOrNone is None: return renderApiErrorTemplate()
        return renderLyricsTemplate(songName=lyricsOrNone.title, lyrics=lyricsOrNone.lyrics)
    except Exception as e:
        return renderConnectionErrorTemplate(e)


@app.route('/api/search_api', methods=['GET'])
def search_api():
    songName = request.args.get('song')
    if isBlankOrNone(songName):
        return SongsSearchApiResponse.Error().toFlaskJsonResponse()

    try:
        songsOrNone = findSongsByNameOrNone(songName)
        if songsOrNone is None: return renderApiErrorTemplate()
        return SongsSearchApiResponse(songsOrNone).toFlaskJsonResponse()

    except Exception as e:
        return SongsSearchApiResponse.Error(e).toFlaskJsonResponse()


@app.route('/api/get_song_from_link', methods=['GET'])
def get_song_from_link_api():
    link = request.args.get('link')

    if isBlankOrNone(link):
        return LyricsSearchApiResponse.Error().toFlaskJsonResponse()

    try:
        lyricsOrNone = getLyricsOrNone(link)
        if lyricsOrNone is None: return renderApiErrorTemplate()
        # TODO: use LyricsSearchApiResponse(lyricsOrNone.lyrics, lyricsOrNone.title).toFlaskJsonResponse()
        return Response(json.dumps(LyricsSearchApiResponse(lyricsOrNone.lyrics, lyricsOrNone.title).__dict__),
                        mimetype="application/json")
    except Exception as e:
        return LyricsSearchApiResponse.Error(e).toFlaskJsonResponse()


@app.errorhandler(404)
def page_not_found(e):
    return renderWrongURLErrorTemplate()
