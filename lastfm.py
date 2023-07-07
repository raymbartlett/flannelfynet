"""Stores LastFM class."""
import json
import requests

from helpers import remove_extras, normalize_title


class LastFM:
    """Stores all user data for the home page."""
    total_albums = 0
    eligible_albums = []

    def __init__(self, api_key, username, duration, limit):
        """Authorize through lastfm."""
        self.api_key = api_key
        self.username = username
        self.duration = duration
        self.limit = limit

    def get_eligible_albums(self):
        """Retrieve all albums saved by the user that potentially have a score."""
        self.eligible_albums = []
        res = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={self.username}&api_key={self.api_key}&period={self.duration}&limit={self.limit}&&format=json', timeout=30)
        if res.status_code != 200:
            return
        saved_albums = json.loads(res.text)['topalbums']['album']

        self.total_albums = len(saved_albums)

        for album in saved_albums:
            title = str(album['name'])
            title = normalize_title(title, 'library')
            artist = str(album['artist']['name']).lower()
            score = -1
            link = str(album['url'])

            self.eligible_albums.append(list((remove_extras(artist + ' - ' + title), score, link)))
        return
