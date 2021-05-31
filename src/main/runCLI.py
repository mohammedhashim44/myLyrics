#! /usr/bin/python3
from src.main.lyrics import *

if __name__ == "__main__":
    running = True
    while running:
        searched_song = input(">> Enter a song name : ")
        if searched_song == "" or searched_song is None:
            print("Error : You must enter string ..")
            continue

        searched_song = searched_song.strip()
        print(">>> Connecting ...")

        result = findSongsByNameOrNone(searched_song)
        count = len(result.songs)
        if count > 0:
            print(">> This is what we found :\n")
            for i in range(count):
                song = result.songs[i]
                msg = '{0}: {1} - {2}'.format((i + 1), song.song_name, song.singer)
                print(msg)

            number = input(">> Choose number or -1 to exit : ")
            number = int(number)
            if number == -1:
                exit()
            if number > count:
                print(">> No such Number !! please read carefully .. \n")
                print("\n" * 20)
            else:
                print("\n\n" + "*" * 30)
                song = result.songs[number - 1]
                msg = '{0}: {1} - {2}'.format(number, song.song_name, song.singer)
                print(msg)
                print(">>> Connecting ...")

                song_lyrics = getLyricsOrNone(song.link)
                print(song_lyrics.lyrics)
        else:
            print(">> No songs found")
