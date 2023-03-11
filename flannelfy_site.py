"""All app routes and function calls."""
from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
import requests
import base64

from spotify import Spotify
from lastfm import LastFM
from helpers import *
from insta_card import generate_card

# scores for all scores tab
from scores import titles_classics
from scores import titles_2010s
from scores_2020s import titles_2020s

app = Flask(__name__)


s = requests.session()
clientID = ''
clientSecret = ''


@app.route('/')  # Home page and button for logging into Spotify
def login():
    """Open screen for user to log in. Redirect URI must match Spotify Developer Dashboard."""
    parameters = {'client_id': clientID, 'response_type': 'code', 'redirect_uri': 'http://127.0.0.1:5000/spotify_access', 'scope': 'user-library-read', 'show_dialog': 'true'}
    BaseURL = 'https://accounts.spotify.com/authorize'
    r = s.get(BaseURL, params=parameters)
    return render_template('login.html', url=r.url)


@app.route('/spotify_results/<token>')  # Page to view results
def spotify_results(token):
    """Open home page with user's results."""
    user = Spotify(token)
    user.get_eligible_albums()
    user.get_user_scores()

    if len(user.eligible_albums) < 1:
        return render_template('error.html', message="you have no eligible albums")

    if len(user.scored_albums) < 1:
        return render_template('error.html', message="you have no scored albums")

    general = str(user.total_albums) + ' albums in total | ' + str(len(user.eligible_albums)) + ' albums are eligible | ' + str(len(user.scored_albums)) + ' albums with a score'

    ordered_scores = by_score(user.scored_albums)
    alphabetical_scores = by_artist(ordered_scores)
    unscored = get_unscored_albums(user.eligible_albums)

    score_data = get_score_data(user.scored_albums)
    labels = list(score_data.keys())
    values = list(score_data.values())
    average = get_average(score_data)
    score_path = get_score_path(average)

    encoded_img_data = generate_card(score_path, labels, values, general, average)
    return render_template('results.html',
        general=general,
        ordered_scores=ordered_scores,
        alphabetical_scores=alphabetical_scores,
        unscored=unscored,
        labels=labels,
        values=values,
        average=average,
        score_path=score_path,
        img_data=encoded_img_data.decode('utf-8')
    )


@app.route('/lastfm_results', methods=['POST'])
def lastfm_results():
    username = request.form['username']
    duration = request.form['duration']
    user = LastFM(username, duration, 100)
    user.get_eligible_albums()
    user.get_user_scores()

    if len(user.eligible_albums) < 1:
        return render_template('error.html', message="you have no eligible albums")

    if len(user.scored_albums) < 1:
        return render_template('error.html', message="you have no scored albums")

    general = 'top ' + str(user.total_albums) + ' albums in the last ' + duration + ' | ' + str(len(user.scored_albums)) + ' have a score'

    ordered_scores = by_score(user.scored_albums)
    alphabetical_scores = by_artist(ordered_scores)
    unscored = get_unscored_albums(user.eligible_albums)

    score_data = get_score_data(user.scored_albums)
    labels = list(score_data.keys())
    values = list(score_data.values())
    average = get_average(score_data)
    score_path = get_score_path(average)

    encoded_img_data = generate_card(score_path, labels, values, general, average)
    return render_template('results.html',
        general=general,
        ordered_scores=ordered_scores,
        alphabetical_scores=alphabetical_scores,
        unscored=unscored,
        labels=labels,
        values=values,
        average=average,
        score_path=score_path,
        img_data=encoded_img_data.decode('utf-8')
    )


@app.route('/all_scores')
def all_scores():
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
    authHeader = base64.urlsafe_b64encode((clientID + ':' + clientSecret).encode('ascii'))
    headers = {'Authorization': 'Basic %s' % authHeader.decode('ascii'), 'Content-Type': 'application/x-www-form-urlencoded'}
    r = s.post('https://accounts.spotify.com/api/token', headers=headers, data=parameters)
    if 'error' in r.json():  # If user does not agree to terms
        return render_template('error.html', message='unable to sign in to spotify')  # Show error with login page, with button to return back to welcome/home page
    access = r.json()['access_token']  # Access token to be used to get info on Spotify user
    return redirect(url_for('spotify_results', token=access))


if __name__ == '__main__':
    app.run(debug=True)
