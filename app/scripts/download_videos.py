import os

from pytube import YouTube
from tqdm import tqdm

from app.settings import VIDEO_LISTS_DIR, DOWNLOADED_VIDEOS_DIR
from app.utils.text import read_lines
from app.utils.youtube import parse_youtube_external_id

video_collections = {
    'colorful_videos': read_lines(os.path.join(VIDEO_LISTS_DIR, 'colorful_videos.txt')),
    'greyscale_videos': read_lines(os.path.join(VIDEO_LISTS_DIR, 'greyscale_videos.txt')),
}

for video_collection_name in video_collections:
    video_urls = video_collections[video_collection_name]
    for video_url in tqdm(video_urls, desc='Downloading {}'.format(video_collection_name)):
        external_id = parse_youtube_external_id(video_url)

        output_path = os.path.join(DOWNLOADED_VIDEOS_DIR, video_collection_name)
        filename_stem = external_id
        file_path = os.path.join(output_path, filename_stem + '.mp4')
        if os.path.isfile(file_path):
            print('\nSkipping {} because it already exists'.format(filename_stem))
        else:
            YouTube(video_url).streams.first().download(
                output_path=output_path, filename=filename_stem
            )
