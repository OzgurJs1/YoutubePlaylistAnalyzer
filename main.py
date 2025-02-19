from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSlider, QMessageBox
from PyQt6.QtCore import Qt
import requests
import re

API_KEY = "your_api_key_here"


class PlaylistAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YouTube Playlist Analyzer")


        self.link_label = QLabel("YouTube Playlist Link:")
        self.link_input = QLineEdit()

        self.speed_label = QLabel("Oynatma Hızı:")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(5)  # 0.5x
        self.speed_slider.setMaximum(20)  # 2.0x
        self.speed_slider.setValue(10)  # Default 1.0x
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.valueChanged.connect(self.update_speed_label)

        self.speed_value_label = QLabel("1.0x")

        self.watched_label = QLabel("İzlenen Video Sayısı:")
        self.watched_input = QLineEdit()

        # Calculate Button
        self.calc_button = QPushButton("Hesapla")
        self.calc_button.clicked.connect(self.calculate_time)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_input)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.speed_slider)
        layout.addWidget(self.speed_value_label)
        layout.addWidget(self.watched_label)
        layout.addWidget(self.watched_input)
        layout.addWidget(self.calc_button)

        self.setLayout(layout)

    def update_speed_label(self):
        self.speed_value_label.setText(f"{self.speed_slider.value() / 10:.1f}x")

    def extract_playlist_id(self, url):
        match = re.search(r"list=([a-zA-Z0-9_-]+)", url)
        return match.group(1) if match else None

    def fetch_video_durations(self, playlist_id):
        video_durations = []
        next_page_token = ""

        while True:
            playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}&pageToken={next_page_token}"
            response = requests.get(playlist_url).json()

            video_ids = [item['contentDetails']['videoId'] for item in response.get("items", [])]

            if video_ids:
                video_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={','.join(video_ids)}&key={API_KEY}"
                video_response = requests.get(video_url).json()

                for item in video_response.get("items", []):
                    duration = item["contentDetails"]["duration"]
                    total_seconds = self.parse_duration(duration)
                    video_durations.append(total_seconds)

            next_page_token = response.get("nextPageToken", "")
            if not next_page_token:
                break

        return video_durations

    def parse_duration(self, duration):
        match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        return hours * 3600 + minutes * 60 + seconds

    def calculate_time(self):
        link = self.link_input.text().strip()
        speed = self.speed_slider.value() / 10
        watched_videos = self.watched_input.text().strip()

        if not link:
            QMessageBox.warning(self, "Hata", "Lütfen YouTube oynatma listesi linkini girin!")
            return

        if not watched_videos.isdigit():
            QMessageBox.warning(self, "Hata", "İzlenen video sayısı geçerli bir sayı olmalıdır!")
            return

        playlist_id = self.extract_playlist_id(link)
        if not playlist_id:
            QMessageBox.warning(self, "Hata", "Geçerli bir YouTube oynatma listesi bağlantısı girin!")
            return

        video_durations = self.fetch_video_durations(playlist_id)
        total_videos = len(video_durations)

        if watched_videos.isdigit():
            watched_videos = int(watched_videos)
            if watched_videos > total_videos:
                QMessageBox.warning(self, "Hata", "Bu oynatma listesinde bu kadar video yok!")
                return

        remaining_videos = total_videos - watched_videos
        total_seconds = sum(video_durations[watched_videos:])
        total_minutes = total_seconds / 60
        total_hours = total_minutes / 60
        adjusted_hours = total_hours / speed
        total_days = adjusted_hours / 24

        QMessageBox.information(self, "Sonuç",
                                f"Kalan süre: {adjusted_hours:.2f} saat\nTahmini gün sayısı: {total_days:.2f} gün")


if __name__ == "__main__":
    app = QApplication([])
    window = PlaylistAnalyzer()
    window.show()
    app.exec()
