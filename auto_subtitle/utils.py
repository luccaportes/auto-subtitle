import os
from typing import Iterator
import requests
import json

def translate(question, source_lang, target_lang):
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "q": question,
        "source": source_lang,
        "target": target_lang,
        "format": "text",
        "api_key": ""
    }

    lt_host = os.getenv("LIBRETRANSLATE_HOST")

    response = requests.post(f"{lt_host}/translate", headers=headers, data=json.dumps(data))
    return response.json()["translatedText"]


def str2bool(string):
    string = string.lower()
    str2val = {"true": True, "false": False}

    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file):
    for i, segment in enumerate(transcript, start=1):
        txt = segment['text'].strip().replace('-->', '->')
        txt = translate(txt, "en", "pt")
        print(
            f"{i}\n"
            f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
            f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
            f"{txt}\n",
            file=file,
            flush=True,
        )


def filename(path):
    return os.path.splitext(os.path.basename(path))[0]
