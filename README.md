<h1 align=center>Smergify</h1>

<p align=center>Shared Spotify playlists</p>


# Setup

* [Basic configuration for a new Raspbian installation on RaspberryPi](https://gist.github.com/LiliOlczak/2cb261a6f03f09fcf04d7090a691e30c)

* Install the required packages in [requirements.txt](requirements.txt)

```
pip install -r requirements.txt
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
