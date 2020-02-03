<h1 align=center>Smergify</h1>

<p align=center>Shared Spotify playlists</p>


# Setup
## Spotify App

* Create your own Spotify App [here](https://developer.spotify.com/dashboard/login)
* Add a Redirect URI to your app, for example ```http://localhost:8080```
* You will need your app's Redirect URI, Client ID and Client Secret later for configuring the Server and Client


## Server
* Setup your own server, for example a [RaspberryPi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
* If you use a RaspberryPi, you can run our [configuration script](https://gist.github.com/LiliOlczak/2cb261a6f03f09fcf04d7090a691e30c) to automatically: 
  * Run a full upgrade
  * Install fail2ban to prevent brute-force attacks
  * Ask for password when using sudo
  * Enable SSH, change port and disable password login
  * Setup [DuckDNS](http://www.duckdns.org/about.jsp)

* Install the required packages in [requirements.txt](server/requirements.txt)

```shell script
pip3 install -r requirements.txt
```


* Open [config.yaml](server/config.yaml) and insert your configuration
  * Client ID, Client Secret and Redirect URI of your previously created App
  * The name of your [database file](server/data.db) (Default: data.db). The file should be in the same folder as your script
  * The name of your log-file which is saved in [logs](server/logs)
  * Minimum and desired playlist size (Amount of songs)

* Add a cronjob with ```crontab -e``` to automatically update all playlists for [groups](server/groups/) created with the client


```shell script
# Runs every Sunday at 00:00
0 0 * * 7 python3 smergify.py
```

## Client

* Install the required packages in [requirements.txt](client/requirements.txt)

```shell script
pip3 install -r requirements.txt
```

* Open [config.yaml](client/config.yaml) and insert your configuration
  
  * Client ID, Client Secret and Redirect URI of your previously created App
  * Username, hostname and port of your server
  * The path to your private key. Leave empty if not needed 
  * Your servers password. Leave empty if not needed
  * The absolute path to the [playlist groups](server/groups) on the server
  * The absolute path to the server [bash script](server/start_smergify_from_client.sh) starting the script


# Usage

Run ```python3 smergify.py``` on your client and follow the instructions.


## Contributors
* [Hacker Manuel](https://github.com/HackerManuel)
* [Olczak Liliana](https://github.com/LiliOlczack)
* [Pertl Johannes](https://github.com/JohannesPertl)
