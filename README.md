<h1 align=center>Smergify</h1>

<p align=center>Shared Spotify playlists</p>

# TO-DO
## Raspberry Pi
- [x] SSH Key
- [x] DuckDNS
- [ ] Complete Setup as bash script

## Cronjobs
- [ ] Every week: [Smergify without arguments](#smergify)

## Client
Python
- [x] Config file for SSH Credentials
    - [x] Username (pi)
    - [x] IP
    - [x] Password or SSH Key
- [ ] Get *user_name* and *user_group* (sys.argv or direct user input)
   - [ ] Check, if group is already full or user is already existing
- [ ] Create .cache file with Spotipy's ```util.prompt_for_user_token```
- [ ] Copy .cache file to folder named like *user_group* on RaspberryPi via SCP
- [ ] Execute [smergify.py](server/smergify.py) with *user_group* as command line argument

## Webserver for redirect URL of Client Authentication
- [ ] Install Apache
- [ ] Create simple index.html with info on how to proceed

 
## Database
Python with Sqlite3
Create database functions necessary for [Smergify](#smergify)
- [x] insert artists
- [x] insert user_has_artist
- [x] insert group
- [x] insert group has user
- [x] insert songs
- [x] insert user
- [x] add try catch blocks - to prevent errors when referencing on e.g illegal users 
- [ ] get matching artists/songs group

 
## Smergify
Python
- [ ] Config.yaml
    - [ ] app_id
    - [ ] app_secret
    - [ ] scope
- [ ] Check if sys.argv is empty
    - [ ] If not: allow 1 argument (*user_group*)
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
- [ ] Error Logging


# Setup

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
