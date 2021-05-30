class Song:
    def __init__(self, song_name, singer, link):
        self.song_name = song_name
        self.singer = singer
        self.link = link

    def to_dict(self):
        return {
            "song_name": self.song_name,
            "singer": self.singer,
            "link": self.link
        }
