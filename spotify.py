"""Stores Spotify class."""
import spotipy

from scores import scores


class Spotify:
    """Stores all user data for the home page."""
    total_albums = 0
    saved_albums = {}

    def __init__(self, token):
        """Authorize through Spotify."""
        self.sp = spotipy.Spotify(auth=token)

    def get_saved_albums(self):
        """Retrieve all albums saved by the user that potentially have a score."""
        self.saved_albums = {}

        # compile every album saved by user into list
        offset = 0
        while True:
            temp = self.sp.current_user_saved_albums(limit=50, offset=offset)['items']
            if len(temp) == 0:
                break
            offset += len(temp)

            for i in temp:
                link = i['album']['external_urls']['spotify']
                title = i['album']['name'].lower()
                artist = (' & '.join(artist['name'] for artist in i['album']['artists'])).lower()

                combined = artist + ' - ' + title
                self.saved_albums[link] = {'score': -1, 'title': combined}

        # get total number of albums in library
        self.total_albums = len(self.saved_albums)