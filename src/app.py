from flask import Flask, render_template, request, redirect, url_for
from lyrics import *
import json

app = Flask(__name__)


def is_empty_or_null(text):
    if text == "" or text is None:
        return True
    return False


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/search_page', methods=['GET'])
def search_page():
    song = request.args.get('song')
    if is_empty_or_null(song):
        err = {'first': 'Empty search', 'second': '..try again.'}
        return render_template('index.html', error=err)
    try:
        search_result = search_song_in_website(song)
        return render_template('search.html', songName=song, songsNumber=len(search_result.songs),
                               songs=search_result.songs)
    except Exception as e:
        print(e)
        error = {'first': 'Connection error', 'second': ' .. try again'}
        return render_template('index.html', error=error)


@app.route('/get_song_from_link', methods=['GET'])
def get_song_from_link():
    link = request.args.get('link')
    if is_empty_or_null(link):
        error = {'first': 'Empty Link', 'second': ' .. try again'}
        return render_template('index.html', error=error)

    try:
        link = link.strip()
        song_lyrics = get_lyrics_from_link(link)
        lyrics_text = song_lyrics.lyrics
        lyrics_text = lyrics_text.replace("\n", "<br/>")
        return render_template('lyricsPage.html', Song=song_lyrics.song_title, lyrics=lyrics_text)
    except Exception as e:
        print(e)
        err = {'first': 'Connection error', 'second': ' .. try again'}
        return render_template('index.html', error=err)


@app.route('/api/search_api', methods=['GET'])
def search_api():
    song = request.args.get('song')
    if song == "" or song is None:
        response = {"success": False}
        return response

    try:
        search_result = search_song_in_website(song)
        songs_dict = []
        for s in search_result.songs:
            songs_dict.append(s.to_dict())
        response = {
            "success": True,
            "songs": songs_dict
        }
        return json.dumps(response, indent=4)

    except Exception as e:
        response = {"success": False}
        return response


@app.route('/api/get_song_from_link', methods=['GET'])
def get_song_from_link_api():
    link = request.args.get('link')

    if link is None or link.strip() == "":
        response = {"success": False}
        return response

    try:
        song_lyrics = get_lyrics_from_link(link)
        lyrics = song_lyrics.lyrics
        song_title = song_lyrics.song_title

        response = {"success": True,"song_title":song_title, "lyrics": lyrics}
        return json.dumps(response, indent=4)
    except Exception as e:
        print(e)
        response = {"success": False}
        return response


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    err = {'first': 'Wrong URL', 'second': '..page not found.'}
    return render_template('index.html', error=err)
