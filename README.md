<h1 align=center>Smergify</h1>

<p align=center>Shared Spotify playlists</p>


## Setup

* Install my fork of [Spotipy](https://github.com/JohannesPertl/spotipy)

```
pip install git+git://github.com/JohannesPertl/spotipy.git
```

* Run the script once to login with your user accounts

```
python3 smergify.py
```

* Add a cronjob to automatically create and update your shared playlists

```
# Runs every Sunday at 00:00
0 0 * * 7 python3 smergify.py
```


## Contributors
* [Hacker Manuel](https://github.com/HackerManuel)
* [Olczak Liliana](https://github.com/LiliOlczack)
* [Pertl Johannes](https://github.com/JohannesPertl)
