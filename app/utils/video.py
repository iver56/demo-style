import os


def get_video_file_paths(root_path):
    """Return a list of paths to all video files in a directory (does not check subdirectories)."""
    video_file_paths = []

    for root, dirs, filenames in os.walk(root_path):
        filenames = sorted(filenames)
        for filename in filenames:
            input_path = os.path.abspath(root)
            file_path = os.path.join(input_path, filename)

            file_extension = filename.split('.')[-1]
            if file_extension.lower() == 'mp4':
                video_file_paths.append(file_path)

        break  # prevent descending into subfolders

    return video_file_paths
