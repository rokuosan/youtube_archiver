import flet as ft

settings = {
    # 優先する言語 詳細はここから
    # https://github.com/yt-dlp/yt-dlp/blob/c26f9b991a0681fd3ea548d535919cec1fbbd430/yt_dlp/extractor/youtube.py#L381-L390
    'language': 'ja',
    # 最大コメント数
    'max_comments': [0, 0, 0, 0],
    # 取得するフォーマット
    # 'format': 'bestvideo*+bestaudio/best',  # これはyt-dlp標準
    'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',
    # 出力ファイル名
    'output_template': '%(title)s [%(id)s].%(ext)s',
    'audio_only': False,
}


def get_prop(prop: str) -> str:
    if prop in settings:
        return settings[prop]
    else:
        return ''


class SettingDialog(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.language = ft.TextField(label='Language', hint_text='ja', value=settings['language'])
        self.format = ft.TextField(label='format', hint_text=settings['format'], value=settings['format'])
        self.template = ft.TextField(label='Output Template', hint_text=settings['output_template'],
                                     value=settings['output_template'])
        self.audio = ft.Checkbox(label='Audio Only Mode', value=settings['audio_only'])

        self.content = ft.Column(
            height=400,
            controls=[
                self.language,
                self.format,
                self.template,
                self.audio
            ]
        )

        self.dialog = ft.AlertDialog(
            title=ft.Text('Settings'),
            on_dismiss=self.close,
            content=self.content,
            actions=[
                ft.TextButton('OK', on_click=self.close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=5)
        )

    def build(self) -> ft.AlertDialog:
        return self.dialog

    def show(self):
        self.dialog.open = True
        self.update()

    def close(self, e):
        settings['audio_only'] = self.audio.value
        settings['language'] = self.language.value
        settings['format'] = self.format.value
        settings['output_template'] = self.template.value

        self.dialog.open = False
        self.update()
