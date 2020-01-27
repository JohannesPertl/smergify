<h1 align=center>Smergify</h1>

<p align=center>Shared Spotify playlists</p>

# TO-DO
## Raspberry PI
- [x] SSH Key
- [x] DuckDNS

## Cronjobs
- [ ] Every minute: [Monitoring](#monitoring)
- [ ] Every week: [Smergify without arguments](#smergify)

## Client
Python
- [ ] Config file for SSH Credentials
    - [ ] Username (pi)
    - [ ] IP
    - [ ] Password or SSH Key
- [ ] Get *user_name* and *user_group* (sys.argv or direct user input)
- [ ] Create .cache file with Spotipy's ```util.prompt_for_user_token```
- [ ] Copy .cache file to folder named like *user_group* on RaspberryPi via SCP
 
## Monitoring
Bash
- [ ] Check for changes in *user_group* folders
    - [ ] If there are changes, call ```python3 smergify.py <user_group>```
    
Resources:  
https://stackoverflow.com/questions/35240994/how-to-run-inotifywait-continuously-and-run-it-as-a-cron-or-deamon
 
## Database
Python with Sqlite3
Create database functions necessary for [Smergify](#smergify)
- [x] insert artists
- [x] insert user_has_artist
- [ ] insert group
- [ ] insert group has user
- [ ] insert songs

 
## Smergify
Python
- [ ] Config.yaml
    - [ ] app_id
    - [ ] app_secret
    - [ ] scope
- [ ] Check if sys.argv is empty
    - [ ] If not: each argument is treated as one *user_group*
    - [ ] If empty: every group (gets called in weekly cronjob)
- [ ] Get users of every usergroup and authenticate them
    - [ ] Use Regex to read username from .cache file
    - [ ] Save users in DB
        - [ ] If already existing but new group: Change to new group
- [ ] Get artists from users via spotipy
    - [ ] Save artists in DB
- [ ] Get top songs from every artist
    - [ ] Save songs in DB
- [ ] Merge songs for every group
- [ ] Create Playlist for every group on Spotify (on App Account on/every User?)


# Setup

* Install my [fork of Spotipy](https://github.com/JohannesPertl/spotipy)

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
