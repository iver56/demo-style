import os
import subprocess
from pathlib import Path

from tqdm import tqdm

from app.settings import DOWNLOADED_VIDEOS_DIR
from app.utils.video import get_video_file_paths

"""
Extract frames from downloaded videos, and store them as JPG files.
"""


video_collections = {
    "colorful_videos": get_video_file_paths(
        os.path.join(DOWNLOADED_VIDEOS_DIR, "colorful_videos")
    ),
    "greyscale_videos": get_video_file_paths(
        os.path.join(DOWNLOADED_VIDEOS_DIR, "greyscale_videos")
    ),
    "ninjadev_videos": get_video_file_paths(
        os.path.join(DOWNLOADED_VIDEOS_DIR, "ninjadev_videos")
    ),
}

for video_collection_name in video_collections:
    video_file_paths = video_collections[video_collection_name]

    for video_file_path in tqdm(
        video_file_paths, desc="Extracting frames from {}".format(video_collection_name)
    ):
        path = Path(video_file_path)

        first_image_path = os.path.join(
            path.parent, path.stem, path.stem + "_00001.jpg"
        )
        if os.path.isfile(first_image_path):
            print(
                "\nSkipping {} because frames seem"
                " to be extracted for this video already".format(path.stem)
            )
            continue

        # Make a folder for the frames, if the folder does not already exist
        os.makedirs(os.path.join(path.parent, path.stem), exist_ok=True)

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                "{}".format(path.as_posix()),
                "{}".format(
                    Path(
                        os.path.join(path.parent, path.stem, path.stem + "_%05d.jpg")
                    ).as_posix()
                ),
            ]
        )
