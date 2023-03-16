import flet as ft

from youtube_archiver.util.Logger import Logger
from youtube_archiver.util.progress_hook import main_hook


class YouTubeArchiver(ft.UserControl):
    YTDL_OPT = {
        'progress_hooks': [main_hook],
        'logger': Logger()
    }

    def __init__(self):
        super().__init__()

        self.video_list = None

        self.download_url = None
        self.download_btn = None

    def build(self):
        self.video_list = ft.ListView(expand=1, spacing=0, padding=0, auto_scroll=True)

        self.download_url: ft.TextField = ft.TextField(hint_text='YouTube URL',
                                                       expand=True, on_submit=self.download_clicked)
        self.download_btn: ft.IconButton = ft.IconButton(ft.icons.DOWNLOAD, on_click=self.download_clicked)

        return ft.Column(
            width=400,
            height=800,
            controls=[
                ft.Row(
                    width=390,
                    controls=[
                        self.download_url,
                        self.download_btn
                    ]
                ),
                self.video_list
            ]
        )

    def download_clicked(self, e):
        url: str = self.download_url.value

        if url.replace(' ', '') == '':
            self.page.snack_bar = ft.SnackBar(ft.Text('URL is empty!'))
            self.page.snack_bar.open = True
            self.page.update()
            return
        elif not url.startswith('https://www.youtube.com/watch?v=') and not url.startswith('https://youtu.be/'):
            self.page.snack_bar = ft.SnackBar(ft.Text('URL is not youtube!'))
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.download_url.value = ''
        self.page.update()

