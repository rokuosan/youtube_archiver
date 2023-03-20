import re

import flet as ft
import urllib.request

from glob import glob
from yt_dlp import YoutubeDL
from time import sleep

from youtube_archiver.component.SettingDialog import SettingDialog, get_prop
from youtube_archiver.component.Video import Video
from youtube_archiver.util.Logger import Logger


pending_list = {}
download_list = {}


def progress_hook(d):
    info = d['info_dict']
    fid = info['id']
    filename = re.sub(r'[\\/:*?"<>|]+', '-', str(info['title']))
    video: Video

    if fid in download_list:
        video = download_list[fid]
    elif filename in pending_list:
        download_list[fid] = pending_list[filename]
        del pending_list[filename]
        video = download_list[fid]
    else:
        return

    if d['status'] == 'downloading':
        percent = round((float(d['downloaded_bytes']) / float(d['total_bytes_estimate'])) * 100)
        video.progress.value = f"{percent} %"
        video.indicator.value = percent / 100
        video.indicator.update()
    elif d['status'] == 'finished':
        video.progress.value = 'Complete!'
        del download_list[fid]
        video.progress.update()
        video.indicator.visible = False
        video.indicator.update()
        sleep(0.4)
        video.progress.visible = False

    video.progress.update()


class YouTubeArchiver(ft.UserControl):

    def __init__(self):
        super().__init__()

        self.video_list = None

        self.download_url = None
        self.download_btn = None

        self.option_btn = None

        self.dialog = SettingDialog()

    def build(self):
        self.video_list = ft.ListView(expand=1, spacing=0, padding=0, auto_scroll=True)

        self.download_url: ft.TextField = ft.TextField(hint_text='YouTube URL',
                                                       expand=True, on_submit=self.download_clicked)
        self.download_btn: ft.IconButton = ft.IconButton(ft.icons.DOWNLOAD, on_click=self.download_clicked)

        self.option_btn = ft.IconButton(ft.icons.SETTINGS, on_click=self.option_clicked)

        return ft.Column(
            width=400,
            height=800,
            controls=[
                ft.Row(
                    width=390,
                    controls=[
                        self.option_btn,
                        self.download_url,
                        self.download_btn
                    ]
                ),
                self.video_list
            ]
        )

    def download_clicked(self, e):

        if get_prop('audio_only'):
            opt = {
                'progress_hooks': [progress_hook],
                'logger': Logger(),
                'format': 'm4a/bestaudio/best',
                'outtmpl': get_prop('output_template'),
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }]
            }
        else:
            opt = {
                'progress_hooks': [progress_hook],
                'logger': Logger(),
                'format': get_prop('format'),
                'outtmpl': get_prop('output_template')
            }

        # Get URL and clear text field
        url: str = self.download_url.value
        self.download_url.value = ''
        self.page.update()
        self.update()

        # Validation
        if not self.url_validation(url):
            return

        # Download
        with YoutubeDL(opt) as yt:
            info = yt.extract_info(url, download=False)
            thumb_url: str = yt.sanitize_info(info)['thumbnails'].pop()['url']
            title = re.sub(r'[\\/:*?"<>|]+', '-', str(info['title']))

            # Check exists
            files = glob(f"{title}*")
            if len(files) > 0:
                self.page.snack_bar = ft.SnackBar(ft.Text('The video has already downloaded.'))
                self.page.snack_bar.open = True
                self.download_url.value = ''
                self.update()
                self.page.update()
                return

            # Get thumbnails
            urllib.request.urlretrieve(thumb_url, f"{title}.png")

            # Add Video
            video = Video(title, f"{title}.png")
            self.video_list.controls.append(video)
            self.update()

            # Download
            pending_list[title] = video
            print(f'{title}')
            yt.download(url)

    def url_validation(self, url: str) -> bool:
        if url.replace(' ', '') == '':
            self.page.snack_bar = ft.SnackBar(ft.Text('URL is empty!'))
            self.page.snack_bar.open = True
            self.page.update()
            return False
        elif not url.startswith('https://www.youtube.com/watch?v=') and not url.startswith('https://youtu.be/'):
            self.page.snack_bar = ft.SnackBar(ft.Text('URL is not youtube!'))
            self.page.snack_bar.open = True
            self.page.update()
            return False

        return True

    def option_clicked(self, e):
        self.page.dialog = self.dialog
        self.page.update()
        self.dialog.show()
