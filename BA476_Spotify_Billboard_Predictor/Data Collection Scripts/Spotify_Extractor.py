#Spotify Extractor
#Tristan Tew
#Takes a list of Spotify Song IDs and pulls Album/Artist Info to create richer data entries

import spotipy
import csv
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Load Dataset
df = pd.read_csv('C:/Users/trist/Downloads/dataset-of-10s.csv')
print(df.head())
#Identify Track ID Column
uri = df["uri"]

#Define Empty lists that will become dataframe columns

#Song Level Columns
num_art = []
explicit = []
track_number = []
release_month = []

#Album Columns
alb_type=[]
album_tracks = []

#Main Artist Columns
ma_popularity = []
ma_followers = []

#Featured Artist Columns
fa_popularity = []
fa_followers = [] 

#Combined Genres
genres = []
genres_count = []

timer = 0
for i in uri:
    timer +=1
    #Use the song metadata to collect the user data
    song_meta = sp.track(i)

    #Store potentially useful song data
    explicit.append(song_meta['explicit'])
    track_number.append(song_meta['track_number'])


    reldate = (song_meta['album']['release_date'])
    relmonth = (reldate[-5:-3:])

    release_month.append(relmonth)

    #Number artists on the song
    number_artists = len(song_meta['artists'])
    num_art.append(number_artists)

    #Collect All Artists
    artists = []
    for i in range(number_artists):
        artist_id = song_meta['artists'][i]['uri']
        artists.append(artist_id)

    #Define Album Data
    album_type = song_meta['album']['album_type']
    alb_uri = song_meta['album']['uri']
    album_full = sp.album(alb_uri)


    album_tracks.append(album_full['total_tracks'])
    alb_type.append(album_type)

    #Define Main Artist
    main_artist_uri = artists[0]
    main_artist_meta = sp.artist(main_artist_uri)

    #Main Artist info section
    ma_popularity.append(main_artist_meta['popularity'])
    ma_followers.append(main_artist_meta['followers']['total'])

    #Add Genres from Main Artis
    song_gen = []
    for g in main_artist_meta['genres']:
        song_gen.append(g)

    #Loop through features for featured artist info
    fols = 0 
    popscore = 0 
    accum = 0 
    for i in range(1,len(artists)):
        accum += 1
        fa_meta = sp.artist(artists[i])
        popscore += fa_meta['popularity']
        fols += (fa_meta['followers']['total'])
        for g in fa_meta['genres']:
            song_gen.append(g)

    genres.append(song_gen)

    if accum == 0:
        fa_popularity.append(0)
    else:
        fa_popularity.append(popscore / accum)
    fa_followers.append(fols)


    print(list(set(song_gen)))
    print(len(list(set(song_gen))))
    genres_count.append(len(list(set(song_gen))))
            
#Song Level Columns
df['explicit'] = explicit
df['track_number'] = track_number
df['number_of_artists_on_song']= num_art
df['release_month'] = release_month
df['genres'] = genres
df['genres_count'] = genres_count

#Album Level Columns
df['alb_type']=alb_type
df['album_tracks'] = album_tracks

#Main Artist Columns
df["main_popularities"] = ma_popularity
df['main_followers']=ma_followers

#Secondary Artist Columns (iterate for total number of columns)
df["feature_popularities"] = fa_popularity
df['feature_followers']=fa_followers


# print(df.head())

df.to_csv('New_Spotify.csv')
