import lyricsgenius

genius = lyricsgenius.Genius("TaHd4DAkJv3jsBfi3WQ8Ra1UkkNjJ1oJn5kgjvqfgOWS98Y-GG4iBS_Qe202j9a5")  # Buraya kendi token’ını yazacaksın
song = genius.search_song("Loca", "Shakira")
print(song.lyrics)
