#  Spotify Drive Backup (Automated Playlist)

This project is an automated Python script designed for those who lose internet connection on the road. The goal is to mirror the recent listening history for driving: it automatically fetches the songs recently listened to on Spotify Desktop and saves them into a single playlist ("Backup da Estrada"). Since the Spotify mobile app has this playlist marked for "Download", it always saves the tracks over home Wi-Fi, allowing offline listening while driving without using mobile data.

## How it works 
1. Connects to the **Spotify Web API** using the OAuth2 flow.
2. Fetches the *Recently Played* history (last 50 songs).
3. Evaluates the current backup playlist to prevent adding duplicate tracks.
4. Adds only the new songs smoothly and autonomously!

## Requirements
* Python 3
* Libraries: `spotipy` and `python-dotenv`

## Getting Started 

1. Install the dependencies:
   ```bash
   pip install spotipy python-dotenv
   ```
2. Create an App on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), set the Redirect URI to `http://127.0.0.1:8888/callback`, and whitelist your Spotify email in the "User Management" section.
3. Hide your local keys by renaming the `.env.example` file to `.env` and inserting your `Client ID` and `Client Secret` inside it.
4. Run the script once in your terminal for the initial browser authorization:
   ```bash
   python spotify_backup.py
   ```

* The script can be easily scheduled using the **Windows Task Scheduler** (or Cron jobs) to run in the background every day at dawn, requiring zero manual intervention since Spotipy handles token refreshment natively.*
