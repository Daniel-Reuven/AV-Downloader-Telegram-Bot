import yt_dlp
import os
import re
from loguru import logger
from clouds import manage_downloads, mega_check_if_exists


class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            logger.debug(f'yt-dlp: {msg}'.format())
            pass
        else:
            self.info(msg)

    def info(self, msg):
        logger.info(f'yt-dlp: {msg}'.format())
        pass

    def warning(self, msg):
        logger.warning(f'yt-dlp: {msg}'.format())
        pass

    def error(self, msg):
        logger.error(f'yt-dlp: {msg}'.format())


def download_youtube_video(yt_link, mode, m):
    if mode == 1:  # Video
        try:
            # Parameters for youtube_dl use
            ydl = {
                'noplaylist': 'True',
                'logger': MyLogger(),
                'verbose': False,
                'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'writethumbnail': True,
                'postprocessors': [{
                    'key': 'EmbedThumbnail',
                    'already_have_thumbnail': False,
                }],
                'outtmpl': './%(id)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl) as ydl:
                ydl.cache.remove()
                tempvideo = ydl.extract_info(yt_link, download=False)
                if tempvideo['duration'] > 600:
                    return "Error, Server error has occurred, video duration is above allowed limit."
                filename = '' + tempvideo['id'] + '.mp4'
                filenameclean = tempvideo['title']
                s = re.sub(r'[^a-zA-Z0-9\u0590-\u05FF\u0627-\u064a\u0400-\u04FF \n\.-]', '', filenameclean)
                # Remove double spaces
                while '  ' in s:
                    s = s.replace("  ", " ")
                # Remove dots at the end of title.
                while s.endswith('.'):
                    s = s[:len(s) - 1]
                if s.endswith(' '):
                    s = s[:len(s) - 1]
                if not len(s) == 0:
                    filename2 = '[' + tempvideo['id'] + ']' + s + '.mp4'
                else:
                    filename2 = '[' + tempvideo['id'] + ']' + 'title contains illegal characters' + '.mp4'
                filecheck = mega_check_if_exists(filename2, m)
                if filecheck.startswith('Error'):
                    if os.path.isfile(filename2):
                        logger.info(f'The file already exists locally'.format())
                    else:
                        logger.info(f'The file does not exist locally, need to download'.format())
                        video = ydl.extract_info(yt_link, download=True)
                        temp_filename = tempvideo['id'] + 'h265.mp4'
                        os.system(f'ffmpeg -i ' + filename + f' -c:v libx265 -vtag hvc1 -c:a aac ' + temp_filename)
                        # Rename the file
                        logger.info(f"Renaming file {temp_filename} to {filename2}".format())
                        os.rename(temp_filename, filename2)
                    logger.info(f"Processing with Mega: {filename2}".format())
                    link = manage_downloads(filename2, m)
                    if os.path.isfile(filename):
                        os.remove(filename)
                        logger.info(f'local file {filename} has been deleted'.format())
                    else:
                        logger.info(f'file to be deleted does not exist'.format())
                    if os.path.isfile(filename2):
                        os.remove(filename2)
                        logger.info(f'local file {filename2} has been deleted'.format())
                    else:
                        logger.info(f'file to be deleted does not exist'.format())
                    return link
                else:
                    return filecheck
        except:
            return "Error, Server error has occurred"
    if mode == 2:  # Audio
        try:
            # Parameters for youtube_dl use
            ydl = {
                'format': 'bestaudio/best',
                'logger': MyLogger(),
                'verbose': False,
                'writethumbnail': True,
                'noplaylist': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                    {
                        'key': 'EmbedThumbnail',
                    }
                ],
                'outtmpl': './%(id)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl) as ydl:
                ydl.cache.remove()
                tempaudio = ydl.extract_info(yt_link, download=False)
                filename = tempaudio['id'] + '.mp3'
                filenameclean = tempaudio['title']
                s = re.sub(r'[^a-zA-Z0-9\u0590-\u05FF\u0627-\u064a\u0400-\u04FF \n\.-]', '', filenameclean)
                while '  ' in s:
                    s = s.replace("  ", " ")
                while s.endswith('.'):
                    s = s[:len(s) - 1]
                if s.endswith(' '):
                    s = s[:len(s) - 1]
                if not len(s) == 0:
                    filename2 = '[' + tempaudio['id'] + ']' + s + '.mp3'
                else:
                    filename2 = '[' + tempaudio['id'] + ']' + 'title contains illegal characters' + '.mp3'
                filecheck = mega_check_if_exists(filename2, m)
                if filecheck.startswith('Error'):
                    if os.path.isfile(filename2):
                        logger.info(f'The file already exists locally'.format())
                    else:
                        logger.info(f'The file does not exist locally, need to download'.format())
                        audio = ydl.extract_info(yt_link, download=True)
                        # Rename the file
                        logger.info(f"Renaming file {filename} to {filename2}".format())
                        os.rename(filename, filename2)
                    logger.info(f"Processing with Mega: {filename2}".format())
                    link = manage_downloads(filename2, m)
                    if os.path.isfile(filename2):
                        os.remove(filename2)
                        logger.info(f'local file has been deleted'.format())
                    else:
                        logger.info(f'file to be deleted does not exist'.format())
                    return link
                else:
                    return filecheck
        except:
            return "Error, Server error has occurred"
