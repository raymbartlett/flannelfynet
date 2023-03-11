"""Stores Spotify class."""
import requests
import json

from helpers import remove_extras
from scores import titles_classics
from scores import titles_2010s
from scores import titles_manual
from scores_2020s import titles_2020s

API_KEY = ''


class LastFM:
    """Stores all user data for the home page."""
    total_albums = 0
    eligible_albums = []
    scored_albums = {}

    def __init__(self, username, duration, limit):
        """Authorize through Spotify."""
        self.username = username
        self.duration = duration
        self.limit = limit

    def get_eligible_albums(self):
        """Retrieve all albums saved by the user that potentially have a score."""
        self.eligible_albums = []
        x = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={self.username}&api_key={API_KEY}&period={self.duration}&limit={self.limit}&&format=json')
        saved_albums = json.loads(x.text)['topalbums']['album']

        self.total_albums = len(saved_albums)

        for album in saved_albums:
            title = str(album['name']).lower()
            artist = str(album['artist']['name']).lower()
            score = -1
            link = str(album['url'])

            self.eligible_albums.append(list((remove_extras(artist + ' - ' + title), score, link)))
        return

    def get_user_scores(self):
        """Assign scores to saved albums."""
        self.scored_albums = {}
        for eligible_album in self.eligible_albums:

            search = remove_extras(eligible_album[0])

            all_titles = {**titles_classics, **titles_2010s, **titles_2020s, **titles_manual}

            if search in all_titles:
                self.scored_albums[search] = (all_titles[search], eligible_album[2])
                eligible_album[1] = all_titles[search]
        return
