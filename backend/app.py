from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import os
import lyricsgenius
from utils import clean_lyrics, translate_multilang_lyrics
import requests
import base64

load_dotenv()

# Genius
genius = lyricsgenius.Genius(os.getenv("GENIUS_API_TOKEN"))
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

# Spotify Credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

app = Flask(__name__)
CORS(app)


def get_spotify_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return r.json().get("access_token")


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


@app.route('/spotify', methods=['GET'])
def get_spotify_url():
    artist = request.args.get('artist')
    title = request.args.get('title')

    token = get_spotify_token()
    if not token:
        return jsonify({"error": "Spotify token error"}), 500

    query = f"{title} {artist}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 1}

    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    items = r.json().get("tracks", {}).get("items")

    if items:
        return jsonify({"url": items[0]["external_urls"]["spotify"]})
    else:
        return jsonify({"error": "Spotify track not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
