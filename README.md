# <img height="30" alt="javascript" src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg"> Blogger Haber Otomasyonu

Bu proje, **NewsAPI’den haberleri çekip** Google Blogger üzerinde otomatik olarak paylaşan bir Python otomasyonudur. Haberler İngilizce çekilir ve **Google Translate ile Türkçeye çevrilir**, ardından Blogger’da paylaşılır. Daha önce paylaşılan haberler tekrar gönderilmez.

---

## 📦 Gereksinimler

- Python 3.10 veya üstü
- Google hesabı
- Blogger blogu
- NewsAPI hesabı
- Gerekli Python kütüphaneleri:

pip install requests googletrans==4.0.0-rc1 google-auth google-auth-oauthlib google-api-python-client

---

## 🔑 API Alımı

### NewsAPI
1. https://newsapi.org/ sitesine üye ol.
2. Hesabına giriş yaptıktan sonra API key oluştur.
3. API key’i kodun başındaki NEWS_API_KEY değişkenine yapıştır:

NEWS_API_KEY = "BURAYA_SENIN_API_KEY"

### Google Blogger API
1. https://console.cloud.google.com/ sitesine git.
2. Yeni bir proje oluştur.
3. Sol menüden APIs & Services > Library’e gir ve Blogger API’yi etkinleştir.
4. APIs & Services > Credentials kısmına gir.
5. Create Credentials > OAuth client ID seç.
   - Application type: Desktop app
   - Bir isim ver ve oluştur.
6. Oluşturulan credentials.json dosyasını indir ve aşağıdaki klasöre koy:

/storage/emulated/0/Download/credentials.json

Not: Eğer farklı bir klasöre koyacaksan, kodda client_json_path değişkenini değiştir.

---

## ⚙️ Dosya Yapısı

project/
│
├─ main.py               # Projenin ana Python dosyası
├─ shared_news.json      # Otomatik oluşturulur; paylaşılan haberlerin URL’lerini tutar
├─ token.json            # Otomatik oluşturulur; Google OAuth token
└─ credentials.json      # Google API için indirdiğin dosya

- shared_news.json ve token.json otomatik oluşturulur.
- credentials.json dosyasını kendin eklemelisin.

---

## 📝 Kullanım

1. Tüm kütüphanelerin yüklü olduğundan emin ol.
2. main.py dosyasını çalıştır:

python main.py

3. İlk çalıştırmada Google hesabın ile OAuth doğrulaması yapman istenir.
4. Program NewsAPI’den haberleri çeker, Türkçeye çevirir ve Blogger’da paylaşır.
5. Daha önce paylaşılan haberler shared_news.json içinde kaydedilir.

---

## ❓ Sık Sorulan Sorular (FAQ)

S1: Python dosyaları GitHub’a nasıl yükleniyor?  
C1: Python dosyaları HTML gibi index.html olarak yüklenmez. GitHub’da .py uzantılı dosya olarak görünür.

Örnek:
main.py
shared_news.json
README.md

- GitHub otomatik olarak .py dosyalarını syntax-highlighted kod olarak gösterir.
- HTML dosyası gibi açılmaz; Python kodu olarak görüntülenir.

S2: Blogger postlarında resimler otomatik yükleniyor mu?  
C2: Kod, urlToImage varsa habere ekler, başka bir dosya yüklemeye gerek yok.

S3: shared_news.json dosyasını silersem ne olur?  
C3: Program tüm haberleri tekrar paylaşır. Bu dosya haberlerin tekrar gönderilmesini önler.

---

## 🔗 Kaynaklar

- https://newsapi.org/
- https://console.cloud.google.com/
- https://developers.google.com/blogger/docs/3.0/using
- https://py-googletrans.readthedocs.io/en/latest/

---

## 🌐 Dil ve Çeviri Ayarları

- Kodda Google Translate ile çeviri yapılır.
- Dil değiştirmek için translate_text fonksiyonundaki target_language parametresini değiştir:

Örnek: Türkçe için
turkish_title = translate_text(title, 'tr')

Diğer örnekler:
- İngilizce: 'en'
- Almanca: 'de'
- Fransızca: 'fr'
- İspanyolca: 'es'

- description ve title alanları aynı şekilde çevirilir.
- Resimler (urlToImage) otomatik olarak Blogger postuna eklenir.

- target_language değerini değiştirerek haberlerin hangi dilde paylaşılacağını ayarlayabilirsin.
