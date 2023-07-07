"""Various helper functions, mostly dealing with user results."""
import Levenshtein
from scores import titles_classics, titles_2010s, titles_manual
from scores_2020s import titles_2020s

THRESHOLD = 0.5


def by_score(albums):
    """Sort albums by score (descending)."""
    temp = []
    output = []

    for i in albums:
        temp.append((i, albums[i][0], albums[i][1]))

    temp.sort(key=lambda x: (-x[1], x[0].split(' - ')[0], x[0].split(' - ')[1]))
    for i in temp:
        output.append([(str(i[1]) + '/10: ' + i[0]), i[2]])
    return output


def by_artist(albums):
    """Sort albums alphabetically by artist."""
    output = albums.copy()
    output.sort(key=lambda x: x[0].split(': ')[1])
    return output


def all_by_score(albums):
    """Sort all albums by score."""
    temp = sorted(albums.items(), key=lambda x: (-x[1], x[0]))
    output = []
    for i in temp:
        output.append([str(i[1]) + '/10: ' + i[0]])
    return output


def all_by_artist(albums):
    """Sort all albums by artist."""
    temp = sorted(albums.items(), key=lambda x: (x[0].split(' - ')[0], -x[1], x[0].split(' - ')[1]))
    output = []
    for i in temp:
        output.append([str(i[1]) + '/10: ' + i[0]])
    return output


def get_score_data(albums):
    """Return data for bar chart of scores distribution."""
    data = {
        '10s': 0,
        '9s': 0,
        '8s': 0,
        '7s': 0,
        '6s': 0,
        '5s': 0,
        '4s': 0,
        '3s': 0,
        '2s': 0,
        '1s': 0,
        '0s': 0,
    }

    for i in albums:
        if albums[i][0] == 10:
            data['10s'] += 1
        elif albums[i][0] == 9:
            data['9s'] += 1
        elif albums[i][0] == 8:
            data['8s'] += 1
        elif albums[i][0] == 7:
            data['7s'] += 1
        elif albums[i][0] == 6:
            data['6s'] += 1
        elif albums[i][0] == 5:
            data['5s'] += 1
        elif albums[i][0] == 4:
            data['4s'] += 1
        elif albums[i][0] == 3:
            data['3s'] += 1
        elif albums[i][0] == 2:
            data['2s'] += 1
        elif albums[i][0] == 1:
            data['1s'] += 1
        elif albums[i][0] == 0:
            data['0s'] += 1

    return data


def get_all_score_data(albums):
    """Return data for bar chart of scores distribution."""
    data = {
        '10s': 0,
        '9s': 0,
        '8s': 0,
        '7s': 0,
        '6s': 0,
        '5s': 0,
        '4s': 0,
        '3s': 0,
        '2s': 0,
        '1s': 0,
        '0s': 0,
    }
    for value in albums.values():
        if value == 10:
            data['10s'] += 1
        elif value == 9:
            data['9s'] += 1
        elif value == 8:
            data['8s'] += 1
        elif value == 7:
            data['7s'] += 1
        elif value == 6:
            data['6s'] += 1
        elif value == 5:
            data['5s'] += 1
        elif value == 4:
            data['4s'] += 1
        elif value == 3:
            data['3s'] += 1
        elif value == 2:
            data['2s'] += 1
        elif value == 1:
            data['1s'] += 1
        elif value == 0:
            data['0s'] += 1

    return data


def get_average(score_data):
    """Return average score."""
    user_sum = score_data['10s'] * 10
    user_sum += score_data['9s'] * 9
    user_sum += score_data['8s'] * 8
    user_sum += score_data['7s'] * 7
    user_sum += score_data['6s'] * 6
    user_sum += score_data['5s'] * 5
    user_sum += score_data['4s'] * 4
    user_sum += score_data['3s'] * 3
    user_sum += score_data['2s'] * 2
    user_sum += score_data['1s'] * 1
    user_sum += score_data['0s'] * 0

    total = 0
    for value in score_data.values():
        total += value

    return round((user_sum / total), 2)


def get_score_path(average):
    """Return the appropriate score png based on average score."""
    image_map = {
        (0, 0.33): 'light0.png',
        (0.33, 0.66): 'decent0.png',
        (0.66, 1): 'strong0.png',
        (1, 1.33): 'light1.png',
        (1.33, 1.66): 'decent1.png',
        (1.66, 2): 'strong1.png',
        (2, 2.33): 'light2.png',
        (2.33, 2.66): 'decent2.png',
        (2.66, 3): 'strong2.png',
        (3, 3.33): 'light3.png',
        (3.33, 3.66): 'decent3.png',
        (3.66, 4): 'strong3.png',
        (4, 4.33): 'light4.png',
        (4.33, 4.66): 'decent4.png',
        (4.66, 5): 'strong4.png',
        (5, 5.33): 'light5.png',
        (5.33, 5.66): 'decent5.png',
        (5.66, 6): 'strong5.png',
        (6, 6.33): 'light6.png',
        (6.33, 6.66): 'decent6.png',
        (6.66, 7): 'strong6.png',
        (7, 7.33): 'light7.png',
        (7.33, 7.66): 'decent7.png',
        (7.66, 8): 'strong7.png',
        (8, 8.33): 'light8.png',
        (8.33, 8.66): 'decent8.png',
        (8.66, 9): 'strong8.png',
        (9, 9.33): 'light9.png',
        (9.33, 9.66): 'decent9.png',
        (9.66, 10): 'strong9.png',
        (10, float('inf')): '10.png'
    }

    for key, value in image_map.items():
        lower_bound, upper_bound = key
        if lower_bound <= average < upper_bound:
            return value
    return 'light0.png'


def normalize_title(title, context):
    """Return normalized album artist - title."""
    title = title.lower()
    title = title.replace('\u200b', '')  # remove zero width space
    if context == 'retrieval':
        title = title.replace('"', '\\"')  # allow for double quotes
    title = title.replace('’', "'")  # normalize apostrophes
    title = title.replace('king gizzard and', 'king gizzard &')
    return title


def remove_extras(album):
    """Return album title without special edition flairs."""
    flairs = [
        "edition",
        "version",
        "deluxe",
        "special",
        "expanded",
        "extended",
        "remaster",
        "remastered",
        "remix",
        "edición",
        "anniversary",
        "original",  # The Weeknd - House Of Balloons
    ]
    parens = album[album.find('('):album.find(')')+1]
    brackets = album[album.find('['):album.find(']')+1]
    for flair in flairs:
        if parens.find(flair) != -1 and parens.find("soundtrack") == -1:
            return album.replace(parens, '').strip()
        if brackets.find(flair) != -1 and brackets.find("soundtrack") == -1:
            return album.replace(brackets, '').strip()
    album = album.rstrip(' +')  # rosalía - motomami +
    return album


def normalized_distance(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    max_length = max(len(str1), len(str2))
    normalized_distance = distance / max_length
    return normalized_distance


def get_user_scores(eligible_albums):
    """Assign scores to saved albums."""
    scored_albums = {}
    unscored_albums = []
    all_titles = {**titles_classics, **titles_2010s, **titles_2020s, **titles_manual}

    for eligible_album in eligible_albums:
        search = remove_extras(eligible_album[0])
        if search in all_titles:
            # exact match
            scored_albums[search] = (all_titles[search], eligible_album[2])
        else:
            closest_key = None
            closest_distance = float('inf')

            search_artist = search.split(' - ')[0]
            for key in all_titles:
                if search.split(' - ')[1] != key.split(' - ')[1]:
                    # different titles
                    continue

                distance = normalized_distance(search_artist, key.split(' - ')[0])
                if distance < closest_distance:
                    closest_distance = distance
                    closest_key = key
            if closest_key is None:
                # no score
                unscored_albums.append((eligible_album[0], eligible_album[2]))
                continue

            key_artist = closest_key.split(' - ')[0]
            if closest_key not in scored_albums:
                if search_artist in key_artist or key_artist in search_artist:
                    # one artist field is substring of the other - almost certainly a match regardless of distance score
                    scored_albums[closest_key] = (all_titles[closest_key], eligible_album[2])
                elif closest_distance < THRESHOLD:
                    # good distance score
                    scored_albums[search] = (all_titles[closest_key], eligible_album[2])
                else:
                    # no score
                    unscored_albums.append((eligible_album[0], eligible_album[2]))

    return scored_albums, unscored_albums
