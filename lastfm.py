"""Stores Spotify class."""
import requests
import json

from scores_lastfm import titles_only
from scores_2020s_lastfm import titles_only_2020s
from helpers import normalize_album as normalize
from helpers import remove_extras


class LastFM:
    """Stores all user data for the home page."""
    total_albums = 0
    eligible_albums = []
    scored_albums = {}

    def __init__(self, api_key, username, duration, limit):
        """Authorize through Spotify."""
        self.api_key = api_key
        self.username = username
        self.duration = duration
        self.limit = limit

    def get_eligible_albums(self):
        """Retrieve all albums saved by the user that potentially have a score."""
        self.eligible_albums = []
        x = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={self.username}&api_key={self.api_key}&period={self.duration}&limit={self.limit}&&format=json')
        if x.status_code != 200:
            return
        saved_albums = json.loads(x.text)['topalbums']['album']

        self.total_albums = len(saved_albums)

        for album in saved_albums:
            title = str(album['name'])
            title = normalize(title, 'library')
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
            title = search.split(' - ')[1]
            all_titles = {**titles_only, **titles_only_2020s}

            if title in all_titles:
                self.scored_albums[search] = (all_titles[title], eligible_album[2])
                eligible_album[1] = all_titles[title]
        return
