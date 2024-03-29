"""A scheduled task that runs every night, overwriting scores_2020s.py with updated scores."""
import os

from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup
from helpers import normalize_title


title_scores = {}
FILE_PATH = 'scores_2020s.py'


def get_scores_2020s():
    """Retrieve 2020s scores from albumoftheyear."""
    base = 'https://www.albumoftheyear.org/ratings/57-the-needle-drop-highest-rated/2020s/{}'

    for page_num in range(0, 999):
        # narrow down to part of page with score information
        url = base.format(str(page_num + 1))
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')
        if 'n<title>The Best Albums of 2020 - Album of The Year</title>' in str(page):
            break
        results = soup.find(id='centerContent')
        results = results.find_all('div', class_='albumListRow')

        for album in results:
            temp_title = album.find_all('meta', attrs={'itemprop': 'name'})[0]
            title = str(temp_title.previous)
            title = normalize_title(title, 'retrieval')
            temp_score = album.find_all('div', class_='scoreValue')[0]
            score = int(re.findall(r'\d+', str(temp_score))[0]) / 10
            title_scores[title] = int(score)

    if os.path.isfile(FILE_PATH):
        os.remove(FILE_PATH)
        print('deleted previous file')
    else:
        print('previous file does not exist')

    new_file = open(FILE_PATH, 'w', encoding='utf-8')
    new_file.write('titles_2020s = {')
    for i in title_scores:
        new_file.write('\n\t')
        new_file.write('"')
        new_file.write(i)
        new_file.write('": ')
        new_file.write(str(title_scores[i]))
        new_file.write(',')
    new_file.write('\n}')

    print('done')


if __name__ == '__main__':
    get_scores_2020s()
