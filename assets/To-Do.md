# TO-DO
## Raspberry Pi
- [x] SSH Key
- [x] DuckDNS
- [x] Complete Setup as bash script

## Cronjobs
- [x] Every day: [Smergify without arguments](#smergify)

## Client
Python
- [x] Config file for SSH Credentials
    - [x] Username (pi)
    - [x] IP
    - [x] Password or SSH Key
- [x] Get SSH connection to RaspberryPi
- [x] Get *user_group* via input
- [x] Create folder named like *user_group* remotely on RaspberryPi via SSH
- [x] Get *user_name* for two users via input
   - [x] Check, if user is already existing
- [x] Create .cache file with Spotipy's ```util.prompt_for_user_token```
- [x] Copy .cache file to folder named like *user_group*
- [x] Execute [smergify.py](server/smergify.py) with *user_group* as command line argument
- [x] Delete .cache files locally

## Webserver for redirect URL of Client Authentication
- [x] Install Apache
- [x] Create simple index.html with info on how to proceed

 
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
- [x] get matching artists/songs group

 
## Smergify
Python
- [x] Config.yaml
    - [x] app_id
    - [x] app_secret
    - [x] redirect_uri
- [x] Check if sys.argv is empty
    - [x] If not: treat arguments like group_names and only use those
    - [x] If empty: every group (gets called in weekly cronjob)
- [x] Get users of every usergroup and authenticate them
    - [x] Use Regex to read username from .cache file
    - [x] Save users in DB
- [x] Get artists from users via spotipy
    - [x] Save artists in DB
- [x] Get top songs from every artist
    - [x] Save songs in DB
- [x] Merge songs for every group
- [x] Create Playlist for every group on Spotify (on every useraccount)
- [x] Error Logging
- [x] Playlist creation monitoring
