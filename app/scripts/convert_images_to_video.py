import argparse
import os
from pathlib import Path
import subprocess

from app.settings import STYLIZED_IMAGE_DIR, TMP_DIR, VIDEO_OUTPUT_DIR
from app.utils.image import get_image_file_paths

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        '--framerate',
        dest='framerate',
        help='Specify the framerate as a positive integer',
        type=int,
        required=False,
        default=30
    )

    args = arg_parser.parse_args()

    image_file_paths = get_image_file_paths(STYLIZED_IMAGE_DIR)
    image_list_file_path = os.path.join(TMP_DIR, 'images.txt')

    with open(image_list_file_path, 'w') as f:
        for path in image_file_paths:
            f.write('file {}\n'.format(Path(path).as_posix()))

    subprocess.run(
        [
            "ffmpeg",
            "-r", "{}".format(args.framerate),
            "-f", "concat",
            "-safe", "0",
            "-i", image_list_file_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "{}".format(Path(os.path.join(VIDEO_OUTPUT_DIR, "video.mp4")).as_posix())
        ],
    )
