from flask import Flask, render_template, request , redirect , url_for 
from getSongs import Lyrics

lyrics = Lyrics()

app = Flask(__name__)

songs = {}

@app.route('/' ,methods=['GET']) 
def home():
    lyrics.error = {}
    return render_template('index.html')


@app.route('/search',methods=['GET'])
def search():

    song = request.args.get('song')
    if song == "" or song == None:
        err = {'first':'Empty search' , 'second':'..try again.'}
        return render_template('index.html',error=err)

    try:
        lyrics.error = {}
        lyrics.getSongsTable(song)
        if len(lyrics.error) != 0 :
            return render_template('index.html',error=lyrics.error)
        
        global songs
        songs = lyrics.songsTable 
        number_of_songs = len(songs) 

        
        for index in range(len(songs)):
            songs[index]['index'] = "get/" + str(index) 
        return render_template('search.html' ,
                                    songName=lyrics.song ,
                                    songsNumber=number_of_songs,
                                    songs=songs)
        
    
    except:
        error = {'first':'Connection error' , 'second':' .. try again'}
        return render_template('index.html',error=error)


@app.route('/get/<int:index>',methods=['GET'])
def get(index):
    try:
        if len(lyrics.songsTable) == 0 :
            err = {'first':'Empty search' , 'second':'..try again.'}
            return render_template('index.html',error=err)

        if index != -1 and index != None and index != "":
            lyrics.getLyricsPageContent(index)
            lyrics.getFinalLyrics() 
            string = lyrics.lyrics
            string = string.replace("\n" , "<br/>").replace("[" , "<hr/>[")
            global songs
        
            return render_template('lyricsPage.html' ,
                                Band=songs[lyrics.id ]['Singer'] ,
                                Song=songs[lyrics.id ]['Song'],
                                lyrics=string)
    except:

        err = {'first':'Connection error' , 'second':' .. try again'}
        return render_template('index.html',error=err)

@app.errorhandler(404)
def page_not_found(e):
    err = {'first':'Wrong URL' , 'second':'..page not found.'}
    return render_template('index.html' , error=err)

