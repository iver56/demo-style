# Demo style

A tiny project where I played around with video/demo stylization.

# Set up local Python environment

1. `conda env create`
2. Activate the environment

# Set up style transfer server on Azure

In the following example, we will use [NVIDIA's FastPhotoStyle implementation](https://github.com/NVIDIA/FastPhotoStyle), which requires a very specific environment, with Linux, an NVIDIA GPU, a particular version of CUDA, and Anaconda 2, amongst other things. Therefore, it is simpler to set it up in an ephemeral VM than trying to install it locally. Here are instructions on how you can set up FastPhotoStyle as a REST API web service on Azure:  

First, spin up a "Data Science Virtual Machine" in Azure

* Region: North Europe
* Storage type: HDD
* Instance type: NC6

When the VM is up and running, you must log into it via SSH and run some commands on it.

First, install docker (the new version will replace the slightly outdated one that is already installed. It will also install nvidia-docker2, which we need):
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository

Then clone iver56's fork of FastPhotoStyle, which includes a simple REST API web service:
* `git clone https://github.com/iver56/FastPhotoStyle.git`
* `cd FastPhotoStyle`
* `git submodule update --init --recursive`
* `bash download_models.sh`

Build docker image (this typically takes at least 8 minutes, so you might want to grab a coffee or something while you wait):  
`sudo docker build -t fast-photo-style:v1.0 .`

In the Azure Portal, navigate to the running instance, go to the network config and add an inbound port rule with destination port 5000.

Start the web service inside docker (you must replace the example username "iver" in the command):  
`sudo docker run -d -v /home/iver/FastPhotoStyle:/root/FastPhotoStyle --net=host --runtime=nvidia fast-photo-style:v1.0 /opt/anaconda2/bin/python /root/FastPhotoStyle/web_service.py`

Take note of which IP address the server runs on. In the following example, we will assume that the IP address is `54.55.56.57`

# Usage

First, add content images to data/content_images and add style images to data/style_images. Label files, made with the [labelme tool](https://github.com/wkentaro/labelme), are optional.

Note: The following command(s) must be run in the local environment, i.e. not on the style transfer server on Azure.

To apply stylization to every content/style combination in the dataset, run a command like this (but replace the host IP example with the correct IP address!):  
`python -m app.scripts.stylize --host 54.55.56.57`

The resulting stylized images are stored in a separate folder: data/stylized_images

## Convert stylized images to video

Note that this script assumes that `ffmpeg.exe` is installed and added to `PATH`.

`python -m app.scripts.convert_images_to_video`
