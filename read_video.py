#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
# @ File       : read_video.py
# @ Description:  
# @ Author     : Alex Chung
# @ Contact    : yonganzhong@outlook.com
# @ License    : Copyright (c) 2017-2018
# @ Time       : 2020/5/21 下午2:50
# @ Software   : PyCharm
#-------------------------------------------------------

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import ffmpeg

# input_video = './data/time.mp4'
# output_video = './outputs/flip.mp4'

input_video = './data/rafting.avi'
output_video = './outputs/flip.mp4'
output_filename = './outputs/thumbnail.jpeg'

def read_show_video(video_path):
    """

    :param video_path:
    :return:
    """
    try:
        probe = ffmpeg.probe(video_path)
        # get video info except audio
        video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        height = int(video_info['height'])
        width = int(video_info['width'])
        num_frames = int(video_info['nb_frames'])
        frame_rate = int(eval(video_info['r_frame_rate']))

        stream = ffmpeg.input(input_video)
        stream = ffmpeg.output(stream, 'pipe:', format='rawvideo', pix_fmt='rgb24')
        out_video, _  = ffmpeg.run(stream, capture_stdout=True)

        # convert array
        video = np.frombuffer(out_video, np.uint8)
        video = np.reshape(video, (-1, height, width, 3))

        # 1s = 1000ms
        wait_time = int(1000 / frame_rate)

        for frame in range(num_frames):

            # plt.imshow(video[frame,:, :, :])
            # plt.show()
            cv.imshow('optical flow', video[frame,:, :, :])
            k = cv.waitKey(wait_time) & 0xff
            if k == 27:
                break

    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        raise e


def generate_thumbnail(in_filename, out_filename, time, width):
    try:
        (
            ffmpeg
                .input(in_filename, ss=time)
                .filter('scale', width, -1)
                .output(out_filename, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode())

if __name__ == "__main__":
    #
    # flip video
    # stream = ffmpeg.input(input_video)
    # stream = ffmpeg.hflip(stream)
    # stream = ffmpeg.output(stream, output_video)
    # stream = ffmpeg.overwrite_output(stream)
    # ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    # ffmpeg.run(stream)
    # get video info
    input_video = './data/rafting.avi'

    probe = ffmpeg.probe(input_video)

    video_stream_info = probe["streams"][0]
    audio_stream_info = probe["streams"][1]
    format_info = probe["format"]
    # show codec info
    print("codec_type: {0} | codec_name: {1}| codec_long_name: {2}".format(video_stream_info["codec_type"],
                                                                         video_stream_info["codec_name"],
                                                                         video_stream_info["codec_long_name"]))
    print("codec_type: {0} | codec_name: {1}| codec_long_name: {2}".format(audio_stream_info["codec_type"],
                                                                           audio_stream_info["codec_name"],
                                                                           audio_stream_info["codec_long_name"]))
    # show container(encapsulation) format
    print("filename:{0} | format_name: {1} | format_long_name: {2}".format(format_info["filename"],
                                                                           format_info["format_name"],
                                                                           format_info["format_long_name"]))
    # codec_type: video | codec_name: mpeg4| codec_long_name: MPEG-4 part 2
    # filename:./data/rafting.avi | format_name: avi | format_long_name: AVI (Audio Video Interleaved)

    # for info in probe["streams"]:
    #     for k, v in info.items():
    #         print(k, ':', v)
    #
    # print('-' * 40)
    # for k, v in probe['format'].items():
    #     print(k, ':', v)

    # read_show_video(input_video)
    # generate_thumbnail(in_filename=input_video, out_filename=output_filename, time=0.1, width=120)






