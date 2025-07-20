from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import lyricsgenius
from utils import clean_lyrics

load_dotenv()
genius = lyricsgenius.Genius(os.getenv("GENIUS_API_TOKEN"))
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

app = Flask(__name__)
CORS(app)



@app.route('/lyrics', methods=['GET'])
def get_lyrics():
    artist = request.args.get('artist')
    title = request.args.get('title')

    if not artist or not title:
        return jsonify({"error": "artist and title required"}), 400

    song = genius.search_song(title, artist)
    if song:
        cleaned_lines = clean_lyrics(song.lyrics)
        return jsonify({"lyrics": cleaned_lines})
    else:
        return jsonify({"error": "Song not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
