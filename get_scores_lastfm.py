"""A scheduled task that runs every night, taking album titles from scores_2020s."""
import os

from scores_2020s import titles_2020s
from helpers import normalize_album as normalize

titles_only = {}
file_path = 'scores_2020s_lastfm.py'


def get_scores_lastfm():
    """Retrive 2020s scores (titles only) from scores_2020s."""
    for key in titles_2020s:
        title = key.split(' - ')[1]
        title = normalize(title, 'retrieval')
        titles_only[title] = titles_2020s[key]

    if os.path.isfile(file_path):
        os.remove(file_path)
        print('deleted previous file')
    else:
        print('previous file does not exist')

    new_file = open(file_path, "w", encoding="utf-8")
    new_file.write('titles_only_2020s = {')
    for key in titles_only:
        new_file.write("\n\t")
        new_file.write('"')
        new_file.write(key)
        new_file.write('": ')
        new_file.write(str(titles_only[key]))
        new_file.write(',')
    new_file.write('\n}')

    print('done')
    return


if __name__ == '__main__':
    get_scores_lastfm()
