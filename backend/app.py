from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import lyricsgenius
from utils import clean_lyrics, translate_multilang_lyrics
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# Genius
genius = lyricsgenius.Genius(os.getenv("GENIUS_API_TOKEN"))
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

# Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

# Flask
app = Flask(__name__)
CORS(app)

# Lyrics endpoint
@app.route('/lyrics', methods=['GET'])
def get_lyrics():
    artist = request.args.get('artist')
    title = request.args.get('title')

    if not artist or not title:
        return jsonify({"error": "artist and title required"}), 400

    song = genius.search_song(title, artist)
    if song:
        lines = clean_lyrics(song.lyrics)
        translated_lines = translate_multilang_lyrics(lines)
        return jsonify({"lyrics": translated_lines})
    else:
        return jsonify({"error": "Song not found"}), 404

# Spotify track ID endpoint


@app.route('/spotify', methods=['GET'])
def get_spotify_track():
    artist = request.args.get('artist')
    title = request.args.get('title')

    if not artist or not title:
        return jsonify({"error": "artist and title required"}), 400

    query = f"{title} {artist}"
    result = sp.search(q=query, type='track', limit=1)
    if result['tracks']['items']:
        item = result['tracks']['items'][0]
        track_info = {
            "track_id": item['id'],
            "track_name": item['name'],
            "artist_name": item['artists'][0]['name'],
            "album_name": item['album']['name'],
            "album_image": item['album']['images'][0]['url'],
            "release_date": item['album']['release_date'],
            "spotify_url": item['external_urls']['spotify']

        }
        return jsonify(track_info)
    else:
        return jsonify({"error": "Track not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
