# YoutubePlaylistAnalyzer
YouTube oynatma listelerindeki videoların süresini analiz eden ve izleme hızına göre ne kadar sürede tamamlanacağını hesaplayan bir Python uygulaması.

🚀 # Özellikler
✅ YouTube API ile video sürelerini çeker.
✅ Oynatma hızına bağlı olarak tahmini izleme süresini hesaplar (0.5x - 2.0x arası).
✅ Daha önce izlenen videoları hesaba katar.
✅ PyQt6 ile kullanıcı dostu bir arayüz sunar.

📌 Kurulum ve Kullanım
1️⃣ Gerekli Bağımlılıkları Yükleyin
bash
pip install -r requirements.txt
2️⃣ API Anahtarınızı Tanımlayın
Güvenlik nedeniyle, API anahtarınızı doğrudan kodun içinde bırakmamalısınız. Bunun yerine .env dosyasında saklayabilirsiniz:

# Proje klasöründe .env dosyası oluşturun ve içine şunu ekleyin:
# ini
YOUTUBE_API_KEY=your_api_key_here

# Python'da dotenv kütüphanesini yükleyin:
pip install python-dotenv

# API anahtarını kod içinde çağırın:
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
3️⃣ Uygulamayı Çalıştırın
python main.py
