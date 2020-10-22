import re
from wordcloud import WordCloud
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import FreqDist
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.express as px
import plotly.tools as tls
import plotly.graph_objs as go
import plotly.offline as py
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy
import sys
import requests
import json
import lyricsgenius
import types
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
genius = lyricsgenius.Genius('l4J-3WFatATy8mJHgnsYVausDrWZo9GsXzui4_DWu5PiXfMDZ_s30iAB2DGtdEMQ')
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
track_name = []
album_name = []
artist_name = []
# creating arrays for storing id and name
for i in recentsongs['items']:
    track_name.append(i['track']['name'])
    artist_name.append(i['track']['artists'][0]['name'])
lyrics = {}
text = []
compoundscore = []
sid = SentimentIntensityAnalyzer()
track_name = list(dict.fromkeys(track_name))
for i in range(len(track_name)):
    song = genius.search_song(track_name[i], artist_name[i])
    songlyrics = song.lyrics.replace("\n", " ").replace("\\'", "\'")
    lyrics[track_name[i]] = songlyrics
    songlyrics = songlyrics.replace('(', '').replace(')', '')
    text.append(re.sub("[\\[].*?[\\]]", "", songlyrics))
    scores = sid.polarity_scores(text[i])
    compoundscore.append(scores['compound'])
text = ' '.join(map(str, text))
print(text.encode("utf-8"))
stopwords = set(stopwords.words('english'))
stopwords.update(["br", "href", "la", "yeah", "yuh", "wan", "i'm"])

sentences = sent_tokenize(text)
words = word_tokenize(text)
words_no_punc = []
for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

ps = PorterStemmer()
clean_words = []
for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(ps.stem(w))
fdist = FreqDist(clean_words)
print(fdist.most_common(10))
fdist.plot(10)
def test():
    print("HEy")

# making wordcloud
words_string = ' '.join(map(str, clean_words))
wordcloud = WordCloud(stopwords=stopwords).generate(words_string)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
print(compoundscore)
plt.plot(compoundscore)
plt.show()
pos_count = 0
neg_count = 0
for num in compoundscore:
    if num >= 0:
        pos_count += 1

    else:
        neg_count += 1
plt.pie([pos_count, neg_count], labels=["Positive Songs", "Negative Songs"])

def lyl():
    return plt.show()
