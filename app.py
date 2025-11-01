import os
import json
import requests
from google.auth.transport.requests import Request
from googletrans import Translator
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Haberleri NewsAPI'den Çekmek için API Ayarları
NEWS_API_KEY = "APP_NEWS_API_KEY"
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&language=en&pageSize=5&apiKey={NEWS_API_KEY}"

# Blogger API Ayarları
BLOG_ID = "APP_BLOG_ID"
SHARED_NEWS_FILE = "/storage/emulated/0/Download/shared_news.json"  # Paylaşılan haberlerin kaydedileceği dosya

# Yetkilendirme için Gerekli Kapsamlar
SCOPES = ['https://www.googleapis.com/auth/blogger']

# Google Translate ile Çeviri
def translate_text(text, target_language='tr'):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Haberleri NewsAPI'den Çekme
def fetch_news():
    response = requests.get(NEWS_API_URL)
    if response.status_code == 200:
        data = response.json()
        print("API Yanıtı:", data)  # API yanıtını yazdırarak kontrol et
        return data.get("articles", [])
    else:
        print("Haberler alınamadı:", response.text)
        return []

# Paylaşılan Haberleri Yükleme
def load_shared_news():
    if os.path.exists(SHARED_NEWS_FILE):
        with open(SHARED_NEWS_FILE, "r") as file:
            shared_news = json.load(file)
            print(f"Yüklenen haberler: {shared_news}")
            return shared_news
    else:
        # Dosya yoksa boş bir dosya oluştur
        with open(SHARED_NEWS_FILE, "w") as file:
            json.dump([], file)
            print(f"{SHARED_NEWS_FILE} dosyası oluşturuldu.")
        return []

# Yeni Paylaşılan Haberleri Kaydetme
def save_shared_news(shared_news):
    with open(SHARED_NEWS_FILE, "w") as file:
        json.dump(shared_news, file)
        print(f"Kaydedilen haberler: {shared_news}")

# Blogger'da Gönderi Paylaşma
def post_to_blogger(service, title, content, image_url=None):
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }

    if image_url:
        body["content"] += f'<img src="{image_url}" alt="Image">'
    
    post = service.posts().insert(blogId=BLOG_ID, body=body).execute()
    print(f"Başlık: '{post['title']}' başarıyla paylaşıldı.")

# Yetkilendirme (credentials.json üzerinden)
def authenticate_blogger():
    creds = None
    client_json_path = "/storage/emulated/0/Download/credentials.json"  # credentials.json dosyasının tam yolu

    # Dosyanın mevcut olup olmadığını kontrol et
    if not os.path.exists(client_json_path):
        print(f"Dosya bulunamadı: {client_json_path}")
        return None

    # Token dosyası yoksa kimlik doğrulama yap
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_json_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Token'ı kaydet
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("blogger", "v3", credentials=creds)

# Ana Program
if __name__ == "__main__":
    # Yetkilendirme
    blogger_service = authenticate_blogger()

    if blogger_service:
        # Daha önce paylaşılan haberleri yükle
        shared_news = load_shared_news()

        # Haberleri Çekme
        articles = fetch_news()
        if not articles:
            print("Haber bulunamadı.")
        else:
            for article in articles:
                title = article.get("title", "Başlıksız Haber")
                description = article.get("description", "Açıklama yok.")
                url = article.get("url", "#")
                image_url = article.get("urlToImage", None)  # Resim URL'si

                # Haberin daha önce paylaşılıp paylaşılmadığını kontrol et
                if url in shared_news:
                    print(f"Daha önce paylaşılan haber atlandı: {title}")
                    continue

                # Çeviri işlemi
                turkish_title = translate_text(title, 'tr')
                turkish_description = translate_text(description, 'tr')
                
                # Türkçe içerik
                turkish_content = f"""
                <h2>{turkish_title}</h2>
                <p>{turkish_description}</p>
                """

                # Blogger'da Paylaşma
                post_to_blogger(blogger_service, turkish_title, turkish_content, image_url)

                # Haberi kaydet
                shared_news.append(url)

        # Paylaşılan haberleri kaydet
        save_shared_news(shared_news)
    else:
        print("Blogger'a bağlanılamadı. Lütfen credentials.json dosyasını kontrol edin.")