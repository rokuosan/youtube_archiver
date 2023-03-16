import flet as ft
import youtube_archiver_app as yt


def main(page: ft.Page):
    page.title = 'YouTube Archiver'
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    app = yt.YouTubeArchiver()

    page.add(app)

    page.update()


if __name__ == '__main__':
    ft.app(target=main)
