"""Stores Spotify class."""
import spotipy

from helpers import remove_extras, normalize_title
from scores import titles_classics


class Spotify:
    """Stores all user data for the home page."""
    total_albums = 0
    eligible_albums = []

    def __init__(self, token):
        """Authorize through Spotify."""
        self.sp = spotipy.Spotify(auth=token)

    def get_eligible_albums(self):
        """Retrieve all albums saved by the user that potentially have a score."""
        self.eligible_albums = []
        saved_albums = self.sp.current_user_saved_albums(limit=50, offset=0)['items']
        total = 10000  # spotify limit?

        # compile every album saved by user into list
        offset = int(50)
        while offset < (total + 50):
            saved_albums.extend(self.sp.current_user_saved_albums(limit=50, offset=offset)['items'])
            offset = offset + 50
            if len(saved_albums) < offset:
                break

        # get total number of albums in library
        self.total_albums = len(saved_albums)

        for i in saved_albums:
            release_year = int((i['album']['release_date'])[0:4])
            title = i['album']['name']
            title = normalize_title(title, 'library')
            artist = (' & '.join(artist['name'] for artist in i['album']['artists'])).lower()
            score = -1
            link = i['album']['external_urls']['spotify']

            normalized = remove_extras(artist + ' - ' + title)
            if release_year >= 2010 and i['album']['album_type'] == 'album':
                # potentially has fantano score
                self.eligible_albums.append(list((normalized, score, link)))
            elif normalized in titles_classics:
                # is a scored classic album
                self.eligible_albums.append(list((normalized, score, link)))
