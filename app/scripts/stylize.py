import argparse
import os
import time

import requests
from PIL import Image
from tqdm import tqdm

from app.settings import CONTENT_IMAGE_DIR, STYLE_IMAGE_DIR, STYLIZED_IMAGE_DIR
from app.utils.image import pil_image_to_base64, base64_png_image_to_pillow_image


def get_label_filename(filename):
    """Given a filename, return the filename of the corresponding label png file.

    This label file shows the semantic segmentation for the image.
    """
    filename_without_extension = '.'.join(filename.split('.')[:-1])
    return filename_without_extension + '.__label__.png'


def run(content_image_dir, style_image_dir, host_name):
    """Iterate over the images in the two folders, and find all combinations of content+style

    Generate a stylized image for each combination, and store the result.

    Because FastPhotoStyle is hard to set up (it needs a very specific environment),
    it runs on its own server, and the service is exposed as a REST API.
    """
    rest_api_url = 'http://{}:5000/stylize/'.format(host_name)

    content_filenames_iterator = next(os.walk(content_image_dir))[2]
    content_filenames = []
    for filename in content_filenames_iterator:
        if '__label__' in filename:
            continue
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.png') or filename.lower().endswith('.jpeg'):
            content_filenames.append(filename)

    style_filenames_iterator = next(os.walk(style_image_dir))[2]
    style_filenames = []
    for filename in style_filenames_iterator:
        if '__label__' in filename:
            continue
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.png') or filename.lower().endswith('.jpeg'):
            style_filenames.append(filename)

    for content_filename in tqdm(content_filenames):
        for style_filename in style_filenames:
            if content_filename == style_filename:
                continue

            start_time = time.time()

            content_label_filename = get_label_filename(content_filename)
            style_label_filename = get_label_filename(style_filename)
            output_image_file_path = os.path.join(
                STYLIZED_IMAGE_DIR,
                content_filename + '__' + style_filename + '.png'
            )
            if os.path.isfile(output_image_file_path):
                print('Skipping, because {} already exists'.format(output_image_file_path))
                continue

            content_image = Image.open(os.path.join(content_image_dir, content_filename))
            style_image = Image.open(os.path.join(style_image_dir, style_filename))

            content_segmentation_image = None
            style_segmentation_image = None
            try:
                content_segmentation_image = Image.open(os.path.join(content_image_dir, content_label_filename))
                style_segmentation_image = Image.open(os.path.join(style_image_dir, style_label_filename))
            except FileNotFoundError as e:
                print(e)
                pass

            data = {
                'content_image_base64': pil_image_to_base64(content_image),
                'content_segmentation_base64': pil_image_to_base64(content_segmentation_image),
                'style_image_base64': pil_image_to_base64(style_image),
                'style_segmentation_base64': pil_image_to_base64(style_segmentation_image),
            }

            r = requests.post(rest_api_url, json=data, timeout=60)
            json_data = r.json()
            output_image = base64_png_image_to_pillow_image(json_data['output_image_base64'])
            output_image.save(
                output_image_file_path,
                format='PNG',
            )
            print('Stylized one image ({} s)'.format(time.time() - start_time))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        '--host',
        dest='host',
        help='Specify the IP address or host name of the FastPhotoStyle server.',
        type=str,
        required=False,
        default="localhost"
    )

    args = arg_parser.parse_args()

    run(content_image_dir=CONTENT_IMAGE_DIR, style_image_dir=STYLE_IMAGE_DIR, host_name=args.host)
