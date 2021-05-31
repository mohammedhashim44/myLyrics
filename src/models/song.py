class Song(dict):
    def __init__(self, song_name, singer, link):
        super().__init__()
        self.song_name: str = song_name
        self.singer: str = singer
        self.link: str = link
