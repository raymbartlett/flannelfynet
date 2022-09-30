# [flannelfy](https://flannelfy.net)


## Setup Tutorial
* Install the packages in requirements.txt
* Run get_scores.py to generate an up to date dict of scores from the 2020s
* Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
    * Add the Client ID and Client Secret to flannelfy_site.py
    * In the Spotify app settings, add "http://127.0.0.1:5000/access" to Redirect URIs and remember to save
* In the command line, run "export FLASK_APP=flannelfy_site.py"
    * You should now be able to run the app with "flask run"

## Future Plans
* EP support
* last.fm support (particularly the most listened to albums)
* Apple Music support

## Contributing
* If you're interested in contributing, make a pull request!

## Notes
* The general structure of flannelfy_site.py was borrowed heavily from another [project](https://github.com/AdrielGenao/spotify-website) by AdrielGenao on GitHub. Go check it out!
* Make sure to run get_scores.py if you want to update the scores dict
* There are a few places that could definitely be made more efficient, but due to either time constraints or having to abide by Spotify's quota extension requirements, I haven't gotten to them yet.
* The formatting looks worse than it does in the hosted environment and I am not sure why.
* If anything isn't clear, open an issue and I'll add comments and/or reformat it to make more sense! You can also reach me on [Twitter](https://twitter.com/raymbartlett)