import re


def parse_youtube_external_id(url):
    """Return the id part of any YouTube URL.

    Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ -> dQw4w9WgXcQ
    """

    youtube_regex = (
        r"(https?://)?(www\.|m\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return None
