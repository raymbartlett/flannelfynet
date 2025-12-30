"""Stores Spotify class."""
import spotipy

from scores import scores


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

        saved_albums = []
        # compile every album saved by user into list
        offset = 0
        while True:
            temp = self.sp.current_user_saved_albums(limit=50, offset=offset)['items']
            if len(temp) == 0:
                break
            offset += len(temp)
            saved_albums.extend(temp)

        # get total number of albums in library
        self.total_albums = len(saved_albums)

        for i in saved_albums:
            release_year = int((i['album']['release_date'])[0:4])
            link = i['album']['external_urls']['spotify']
            score = -1

            title = i['album']['name']
            artist = (' & '.join(artist['name'] for artist in i['album']['artists'])).lower()

            combined = artist + ' - ' + title

            if release_year >= 2010 and i['album']['album_type'] == 'album':
                # potentially has fantano score
                self.eligible_albums.append(list(link, score, combined))
