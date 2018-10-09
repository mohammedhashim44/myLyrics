# import statements

import requests
import re
from bs4 import BeautifulSoup


class Lyrics():

    def __init__(self):

        # The lyrics website
        self.website = "https://www.lyricsmode.com/"
        self.website_search = "https://www.lyricsmode.com/search.php?search="
        self.songsTable = []
        self.lyricsHtml = ""
        self.lyrics = ""
        self.song = ""
        self.id = -1
        self.error = {}
        self.error_found = 0

    # return page content html or -1 of error
    def getPageContent(self, page):
        # Start requsest
        r = requests.get(page)

        # Check status code
        if r.status_code == requests.codes.ok:
            # return content
            return r.text

        else:
            self.error = {'first':'Connection error' , 'second':'.. try again'}
            return -1


    def getSongsTable(self, song_name):
        self.song = song_name
        search_url = self.website_search + song_name


        searchPage = self.getPageContent(search_url)
        if searchPage == -1:
            
            return

        # cut table from the page
        begin = searchPage.find('<div class="lm-section-list">')
        end = searchPage.find('TODO inline styles')

        songs = []
        # check begin and end
        if begin != -1 and end != -1:

            lyrics = searchPage[begin : end ]
            soup = BeautifulSoup(lyrics , 'html.parser')
            

            tr = soup.findAll("div", {"class": "lm-list__row"})
            for i in range(len(tr) ):

                soup2 = BeautifulSoup(str(tr[i]) , 'html.parser')
                a = soup2.find_all('a')
                index = 0
                dic = {}
                arr = ['Singer' , 'Song' , 'link']
                for k in range(len(a)):
                    dic[arr[k]] = a[k].text
                    if index == 0 :
                        index = 1
                    else:
                        dic[arr[2]] = a[k].attrs['href'] 

                songs.append(dic)

            if len(songs) == 0 :
                self.error =  {'first':'No songs found' , 'second':'.. try again'}

            else:
                for i in range(len(songs)):
                    if songs[i]['link'][0] == '/':
                        songs[i]['link'] = songs[i]['link'][1:]
        else:
            
            begin = searchPage.find('<!--NO_SEARCH-->')
            end = searchPage.find('<!--/NO_SEARCH-->')
            if begin != -1 and end != -1:
                self.error =  {'first':'No songs found' , 'second':'.. try again'}
            

        self.songsTable = songs
        return                


    def getLyricsPageContent(self, song_id):
        # id is the number of the song in the table

        if song_id > len(self.songsTable) :
            print("No id match")
            return
        self.id = song_id

        if self.songsTable[song_id]['link'][0] == '/':
            self.songsTable[song_id]['link'] = self.songsTable[song_id ]['link'][1:]
            


        lyrics_link = self.website + self.songsTable[song_id]['link']
    
    
        lyrics_request = requests.get(lyrics_link)

        if lyrics_request.status_code == requests.codes.ok:
            
            html = lyrics_request.text
            soup = BeautifulSoup(html , 'html.parser')
            p = soup.find('p' , id="lyrics_text")

            self.lyricsHtml = str(p).strip()
            return 

        else:
            print(lyrics_request.status_code)
            print(lyrics_link)
            print("Error connection")
            return 

    def getFinalLyrics(self):
        text = self.lyricsHtml
        if text == -1 or text == "":
            return

        # get <p> element in source code
       
        lyrics = ""

        soup = BeautifulSoup(text , 'html.parser')
        p = soup.find('p' , id="lyrics_text")

        self.lyrics = p.text

        
    def run(self):
       
        running = True 
        while running :

            songName = input(">> Enter a song name : ") 
            if songName == "" or songName == None:
                print("Error : You must enter string ..")
                continue
            print(">> Connecting ... ")
            self.getSongsTable(songName)


            if len(self.songsTable) > 0 :
                print(">> This all we found :\n\n")
                k = 0
                for i in self.songsTable :
                    k += 1
                    print(" No."+str(k)+" || Singer : " + i['Singer']
                             + " || Song : " + i['Song'])
                number = input(">> Choose number or -1 to exit : ")
                number = int(number)
                if number == -1:
                    exit() 
                if number > len(self.songsTable) :
                    print(">> No such Number !! please read carefully .. \n")
                    print("\n"*20)
                else:
                    print("\n\n" + "*"*10)

                    print(" No."+str(number)+" || Singer : " + self.songsTable[number - 1]['Singer']
                             + " || Song : " + self.songsTable[number - 1]['Song'])


                    self.getLyricsPageContent(number-1)
                    self.getFinalLyrics()

                    print("\n\n" + "*"*10)

                    print(self.lyrics) 

                    print("\n\n" + "*"*10)
            else:
                print(">> No songs found")
