"""Stores Fantano class."""
import spotipy
import re

from scores_2010s import titles_2010s
from scores_2020s import titles_2020s


class Fantano:
    """Stores all relevant user data for the home page."""

    total_albums = 0
    eligible_albums = []
    scored_albums = {}

    def __init__(self, token):
        """Authorize through Spotify."""
        self.sp = spotipy.Spotify(auth=token)

    def check_classic_album(self, artist, title, score, link):
        """Check to see if album is a 10 from a previous decade, making it technically ineligible, so must be caught here."""
        # 10s from the 2000s
        if (artist + ' - ' + title == "Daft Punk - Discovery"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "System Of A Down - Toxicity"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Björk - Vespertine"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Godspeed You! Black Emperor - Lift Your Skinny Fists Like Antennas to Heaven"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Madvillain & Madlib & MF DOOM - Madvillainy"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        # 10s from the 1990s
        elif (artist + ' - ' + title == "Ms. Lauryn Hill - The Miseducation of Lauryn Hill"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Nirvana - Nevermind"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Nirvana - Nevermind (Deluxe Edition)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Nirvana - Nevermind (Remastered)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Nirvana - Nevermind (Super Deluxe Edition)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Nirvana - Nevermind (30th Anniversary Super Deluxe)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Neutral Milk Hotel - In the Aeroplane Over the Sea"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Wu-Tang Clan - Enter The Wu-Tang (36 Chambers)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Wu-Tang Clan - Enter The Wu-Tang (36 Chambers) [Expanded Edition]"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Depeche Mode - Violator (2006 Remaster)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        # 10s from the 1980s
        elif (artist + ' - ' + title == "Metallica - Master of Puppets (Remastered)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Metallica - Master of Puppets (Remastered Deluxe Box Set)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Public Enemy - It Takes A Nation Of Millions To Hold Us Back"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Public Enemy - It Takes A Nation Of Millions To Hold Us Back (Deluxe Edition)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Kate Bush - Hounds of Love (2018 Remaster)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Talking Heads - Remain in Light"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Talking Heads - Remain in Light (Deluxe Version)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Prince - Purple Rain"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        elif (artist + ' - ' + title == "Prince - Purple Rain (Deluxe Expanded Edition)"):
            self.eligible_albums.append(list((artist + ' - ' + title, score, link)))

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
            artist = ' & '.join(artist['name'] for artist in i['album']['artists'])
            score = -1
            link = i['album']['external_urls']['spotify']

            if (release_year >= 2010) and (i['album']['album_type'] == 'album'):
                # potentially has Fantano score
                self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
            else:
                self.check_classic_album(artist, title, score, link)

        return

    def get_user_scores(self):
        """Assign scores to albums saved by the user."""
        self.scored_albums = {}
        for i in self.eligible_albums:

            search = self.remove_extras(i[0].lower())
            search_group_first = ' '
            search_group_last = ' '
            if ' & ' in search:
                search_group_last = search.split(' & ')[-1].split(' - ')[0] + ' - ' + search.split(' - ', 1)[1]
                search_group_first = search.split(' & ')[0] + ' - ' + search.split(' - ', 1)[1]

            if search in titles_2010s:
                self.scored_albums[self.remove_extras(i[0])] = (titles_2010s[search], i[2])
                i[1] = titles_2010s[search]
            elif search_group_first in titles_2010s:
                self.scored_albums[self.remove_extras(i[0])] = (titles_2010s[search_group_first], i[2])
                i[1] = titles_2010s[search_group_first]
            elif search_group_last in titles_2010s:
                self.scored_albums[self.remove_extras(i[0])] = (titles_2010s[search_group_last], i[2])
                i[1] = titles_2010s[search_group_last]
            elif search in titles_2020s:
                self.scored_albums[self.remove_extras(i[0])] = (titles_2020s[search], i[2])
                i[1] = titles_2020s[search]
            elif search_group_first in titles_2020s:
                self.scored_albums[self.remove_extras(i[0])] = (titles_2020s[search_group_first], i[2])
                i[1] = titles_2020s[search_group_first]
            elif search_group_last in titles_2020s:
                self.scored_albums[self.remove_extras(i[0])] = (titles_2020s[search_group_last], i[2])
                i[1] = titles_2020s[search_group_last]

        return

    def remove_extras(self, album):
        """Remove flair from album titles in order to match with score lists and remove duplicates."""
        remove_flair = re.compile(re.escape(' (remastered)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (remaster)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (deluxe)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (deluxe edition)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (deluxe expanded edition)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (deluxe version)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (extended)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (extended edition)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (expanded edition)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' [expanded edition]'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (special version)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (special edition)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (bonus track version)'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' [platinum edition]'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape('edición especial'), re.IGNORECASE)
        album = remove_flair.sub('', album)

        # specific to particular albums

        remove_flair = re.compile(re.escape(' (the platinum pleasure edition)'), re.IGNORECASE)  # Jessie Ware - What's Your Pleasure?
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (30th anniversary super deluxe)'), re.IGNORECASE)  # Nirvana - Nevermind
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (2006 remaster)'), re.IGNORECASE)  # Depeche Mode - Violator
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (remastered deluxe box set)'), re.IGNORECASE)  # Metallica - Master of Puppets
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (2018 remaster)'), re.IGNORECASE)  # Kate Bush - Hounds of Love
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (mirror to mirror)'), re.IGNORECASE)  # Car Seat Headrest - Twin Fantasy
        album = remove_flair.sub('', album)

        remove_flair = re.compile(re.escape(' (original)'), re.IGNORECASE)  # The Weeknd - House Of Balloons
        album = remove_flair.sub('', album)

        return album
