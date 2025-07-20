import re
from langdetect import detect, DetectorFactory
from googletrans import Translator

DetectorFactory.seed = 0
translator = Translator()


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def translate_line(text, source_lang, dest_lang):
    try:
        if text.strip() == "":
            return ""
        return translator.translate(text, src=source_lang, dest=dest_lang).text
    except:
        return "[Çeviri başarısız]"


def translate_multilang_lyrics(lines):
    result = []
    for line in lines:
        lang = detect_language(line)
        try:
            en = translate_line(line, lang, "en") if lang != "en" else line
            tr = translate_line(line, lang, "tr") if lang != "tr" else line
            es = translate_line(line, lang, "es") if lang != "es" else line
        except:
            en, tr, es = "[Çeviri başarısız]", "[Çeviri başarısız]", "[Çeviri başarısız]"

        result.append({
            "original": line,
            "lang": lang,
            "en": en,
            "tr": tr,
            "es": es
        })
    return result


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
