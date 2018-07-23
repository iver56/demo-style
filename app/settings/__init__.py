import os


BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
DATA_DIR = os.path.join(BASE_DIR, 'data')
STYLE_IMAGE_DIR = os.path.join(DATA_DIR, 'style_images')
CONTENT_IMAGE_DIR = os.path.join(DATA_DIR, 'content_images')
STYLIZED_IMAGE_DIR = os.path.join(DATA_DIR, 'stylized_images')
VIDEO_OUTPUT_DIR = os.path.join(DATA_DIR, 'video_output')
TMP_DIR = os.path.join(DATA_DIR, 'tmp')
VIDEO_LISTS_DIR = os.path.join(DATA_DIR, 'video_lists')
DOWNLOADED_VIDEOS_DIR = os.path.join(DATA_DIR, 'downloaded_videos')
