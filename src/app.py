from flask import Flask, render_template, request , redirect , url_for
from lyrics import *

app = Flask(__name__)

@app.route('/' ,methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/search',methods=['GET'])
def search():

    song = request.args.get('song')
    if song == "" or song is None:
        err = {'first':'Empty search' , 'second':'..try again.'}
        return render_template('index.html',error=err)

    try:
        search_result = search_song(song)
        return render_template(
            'search.html',
            songName=song,
            songsNumber=len(search_result.songs),
            songs = search_result.songs
        )
    except Exception as e:
        print(e)
        error = {'first':'Connection error' , 'second':' .. try again'}
        return render_template('index.html',error=error)


@app.route('/get',methods=['GET'])
def get():
    link = request.args.get('link')

    if link is None or link.strip() == "":
        error = {'first': 'Empty Link', 'second': ' .. try again'}
        return render_template('index.html', error=error)

    try:
        link = link.strip()
        song_lyrics = get_lyrics_from_link(link)
        lyrics_text = song_lyrics.lyrics
        lyrics_text = lyrics_text.replace("\n" , "<br/>")
        return render_template('lyricsPage.html',
                               Song=song_lyrics.song_title,
                               lyrics=lyrics_text)
    except Exception as e:
        print(e)
        err = {'first': 'Connection error', 'second': ' .. try again'}
        return render_template('index.html', error=err)


@app.errorhandler(404)
def page_not_found(e):
    err = {'first':'Wrong URL' , 'second':'..page not found.'}
    return render_template('index.html' , error=err)

