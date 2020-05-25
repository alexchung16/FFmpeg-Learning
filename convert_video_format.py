#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
# @ File       : convert_video_format.py
# @ Description:  
# @ Author     : Alex Chung
# @ Contact    : yonganzhong@outlook.com
# @ License    : Copyright (c) 2017-2018
# @ Time       : 2020/5/25 上午10:29
# @ Software   : PyCharm
#-------------------------------------------------------

import os
import ffmpeg


input_video = './data/rafting.avi'
output_video = './outputs/rafting.mp4'


if __name__ == "__main__":

    # get video info
    probe = ffmpeg.probe(input_video)
    print(probe["streams"])
    print(probe['format'])

    # video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    # width = int(video_stream['width'])
    # height = int(video_stream['height'])

    for info in probe["streams"]:
        for k, v in info.items():
            print(k, ':', v)

    for k, v in probe['format'].items():
        print(k, ':', v)

    # convert video codec to h.264
    def convert_format(ffmpeg_exec="ffmpeg", input_file=None, output_file=None, codec="libx264"):

       convert_command = f'{ffmpeg_exec} -y -i {input_file} -map 0 -c:v {codec} -c:a copy {output_file}'

       result = os.popen(convert_command)
       return result.readline()


    result = convert_format(input_file=input_video, output_file=output_video)
    print(result)