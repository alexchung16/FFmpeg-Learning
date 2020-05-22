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
    # probe = ffmpeg.probe(input_video)
    # print(probe["streams"])
    # print(probe['format'])
    #
    # # video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    # # width = int(video_stream['width'])
    # # height = int(video_stream['height'])
    #
    # for info in probe["streams"]:
    #     for k, v in info.items():
    #         print(k, ':', v)
    #
    # for k, v in probe['format'].items():
    #     print(k, ':', v)


    # general thumbnail for video
    # try:
    #     stream = ffmpeg.input(input_video, ss=0.1)
    #     stream = ffmpeg.filter(stream, 'scale', 120, -1)
    #     stream = ffmpeg.output(stream, output_filename, vframes=1)
    #     stream = ffmpeg.overwrite_output(stream)
    #     ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    # except ffmpeg.Error as e:
    #     print(e.stderr.decode(), file=sys.stderr)
    #     raise e

    # def generate_thumbnail(in_filename, out_filename, time, width):
    #     try:
    #         (
    #             ffmpeg
    #                 .input(in_filename, ss=time)
    #                 .filter('scale', width, -1)
    #                 .output(out_filename, vframes=1)
    #                 .overwrite_output()
    #                 .run(capture_stdout=True, capture_stderr=True)
    #         )
    #     except ffmpeg.Error as e:
    #         print(e.stderr.decode())
    #
    # generate_thumbnail(in_filename=input_video, out_filename=output_filename, time=0.1, width=120)

    # convert video to numpy array

    try:
        probe = ffmpeg.probe(input_video)
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




