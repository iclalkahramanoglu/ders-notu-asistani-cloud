# Ders Notu Analiz Asistanı - Cloud

INP121 Projesi - RAG (Retrieval-Augmented Generation) ile Yapay Zeka Destekli Ders Notu Asistanı

## Canlı Demo

**Uygulamayı kullanmak için:** https://ders-notu-asistani-cloud-hutkmrfw4hg72ntuzbcaey.streamlit.app

Herkes bu linkten uygulamaya erişebilir, PDF yükleyip sorular sorabilir!

---

## Proje Hakkında

Bu proje, ders notlarınızı PDF formatında yükleyerek yapay zeka ile sorularınıza anında cevap alabileceğiniz bir asistan uygulamasıdır. 

**RAG Teknolojisi** kullanılarak AI sadece yüklediğiniz notlardan bilgi alır, bu sayede:
- ✅ Güvenilir ve doğru cevaplar
- ✅ Kaynak gösterimi
- ✅ Hallüsinasyon (uydurma) riski minimum

---

## Özellikler

- **PDF Yükleme:** Ders notlarınızı kolayca yükleyin
- **Groq AI:** Llama 3.3 70B modeli ile güçlü cevaplar
- **Akıllı Arama:** Sentence-Transformers ile hassas bilgi bulma
- **Qdrant Cloud:** Bulut tabanlı vektör veritabanı
- **Chat Arayüzü:** Kolay ve kullanıcı dostu sohbet ekranı
- **İstatistikler:** Yüklenen metin sayısı ve kaynak gösterimi
- **Görsel Geri Bildirim:** PDF yükleme başarı animasyonları

---

## Kullanılan Teknolojiler

### AI & ML
- **Groq AI** - Llama 3.3 70B Versatile model
- **Sentence-Transformers** - paraphrase-multilingual-MiniLM-L12-v2
- **PyPDF2** - PDF metin çıkarma

### Veritabanı & Backend
- **Qdrant Cloud** - Vektör veritabanı (384 boyutlu embeddings)
- **Python 3.13+**
- **Streamlit** - Web arayüzü framework'ü

### Deployment
- **Streamlit Cloud** - Ücretsiz hosting
- **GitHub** - Versiyon kontrolü ve kaynak kod

---

## Lokal Kurulum (Opsiyonel)

Projeyi kendi bilgisayarınızda çalıştırmak isterseniz:

### Gereksinimler
- Python 3.10 veya üzeri
- Groq API Key ([console.groq.com](https://console.groq.com))
- Qdrant Cloud hesabı ([cloud.qdrant.io](https://cloud.qdrant.io))

### Kurulum Adımları
```bash
# 1. Repoyu klonlayın
git clone https://github.com/iclalkahramanoglu/ders-notu-asistani-cloud.git
cd ders-notu-asistani-cloud

# 2. Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. .env dosyası oluşturun
nano .env
```

`.env` içeriği:
```
GROQ_API_KEY=your_groq_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```
```bash
# 5. Uygulamayı çalıştırın
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` açılacaktır.

---

## Kullanım

1. **PDF Yükle:** Sol sidebar'dan PDF dosyanızı yükleyin
2. **Bekleyin:** PDF analiz edilip vektör veritabanına kaydedilecek
3. **Soru Sorun:** Chat alanından sorularınızı yazın
4. **Cevap Alın:** AI notlarınızdan ilgili bilgiyi bulup cevap verecek

### Örnek Sorular
- "Bu derste hangi konular işleniyor?"
- "Python'da döngü nedir?"
- "Fonksiyonları örneklerle açıkla"
- "Bölüm 3'teki örnekleri göster"

---

## Proje Mimarisi
Kullanıcı → Streamlit UI → PDF Upload
                ↓
         Sentence Transformers (Embedding)
                ↓
         Qdrant Cloud (Vector DB)
                ↓
         Semantic Search (Benzer metinleri bul)
                ↓
         Groq AI (Llama 3.3 70B)
                ↓
         Cevap → Streamlit UI → Kullanıcı
  
---

## Proje Yapısı
ders-notu-asistani-cloud/
├── app.py                 # Ana uygulama
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Bu dosya
├── .env                  # API anahtarları (lokal, GitHub'a yüklenmez)
└── .gitignore           # Git ignore kuralları
---

## Geliştiriciler

İclal Kahramanoğlu-Sude Kapramcı-Ekrem Efe Çelik-Çağatay Koç
Yeditepe Üniversitesi  
INP121  
Aralık 2024


