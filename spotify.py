"""Stores Spotify class."""
import spotipy

from helpers import remove_extras, normalize_title
from scores import titles_classics

from top_tracks import *
all_top_tracks = (
    top_tracks_2010 |
    top_tracks_2011 |
    top_tracks_2012 |
    top_tracks_2013 |
    top_tracks_2014 |
    top_tracks_2015 |
    top_tracks_2016 |
    top_tracks_2017 |
    top_tracks_2018 |
    top_tracks_2019 |
    top_tracks_2020 |
    top_tracks_2021 |
    top_tracks_2022 |
    top_tracks_2010s
)

from worst_tracks import *
all_worst_tracks = (
    worst_tracks_2016 |
    worst_tracks_2017 |
    worst_tracks_2018 |
    worst_tracks_2019 |
    worst_tracks_2020 |
    worst_tracks_2021 |
    worst_tracks_2022 |
    worst_tracks_2010s
)


class Library:
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
            batch = self.sp.current_user_saved_albums(limit=50, offset=offset)['items']
            if len(batch) == 0:
                break
            offset += len(batch)
            saved_albums.extend(batch)

        # get total number of albums in library
        self.total_albums = len(saved_albums)

        for i in saved_albums:
            try:
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
            except:
                continue


class Playlist:
    """Stores all user data for the home page."""
    top_tracks = []
    worst_tracks = []
    unranked_tracks = []
    total_tracks = 0

    def __init__(self, token):
        """Authorize through Spotify."""
        self.sp = spotipy.Spotify(auth=token)

    def get_playlist(self, title):
        """Retrieve all albums saved by the user that potentially have a score."""
        playlist_id = ''

        # compile every album saved by user into list
        offset = 0
        while True:
            if playlist_id != '':
                break
            temp = self.sp. current_user_playlists(limit=50, offset=0)['items']
            if len(temp) == 0:
                break
            for playlist in temp:
                if playlist['name'] == title:
                    playlist_id = playlist['id']
                    break
            offset += len(temp)

        tracks = self.sp.playlist(playlist_id, fields=None, market=None, additional_types=('track'))['tracks']['items']
        for i in tracks:
            try:
                self.total_tracks += 1
                track = i['track']
                release_year = int((track['album']['release_date'])[0:4])
                title = track['name']
                artist = (' & '.join(artist['name'] for artist in track['artists'])).lower()
                link = track['external_urls']['spotify']

                normalized = artist + ' - ' + normalize_title(title, 'retrieval')
                if release_year >= 2010:
                    # potentially has fantano score
                    if normalized in all_top_tracks:
                        self.top_tracks.append(list((normalized, link)))
                    elif normalized in all_worst_tracks:
                        self.worst_tracks.append(list((normalized, link)))
                    else:
                        self.unranked_tracks.append(list((normalized, link)))
            except:
                continue
