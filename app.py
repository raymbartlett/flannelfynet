"""All app routes and function calls."""
import base64
from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
import requests

from spotify import Spotify
from lastfm import LastFM
from helpers import *
from insta_card import generate_card

# scores for all scores tab
from scores import titles_classics, titles_2010s
from scores_2020s import titles_2020s

app = Flask(__name__)


s = requests.session()
CLIENT_ID = ""
CLIENT_SECRET = ""
LASTFM_KEY = ""


@app.route('/')
def login():
    """Open screen for user to log in. Redirect URI must match Spotify Developer Dashboard."""
    parameters = {'client_id': CLIENT_ID, 'response_type': 'code', 'redirect_uri': 'http://127.0.0.1:5000/spotify_access', 'scope': 'user-library-read', 'show_dialog': 'true'}
    base_url = 'https://accounts.spotify.com/authorize'
    r = s.get(base_url, params=parameters)
    return render_template('login.html', url=r.url)


@app.route('/spotify_results/<token>')
def spotify_results(token):
    """Open results page with Spotify data."""
    user = Spotify(token)
    user.get_eligible_albums()
    scored_albums, unscored_albums = get_user_scores(user.eligible_albums)

    if len(user.eligible_albums) < 1:
        return render_template('error.html', message="you have no eligible albums")

    if len(scored_albums) < 1:
        return render_template('error.html', message="you have no scored albums")

    general = str(user.total_albums) + ' albums in total | ' + str(len(user.eligible_albums)) + ' albums are eligible | ' + str(len(scored_albums)) + ' albums with a score'

    ordered_scores = by_score(scored_albums)
    alphabetical_scores = by_artist(ordered_scores)
    unscored_albums.sort(key=lambda x: (x[0].split(' - ')[0], x[0].split(' - ')[1]))

    score_data = get_score_data(scored_albums)
    labels = list(score_data.keys())
    values = list(score_data.values())
    average = get_average(score_data)
    score_path = get_score_path(average)

    encoded_img_data = generate_card(score_path, labels, values, general, average)
    return render_template('results.html',
        general=general,
        ordered_scores=ordered_scores,
        alphabetical_scores=alphabetical_scores,
        unscored=unscored_albums,
        labels=labels,
        values=values,
        average=average,
        score_path=score_path,
        img_data=encoded_img_data.decode('utf-8')
    )


@app.route('/lastfm_results', methods=['POST'])
def lastfm_results():
    """Open results page with last.fm data."""
    username = request.form['username']
    if username == '':
        return render_template('error.html', message="no username given")

    duration = request.form['duration']
    limit = 0
    duration_str = ''
    if duration == 'overall':
        duration_str = ' all time'
        limit = 100
    elif duration == '7day':
        duration_str = ' the last 7 days'
        limit = 10
    elif duration == '1month':
        duration_str = ' the last month'
        limit = 25
    elif duration == '3month':
        duration_str = ' the last 3 months'
        limit = 50
    elif duration == '6month':
        duration_str = ' the last 6 months'
        limit = 100
    elif duration == '12month':
        duration_str = ' the last year'
        limit = 100

    user = LastFM(LASTFM_KEY, username, duration, limit)
    user.get_eligible_albums()
    scored_albums, unscored_albums = get_user_scores(user.eligible_albums)

    if len(user.eligible_albums) < 1:
        return render_template('error.html', message="you have no eligible albums or your last.fm username is invalid")
    if len(scored_albums) < 1:
        return render_template('error.html', message="you have no scored albums")


    general = 'top ' + str(user.total_albums) + ' albums of ' + duration_str + ' | ' + str(len(scored_albums)) + ' with a score'

    ordered_scores = by_score(scored_albums)
    alphabetical_scores = by_artist(ordered_scores)
    unscored_albums.sort(key=lambda x: (x[0].split(' - ')[0], x[0].split(' - ')[1]))

    score_data = get_score_data(scored_albums)
    labels = list(score_data.keys())
    values = list(score_data.values())
    average = get_average(score_data)
    score_path = get_score_path(average)

    encoded_img_data = generate_card(score_path, labels, values, general, average)
    return render_template('results.html',
        general=general,
        ordered_scores=ordered_scores,
        alphabetical_scores=alphabetical_scores,
        unscored=unscored_albums,
        labels=labels,
        values=values,
        average=average,
        score_path=score_path,
        img_data=encoded_img_data.decode('utf-8')
    )


@app.route('/all_scores')
def all_scores_results():
    """Open results page with all scores."""
    all_scores = {**titles_classics, **titles_2010s, **titles_2020s}
    num_scores = len(all_scores)
    average = round((sum(all_scores.values())/len(all_scores)), 2)
    score_path = get_score_path(average)
    sorted_by_score = all_by_score(all_scores)
    sorted_by_artist = all_by_artist(all_scores)
    score_data = get_all_score_data(all_scores)
    labels = list(score_data.keys())
    values = list(score_data.values())
    return render_template(
        'all_scores.html',
        num_scores=num_scores,
        average=average,
        score_path=score_path,
        labels=labels,
        values=values,
        by_score=sorted_by_score,
        by_artist=sorted_by_artist
    )


@app.route('/spotify_access')
def spotify_access():
    """Endpoint for user login and going to home page, or error page if login fails."""
    code = request.args.get('code')  # Setup for retrieving authorization code/access token
    parameters = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'http://127.0.0.1:5000/spotify_access'}
    auth_header = base64.urlsafe_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode('ascii'))
    headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii'), 'Content-Type': 'application/x-www-form-urlencoded'}
    r = s.post('https://accounts.spotify.com/api/token', headers=headers, data=parameters)
    if 'error' in r.json():  # If user does not agree to terms
        return render_template('error.html', message='unable to sign in to spotify')  # Show error with login page, with button to return back to welcome/home page
    access = r.json()['access_token']  # Access token to be used to get info on Spotify user
    return redirect(url_for('spotify_results', token=access))


if __name__ == '__main__':
    app.run(debug=True)
