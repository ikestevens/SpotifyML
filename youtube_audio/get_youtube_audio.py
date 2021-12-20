import spotipy
import spotipy.util as util
import os
import re
import urllib.request
from pytube import YouTube

#Auth into Spotify api
secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
scope = 'playlist-modify-private playlist-modify-public user-top-read playlist-read-private user-library-read user-follow-read'
username = 'isaacbradys'


token = util.prompt_for_user_token(username, scope,
                                   client_id="569563cc71bb4548a49d5e53d7b226a3",
                                   client_secret = secret,
                                   redirect_uri = 'http://localhost:8080')
spotify = spotipy.Spotify(auth=token)

# get the songs in my download playlist
playlist_tracks = spotify.user_playlist_tracks(playlist_id = '2b6UJkLaXa6UL8JLfHF6yv')
songs = []
nextone = True
while nextone:
    if not playlist_tracks['next']:
        nextone = False
    for item in playlist_tracks["items"]:
        songs.append(item['track']['name'] + " by " + item['track']['artists'][0]['name'])
    playlist_tracks = spotify.next(playlist_tracks)

# get all the songs youtube urls and download them
for song in songs:
    search_url = "https://www.youtube.com/results?search_query=" + song.replace(" ", "+")
    html = urllib.request.urlopen(search_url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    the_url = "https://www.youtube.com/watch?v=" + video_ids[0]
    yt = YouTube(the_url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path="downloaded_audio/")
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded.")
