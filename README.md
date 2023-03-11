# [flannelfy](https://flannelfy.net)


## Setup Tutorial
* Install the packages in requirements.txt
* Run get_scores.py to generate an up-to-date file of scores from the 2020s
* Run get_lastfm_scores_2020s.py to sync to up-to-date 2020s scores for the last.fm page
* Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
    * In the Spotify app settings, add "http://127.0.0.1:5000/spotify_access" to Redirect URIs and remember to save
    * Add the Client ID and Client Secret to flannelfy_site.py
* Create a project in the [last.fm API Page](https://www.last.fm/api)
    * Add the API Key to lastfm.py
* In the command line, run "export FLASK_APP=flannelfy_site.py"
    * You should now be able to run the app with "flask run"

## Notes
* The general structure of flannelfy_site.py was borrowed heavily from another [project](https://github.com/AdrielGenao/spotify-website) by AdrielGenao on GitHub. Go check it out!
* Make sure to run get_scores.py whenever you want to update scores_2020s.py to include new reviews.
* If you want to add features, feel free to make a PR. You can reach me on [Twitter](https://twitter.com/raymbartlett) to collaborate or ask questions.