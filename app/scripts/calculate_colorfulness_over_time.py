import os

import cv2
import imutils
import matplotlib.pyplot as plt
import six
from tqdm import tqdm

from app.settings import DOWNLOADED_VIDEOS_DIR, PLOTS_DIR
from app.utils.colorfulness import calculate_image_colorfulness
from app.utils.image import get_image_file_paths
from app.utils.video import get_immediate_child_directories


def plot_colorfulness_series(series, output_path):
    """Plot colorfulness series and save the figure to file."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Colorfulness")
    ax.plot(series)
    plt.savefig(output_path)
    plt.close(fig)


if __name__ == "__main__":
    video_collections = {
        "colorful_videos": os.path.join(DOWNLOADED_VIDEOS_DIR, "colorful_videos"),
        "greyscale_videos": os.path.join(DOWNLOADED_VIDEOS_DIR, "greyscale_videos"),
    }

    for video_collection_name, directory in six.iteritems(video_collections):
        frame_folders = get_immediate_child_directories(directory)
        for frame_folder in tqdm(frame_folders):
            frame_paths = get_image_file_paths(frame_folder)

            image_colorfulness_values = []

            for frame_path in tqdm(frame_paths):
                image = cv2.imread(frame_path)
                image = imutils.resize(image, width=250)
                image_colorfulness = calculate_image_colorfulness(image)
                image_colorfulness_values.append(image_colorfulness)

            print(image_colorfulness_values)

            plot_colorfulness_series(
                image_colorfulness_values,
                os.path.join(
                    PLOTS_DIR, "{}_colorfulness.png".format(frame_folder.parts[-1])
                ),
            )
