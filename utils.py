import re

def clean_lyrics(raw_lyrics: str) -> list[str]:
    lines = raw_lyrics.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"\d+ Contributors", line):
            continue
        if "Lyrics" in line:
            continue
        if re.match(r"\(.*?\)", line):
            continue  # Parantezli satırları atla
        cleaned.append(line)
    return cleaned
