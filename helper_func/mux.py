
from config import Config
import time
import re
import asyncio


progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }
    if not items:
        return None
    return items

async def readlines(stream):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)

        for line in lines:
            yield line

        data.extend(await stream.read(1024))


async def softmux_vid(vid_filename, sub_filename, msg):

    vid = Config.DOWNLOAD_DIR+'/'+vid_filename
    sub = Config.DOWNLOAD_DIR+'/'+sub_filename

    out_file = '.'.join(vid_filename.split('.')[:-1])
    output = out_file+'1.mkv'
    out_location = Config.DOWNLOAD_DIR+'/'+output
    sub_ext = sub_filename.split('.').pop()
    command = [
            'ffmpeg','-hide_banner',
            '-i',vid,
            '-i',sub,
            '-map','1:0','-map','0',
            '-disposition:s:0','default',
            '-c:v','copy',
            '-c:a','copy',
            '-c:s',sub_ext,
            '-y',out_location
            ]

    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )

    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/ffmpeg.py#L114
    
    
    if process.returncode == 0:
        await msg.edit('Muxing  Completed Successfully!\n\nTime taken : {} seconds'.format(round(start-time.time())))
    else:
        await msg.edit('An Error occured while Muxing!')
        return False
    time.sleep(2)
    return output


async def hardmux_vid(vid_filename, sub_filename, msg):
    
    sssf = sub_filename
    vid = Config.DOWNLOAD_DIR+'/'+vid_filename
    sub = "fonts/edited.ass"
    out_file = '.'.join(vid_filename.split('.')[:-1])
    output = out_file+'1.mp4'
    out_location = Config.DOWNLOAD_DIR+'/'+output
      
    command = [
            'ffmpeg','-hide_banner',
            '-i',vid,
            '-vf',"subtitles="+sub+":fontsdir=fonts/font:force_style='Fontname=B Titr,Fontsize=28,PrimaryColour=&H0000FFFF'", #,SecondaryColour=&H0300FFFF'", #,OutlineColour=&H00000000,BackColour=&H02000000,ScaleX=100,ScaleY=100,BorderStyle=1,Outline=1,Alignment=2,MarginL=10,MarginR=10,MarginV=10,Encoding=1'",
            '-c:v','h264',
            '-map','0:v:0',
            '-map','0:a:0?',
            #'-preset','ultrafast',
            '-y',out_location
            ]
    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    
    
    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/ffmpeg.py#L114
    
    if process.returncode == 0:
        await msg.edit('Muxing  Completed Successfully!\n\nTime taken : {} seconds'.format(round(start-time.time())))
    else:
        await msg.edit('An Error occured while Muxing!')
        return False
    time.sleep(2)
    return output
