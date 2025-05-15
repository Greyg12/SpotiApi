# Import necessary libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
import time
import os
from dotenv import load_dotenv
from spotipy.exceptions import SpotifyException

# Load environment variables from the .env file (make sure you have this file!)
load_dotenv()

# Spotify API configuration (keys loaded from .env)
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-read-private playlist-modify-private user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Function with automatic retry for 429 (Too Many Requests)
def get_album_with_retry(sp, album_id, retries=5):
    for attempt in range(retries):
        try:
            return sp.album(album_id)
        except SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", 5))
                print(f"⚠️ API limit reached! Waiting {retry_after} seconds...")
                time.sleep(retry_after + 1)
            else:
                print(f"Error fetching album: {e}")
                break
        except Exception as e:
            print(f"Other error with album: {e}")
            break
    return None

# Fetch playlist data
playlist_id = '4fsu0ZRfn3EJ4ezICrYAcV' #YOUR PLAYLIST ID
try:
    playlist = sp.playlist(playlist_id)
    main_playlist_name = playlist['name']
except Exception as e:
    print(f"Error: {e}")
    exit()

# Collecting track information
all_tracks = []
tracks = playlist['tracks']

while tracks:
    for item in tracks['items']:
        try:
            track = item.get('track', {})
            if not track or not track.get('id'):
                continue

            # Fetch release year with safeguards and retry
            release_year = None
            try:
                if track.get('album') and track['album'].get('id'):
                    album = get_album_with_retry(sp, track['album']['id'])  # ✅ retry
                    time.sleep(0.2)  # ⏱️ delay to prevent rate limits
                    if album:
                        release_date = album.get('release_date', '')
                        if release_date:
                            release_year = int(release_date.split('-')[0])
            except Exception as e:
                print(f"Error with album: {e}")

            # Add to list
            all_tracks.append({
                'track_id': track['id'],
                'track_name': track.get('name', 'Unknown title'),
                'release_year': release_year
            })

        except Exception as e:
            print(f"Error processing track: {e}")
            continue

    if tracks.get('next'):
        time.sleep(0.5)  # ⏱️ delay between playlist pages
        tracks = sp.next(tracks)
    else:
        tracks = None

# Create DataFrame with additional safeguards
df = pd.DataFrame(all_tracks)

# Clean and convert release year
df['release_year'] = (
    pd.to_numeric(df['release_year'], errors='coerce')
    .fillna(-1)
    .astype(int)
    .replace(-1, pd.NA)
)

# Function to assign decade
def assign_decade(year):
    try:
        year_int = int(round(float(year)))
        if 1900 < year_int < 2100:
            return f"{(year_int // 10) * 10}s"
        return 'Unknown decade'
    except (ValueError, TypeError):
        return 'Unknown decade'

# Add 'decade' column
df['decade'] = df['release_year'].apply(assign_decade)

# Group by decades
user_id = sp.me()['id']
decade_groups = df.groupby('decade', observed=True)

# Handle "Unknown decade"
if 'Unknown decade' in decade_groups.groups:
    unknown_group = decade_groups.get_group('Unknown decade')
    if not unknown_group.empty:
        unknown_playlist = sp.user_playlist_create(
            user=user_id,
            name=f"{main_playlist_name} - Unknown decade",
            public=False
        )
        track_ids = unknown_group['track_id'].tolist()
        for i in range(0, len(track_ids), 100):
            sp.playlist_add_items(unknown_playlist['id'], track_ids[i:i + 100])
            time.sleep(1)
        print(f"✅ Created playlist: {main_playlist_name} - Unknown decade ({len(track_ids)} tracks)")

# Create playlists for known decades
for decade, group in decade_groups:
    if decade == 'Unknown decade':
        continue

    if not group.empty:
        try:
            clean_decade = decade.replace('.0', '')
            playlist_name = f"{main_playlist_name} - {clean_decade}"

            new_playlist = sp.user_playlist_create(
                user=user_id,
                name=playlist_name,
                public=False
            )

            track_ids = group['track_id'].tolist()
            for i in range(0, len(track_ids), 100):
                sp.playlist_add_items(new_playlist['id'], track_ids[i:i + 100])
                time.sleep(1)
            print(f"✅ Created playlist: {playlist_name} ({len(track_ids)} tracks)")

        except Exception as e:
            print(f"❌ Error creating playlist {playlist_name}: {e}")

print("🎉 Process completed successfully!")
