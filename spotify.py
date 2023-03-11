"""Stores Spotify class."""
import spotipy

from helpers import remove_extras
from scores import titles_classics
from scores import titles_2010s
from scores import titles_manual
from scores_2020s import titles_2020s


class Spotify:
    """Stores all user data for the home page."""
    total_albums = 0
    eligible_albums = []
    scored_albums = {}

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
            title = (i['album']['name']).lower()
            artist = (' & '.join(artist['name'] for artist in i['album']['artists'])).lower()
            score = -1
            link = i['album']['external_urls']['spotify']

            if (release_year >= 2010) and (i['album']['album_type'] == 'album'):
                # potentially has fantano score
                self.eligible_albums.append(list((remove_extras(artist + ' - ' + title), score, link)))
            elif (remove_extras(artist + ' - ' + title) in titles_classics):
                # is a scored classic album
                self.eligible_albums.append(list((remove_extras(artist + ' - ' + title), score, link)))
        return

    def get_user_scores(self):
        """Assign scores to saved albums."""
        self.scored_albums = {}
        for eligible_album in self.eligible_albums:

            search = remove_extras(eligible_album[0])
            search_group_first = ''
            search_group_last = ''
            if ' & ' in search.split(' - ')[0]:
                search_group_first = search.split(' - ')[0].split(' & ')[0] + ' - ' + search.split(' - ', 1)[1]
                search_group_last = search.split(' - ')[0].split(' & ')[-1] + ' - ' + search.split(' - ', 1)[1]

            all_titles = {**titles_classics, **titles_2010s, **titles_2020s, **titles_manual}

            if search in all_titles:
                self.scored_albums[search] = (all_titles[search], eligible_album[2])
                eligible_album[1] = all_titles[search]
            elif search_group_first in all_titles:
                self.scored_albums[search_group_first] = (all_titles[search_group_first], eligible_album[2])
                eligible_album[1] = all_titles[search_group_first]
            elif search_group_last in all_titles:
                self.scored_albums[search_group_last] = (all_titles[search_group_last], eligible_album[2])
                eligible_album[1] = all_titles[search_group_last]
        return
