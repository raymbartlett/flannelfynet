"""A scheduled task that runs every night, overwriting scores_2020s.py with updated scores."""
import os

from urllib.request import Request, urlopen
import html
import re
from bs4 import BeautifulSoup


title_scores = {}
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

    # manual inputs (different on AOTY)
    title_scores["ichiko aoba - windswept adan"] = 9
    title_scores["haru nemuri - shunka ryougen"] = 7
    title_scores["tricot - 上出来"] = 7
    title_scores["xibalba - años en infierno"] = 6
    title_scores["floating points & pharoah sanders - promises"] = 9
    title_scores["denzel curry - melt my eyez see your future"] = 8
    title_scores["cordae - from a birds eye view"] = 6
    title_scores["future - i never liked you"] = 5
    title_scores["jane remover - frailty"] = 7
    title_scores["blu & exile & blu & exile - miles"] = 9
    title_scores["danger mouse & black thought - cheat codes"] = 8
    title_scores["ethel cain - preacher’s daughter"] = 6
    title_scores["nas - king's disease ii"] = 8
    title_scores["death's dynamic shroud - faith in persona"] = 8
    title_scores["chat pile - god's country"] = 8
    # King Gizzard & The Lizard Wizard
    title_scores["king gizzard & the lizard wizard - l.w."] = 7
    title_scores["king gizzard & the lizard wizard - omnium gatherum"] = 6
    title_scores["king gizzard & the lizard wizard - k.g."] = 6
    title_scores["king gizzard & the lizard wizard - butterfly 3000"] = 5

    if os.path.isfile(file_path):
        os.remove(file_path)
        print('deleted previous file')
    else:
        print('previous file does not exist')

    x = open("scores_2020s.py", "w", encoding="utf-8")
    x.write('titles_2020s = {')
    for i in title_scores:
        x.write("\n\t")
        x.write('"')
        x.write(i)
        x.write('": ')
        x.write(str(title_scores[i]))
        x.write(',')
    x.write('\n}')

    print('done')
    return


if __name__ == "__main__":
    get_scores_2020s()
