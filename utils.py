import re
import deepl
from langdetect import detect, DetectorFactory
import os
from dotenv import load_dotenv

DetectorFactory.seed = 0
load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(DEEPL_API_KEY)


def detect_language(text):
    try:
        lang = detect(text)
        if lang not in ["en", "tr", "es"]:  # DeepL için gerekli diller
            return "en"  # varsayılan fallback
        return lang
    except:
        return "en"



def translate_line_deepl(text, target_lang):
    try:
        if text.strip() == "":
            return ""
        result = translator.translate_text(text, target_lang=target_lang.upper())
        # Aynıysa, çevrilmemiştir → büyük ihtimalle zaten o dildeydi
        if result.text.strip().lower() == text.strip().lower():
            return text
        return result.text
    except Exception as e:
        print(f"Çeviri hatası ({target_lang.upper()}):", e)
        return "[Çeviri başarısız]"


def translate_multilang_lyrics(lines):
    result = []
    for line in lines:
        try:
            en = translate_line_deepl(line, "EN-US")
            tr = translate_line_deepl(line, "TR")
            es = translate_line_deepl(line, "ES")
        except:
            en = tr = es = "[Çeviri başarısız]"

        result.append({
            "original": line,
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
            continue
        cleaned.append(line)
    return cleaned
