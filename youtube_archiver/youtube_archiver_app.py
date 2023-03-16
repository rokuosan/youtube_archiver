import flet as ft


class YouTubeArchiver(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.video_list = None

        self.download_url = None
        self.download_btn = None

    def build(self):
        self.video_list = ft.ListView(expand=1, spacing=0, padding=0, auto_scroll=True)

        self.download_url = ft.TextField(hint_text='YouTube URL', expand=True)
        self.download_btn = ft.IconButton(ft.icons.DOWNLOAD)

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
