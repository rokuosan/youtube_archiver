import flet as ft


class Video(ft.UserControl):
    def __init__(self, title: str, thumbnails: str):
        super().__init__()
        self.title = title
        self.thumbnails = thumbnails
        self.progress = ft.Text('')
        self.indicator = ft.ProgressBar(width=200)
        self.indicator.value = 0

    def build(self):
        if self.thumbnails == '':
            icon = ft.Icon(ft.icons.MUSIC_NOTE, size=64)
        else:
            icon = ft.Image(src=self.thumbnails, width=64, height=64, fit=ft.ImageFit.CONTAIN)

        return ft.Row(
            controls=[
                icon,
                ft.Column(
                    controls=[
                        ft.Text(self.title),
                        ft.Column([self.progress, self.indicator])
                    ]
                )
            ]
        )
