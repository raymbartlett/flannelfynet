"""Various helper functions, mostly dealing with user results."""
import json

from scores import scores


def by_score(albums):
    """Sort albums by score (descending)."""
    sorted_albums = sorted(
        albums.items(),
        key=lambda x: (-x[1][0], x[0].split(' - ')[0], x[0].split(' - ')[1])
    )
    return [[f"{score}/10: {title}", link] for title, (score, link) in sorted_albums]

def by_artist(albums):
    """Sort scored albums alphabetically by artist."""
    return sorted(albums, key=lambda x: x[0].split(': ')[1])

def by_artist_unscored(albums):
    """Sort unscored albums alphabetically by title."""
    return [[title, link] for title, link in sorted(albums.items())]


def get_score_data(albums):
    """Return data for bar chart of scores distribution."""
    data = {f'{i}s': 0 for i in range(11)}
    
    for album in albums.values():
        score = album[0]
        if 0 <= score <= 10:
            data[f'{score}s'] += 1
    
    return data


def get_average(score_data):
    """Return average score."""
    user_sum = sum(int(key[:-1]) * count for key, count in score_data.items())
    total = sum(score_data.values())
    return round(user_sum / total, 2)


def get_score_path(average):
    """Return the appropriate score png based on average score."""
    if average >= 10:
        return '10.png'
    
    base_score = int(average)
    fractional_part = average - base_score
    
    tier = 'light' if fractional_part < 0.33 else 'decent' if fractional_part < 0.66 else 'strong'
    
    return f'{tier}{base_score}.png'


def get_user_scores(saved_albums):
    """Assign scores to saved albums."""
    scored_albums = {}
    unscored_albums = {}

    for key in saved_albums:
        if key in scores:
            scored_albums[saved_albums[key]['title']] = (scores[key]['score'], key)
        else:
            unscored_albums[saved_albums[key]['title']] = key

    return scored_albums, unscored_albums
