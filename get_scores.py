"""A scheduled task that runs every night, overwriting scores_2020s.py with updated scores."""
import os

from urllib.request import Request, urlopen
import html
import re
from bs4 import BeautifulSoup


title_scores = {
    "ichiko aoba - windswept adan": 9,
    "haru nemuri - shunka ryougen": 7,
    "tricot - 上出来": 7,
    "xibalba - años en infierno": 6,
    "floating points & pharoah sanders - promises": 9,
    "denzel curry - melt my eyez see your future": 8,
    "cordae - from a birds eye view": 6,
    "future - i never liked you": 5,
    "jane remover - frailty": 7,
    "blu & exile & blu & exile - miles": 9,
    "danger mouse & black thought - cheat codes": 8,
    "ethel cain - preacher’s daughter": 6,
    "nas - king's disease ii": 8,
    "death's dynamic shroud - faith in persona": 8,
    "chat pile - god's country": 8,
    # King Gizzard & The Lizard Wizard
    "king gizzard & the lizard wizard - k.g.": 6,
    "king gizzard & the lizard wizard - l.w.": 7,
    "king gizzard & the lizard wizard - butterfly 3000": 5,
    "king gizzard & the lizard wizard - omnium gatherum": 6,
    "king gizzard & the lizard wizard - ice, death, planets, lungs, mushrooms and lava": 7,
    "king gizzard & the lizard wizard - laminated denim": 8,
    "king gizzard & the lizard wizard - changes": 7,
}
file_path = "scores_2020s.py"


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
        results = soup.find(id="centerContent")
        results = results.find_all("div", class_="albumListRow")

        for album in results:
            temp_title = album.find_all('meta', attrs={'itemprop': 'name'})[0]
            title = html.unescape(str(temp_title).split('"')[1]).lower()
            title = title.replace('\u200b', '')  # remove zero width space
            temp_score = album.find_all("div", class_="scoreValue")[0]
            score = int(re.findall(r'\d+', str(temp_score))[0]) / 10
            title_scores[title] = int(score)

    if os.path.isfile(file_path):
        os.remove(file_path)
        print('deleted previous file')
    else:
        print('previous file does not exist')

    new_file = open("scores_2020s.py", "w", encoding="utf-8")
    new_file.write('titles_2020s = {')
    for i in title_scores:
        new_file.write("\n\t")
        new_file.write('"')
        new_file.write(i)
        new_file.write('": ')
        new_file.write(str(title_scores[i]))
        new_file.write(',')
    new_file.write('\n}')

    print('done')
    return


if __name__ == "__main__":
    get_scores_2020s()
