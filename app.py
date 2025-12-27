# ==============================
# DERS NOTU ANALİZ ASİSTANI - CLOUD VERSİYONU (GÜNCEL)
# ==============================

import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib

# Çevre değişkenlerini yükle
load_dotenv()

# API Ayarları
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Sayfa Ayarları
st.set_page_config(
    page_title="🎓 Ders Notu Asistanı",
    page_icon="📚",
    layout="wide"
)

st.title("🎓 Ders Notu Analiz Asistanı - Cloud")
st.markdown("---")

# ==============================
# SİSTEM BAŞLATMA
# ==============================

@st.cache_resource
def initialize_clients():
    """API istemcilerini başlat"""
    
    with st.spinner("🔧 Sistem başlatılıyor..."):
        
        # Groq Client
        st.info("🤖 Groq AI bağlantısı kuruluyor...")
        try:
            groq_client = Groq(api_key=GROQ_API_KEY)
            st.success("✅ Groq hazır!")
        except Exception as e:
            st.error(f"❌ Groq hatası: {e}")
            st.stop()
        
        # Qdrant Client
        st.info("📊 Qdrant veritabanına bağlanılıyor...")
        try:
            qdrant_client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
            )
            
            # Collection oluştur (yoksa)
            collection_name = "ders_notlari"
            collections = qdrant_client.get_collections().collections
            collection_exists = any(c.name == collection_name for c in collections)
            
            if not collection_exists:
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
            
            st.success("✅ Qdrant hazır!")
            return groq_client, qdrant_client, collection_name
            
        except Exception as e:
            st.error(f"❌ Qdrant hatası: {e}")
            st.stop()

# İstemcileri başlat
groq_client, qdrant_client, collection_name = initialize_clients()

st.markdown("---")

# ==============================
# YARDIMCI FONKSİYONLAR
# ==============================

def create_embedding(text):
    """Basit hash tabanlı embedding (demo için)"""
    hash_obj = hashlib.sha256(text.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # 384 boyutlu vektör oluştur
    embedding = []
    for i in range(384):
        embedding.append(((hash_int >> i) & 1) * 2 - 1)
    
    return embedding

def search_knowledge(query_text, limit=3):
    """Bilgi tabanında arama yap"""
    try:
        query_vector = create_embedding(query_text)
        
        results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit
        )
        
        contexts = []
        if hasattr(results, 'points'):
            for point in results.points:
                if hasattr(point, 'payload') and 'text' in point.payload:
                    contexts.append(point.payload['text'])
        
        return contexts
    except Exception as e:
        st.error(f"Arama hatası: {e}")
        return []

def ask_groq(question, contexts):
    """Groq AI'dan cevap al"""
    
    # Context'leri birleştir
    context_text = "\n\n".join(contexts) if contexts else "Bilgi bulunamadı."
    
    # Prompt oluştur
    prompt = f"""Sen bir ders notu asistanısın. Aşağıdaki ders notlarına dayanarak soruyu cevapla.

DERS NOTLARI:
{context_text}

SORU: {question}

CEVAP (sadece Türkçe, notlara dayanarak):"""
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Sen yardımcı bir ders notu asistanısın. Sadece verilen notlara dayanarak Türkçe cevap veriyorsun."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Groq hatası: {str(e)}"

# ==============================
# PDF YÜKLEME (Admin Panel)
# ==============================

with st.sidebar:
    st.header(" Ders Notu Yükle")
    
    uploaded_file = st.file_uploader("PDF yükle", type=['pdf'])
    
    if uploaded_file and st.button("Yükle ve Analiz Et"):
        with st.spinner("PDF işleniyor..."):
            try:
                # PDF'i oku
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                
                text_chunks = []
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        # Metin parçalarına böl (500 karakter)
                        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                        text_chunks.extend(chunks)
                
                # Qdrant'a kaydet
                points = []
                for idx, chunk in enumerate(text_chunks):
                    vector = create_embedding(chunk)
                    point = PointStruct(
                        id=hash(chunk + str(idx)) % (10 ** 8),  # Unique ID
                        vector=vector,
                        payload={"text": chunk, "source": uploaded_file.name}
                    )
                    points.append(point)
                
                qdrant_client.upsert(
                    collection_name=collection_name,
                    points=points
                )
                
                st.success(f"✅ {len(text_chunks)} metin parçası yüklendi!")
                
            except Exception as e:
                st.error(f"❌ Yükleme hatası: {e}")
    
    st.markdown("---")
    st.caption(" İlk kullanımda PDF yüklemelisiniz")

# ==============================
# CHAT ARAYÜZÜ
# ==============================

st.markdown("### 💬 Asistanınıza Soru Sorun")

# Chat geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı inputu
if prompt := st.chat_input("Sorunuzu yazın..."):
    
    # Kullanıcı mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Asistan cevabı
    with st.chat_message("assistant"):
        with st.spinner("🔍 Notlarda arıyorum..."):
            
            # Bilgi tabanında ara
            contexts = search_knowledge(prompt)
            
            # Groq'tan cevap al
            answer = ask_groq(prompt, contexts)
            
            st.markdown(answer)
            
            # Kaydet
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer
            })

# ==============================
# YAN PANEL - BİLGİ
# ==============================
with st.sidebar:
    st.markdown("---")
    st.header(" Kullanım Kılavuzu")
    
    st.markdown("""
    **Adımlar:**
    1. Sol panelden PDF yükleyin
    2. Soru sorun
    3. AI notlardan bilgi bulup cevaplar
    
    **Örnek Sorular:**
    - "Python nedir?"
    - "Döngüler nasıl çalışır?"
    - "Fonksiyon örnekleri ver"
    """)
    
    st.markdown("---")
    
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    
