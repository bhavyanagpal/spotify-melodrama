from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy
import sys
import requests
import json
import pandas as pd
import types
from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
import re

# for acessing private playlists

scope = 'playlist-read-private'
username = '8eia8ggl4ipbhouhun62o9y8i'
client_id = '3cb41450f466404399f3e0de3e4c89f2'
client_secret = '51406619960a46c3a0fc8682e5152784'
redirect_uri = 'http://localhost:8888/callback/'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
token = util.prompt_for_user_token(username, scope, client_id, client_secret,
                                   redirect_uri)

# accessing last 50 tracks frpm history


def current_user_recently_played(self, limit=50):
    return self._get('me/player/recently-played', limit=limit)


token = util.prompt_for_user_token(
    username='8eia8ggl4ipbhouhun62o9y8i',
    scope="user-read-recently-played user-read-private user-top-read user-read-currently-playing",
    client_id='3cb41450f466404399f3e0de3e4c89f2',
    client_secret='51406619960a46c3a0fc8682e5152784',
    redirect_uri='http://localhost:8888/callback/')

spotify = spotipy.Spotify(auth=token)
spotify.current_user_recently_played = types.MethodType(current_user_recently_played, spotify)

# creating .json file
recentsongs = spotify.current_user_recently_played(limit=50)
out_file = open("recentsongs.json", "w")
out_file.write(json.dumps(recentsongs, sort_keys=True, indent=2))
out_file.close()


f = open('recentsongs.json',)
data = json.load(f)
f.close()
track_id = []
track_name = []
album_name = []
artist_name = []
track_time = []
# creating arrays for storing id and name
for i in recentsongs['items']:
    track_id.append(i['track']['id'])
    track_name.append(i['track']['name'])
    album_name.append(i['track']['album']['name'])
    artist_name.append(i['track']['artists'][0]['name'])
    temp = i['played_at']
    track_time.append(re.sub('.[0-9].[000-999]Z', '', temp))

# accessing features of all 50 tracks
features = []
tracks = {}
for track in track_id:
    features.append(sp.audio_features(track))

# initialising all tracks with corresponding feature values and storing in a dictionary
for i in range(0, 50):
    tracks[i+1] = {}
for i in range(0, 50):
    tracks[i+1]['number'] = i+1
    tracks[i+1]['time'] = track_time[i]
    tracks[i+1]['name'] = track_name[i]
    tracks[i+1]['id'] = track_id[i]
    tracks[i+1]['album'] = album_name[i]
    tracks[i+1]['artist'] = artist_name[i]
    tracks[i+1]['acousticness'] = features[i][0]['acousticness']
    tracks[i+1]['danceability'] = features[i][0]['danceability']
    tracks[i+1]['energy'] = features[i][0]['energy']
    tracks[i+1]['instrumentalness'] = features[i][0]['instrumentalness']
    tracks[i+1]['liveness'] = features[i][0]['liveness']
    tracks[i+1]['loudness'] = features[i][0]['loudness']
    tracks[i+1]['speechiness'] = features[i][0]['speechiness']
    tracks[i+1]['tempo'] = features[i][0]['tempo']
    tracks[i+1]['valence'] = features[i][0]['valence']
    pop = sp.track(track_id[i])
    tracks[i+1]['popularity'] = pop['popularity']

# creating dictionary to convert into dataframe
feature = ['number', 'time', 'name', 'id', 'album', 'artist', 'acousticness',
           'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
           'speechiness', 'tempo', 'valence', 'popularity']
dic_df = {}

# initialising dictionary
for x in feature:
    dic_df[x] = []
for j in range(1, 50):
    for x in feature:
        dic_df[x].extend([tracks[j][x]])

# creating dataframe from dictionary
dataframe = pd.DataFrame.from_dict(dic_df).drop_duplicates(subset='name')
pd.set_option('display.width', None)
print(dataframe)
valence_vals = dataframe['valence'].tolist()
less_count, more_count, middle_count = 0, 0, 0
for num in valence_vals:

    if num >= 0 and num < 0.5:
        less_count += 1
    elif num >= 0.5 and num < 0.6:
        middle_count += 1
    else:
        more_count += 1

venn2_unweighted(subsets=(less_count, more_count, middle_count),
                 set_labels=('Low Spirit', 'High Spirit'), set_colors=('navy', 'lime'),
                 alpha=0.5)
dataframe.plot.line(x='time', y=['danceability', 'energy', 'valence'])
plt.xticks(rotation=90)
plt.show()

# if the graph is erratic, thay maybe because of streaming of a particular artist/ album,
# since an album contains a mixture of sad and energetic songs. so we take a look
# at the number of unique artists and albums in the history :

def val():
    return (dataframe['album'].value_counts(ascending=False),dataframe['artist'].value_counts(ascending=False))

