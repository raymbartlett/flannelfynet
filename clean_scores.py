"""A scheduled task that runs every night, overwriting scores_2020s.py with updated scores."""
import os
import json

link_scores = {}
FILE_PATH = 'scores.py'


def clean_scores():
    with open("scores.json", "r") as f:
        scores = json.load(f)

    for album in scores["albums"]:
        try:
            link_scores[album["media_links"]["Spotify"]] = {
                "score": int(album["score"]),
                "artist": album["artist_clean"],
                "album": album["album_clean"],
            }
        except:
            print(f'error occurred on album {album["artist_clean"]} - {album["album_clean"]}')
    
    if os.path.isfile(FILE_PATH):
        os.remove(FILE_PATH)
        print('deleted previous file')
    else:
        print('previous file does not exist')

    file = open(FILE_PATH, 'w', encoding='utf-8')
    file.write('scores = ' + json.dumps(link_scores, ensure_ascii=False, indent=1))

    print('done')


if __name__ == '__main__':
    clean_scores()
