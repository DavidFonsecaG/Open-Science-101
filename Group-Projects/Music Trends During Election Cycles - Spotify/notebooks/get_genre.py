import pandas as pd
import requests
import base64
from dotenv import load_dotenv
import os

# Spotify API credentials
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Get token
def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

# Get track info
def get_track_info(track_id, access_token):
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching track info: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")
    
    response.raise_for_status()
    return response.json()

# Get artist info
def get_artist_info(artist_id, access_token):
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching artist info: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")
    
    response.raise_for_status()
    return response.json()

# Get genre for a track by using the artist's genres
def get_track_genre(track_id, access_token):
    track_info = get_track_info(track_id, access_token)
    artist_id = track_info['artists'][0]['id']
    artist_info = get_artist_info(artist_id, access_token)
    return ', '.join(artist_info.get('genres', []))

# Main
def add_genres_to_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    access_token = get_access_token()
    df['genre'] = None
    count = 0
    for index, row in df.iterrows():
        track_id = row['track_id']
        genre = get_track_genre(track_id, access_token)
        df.at[index, 'genre'] = genre
        print(count)
        count +=1
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved to {output_csv}")

input_csv = 'playlist_2010to2023.csv'
output_csv = 'playlist_with_genres.csv'
add_genres_to_csv(input_csv, output_csv)
