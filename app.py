import streamlit as st
import pickle
from feature import FeatureExtraction
import numpy as np

# --- Sayfa Yapılandırması (Her zaman en başta olmalı) ---
st.set_page_config(
    page_title="Phishing URL Analiz Aracı",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Özel CSS Dosyasını Yüklemek için Fonksiyon ---
def load_css(file_name):
    """
    Belirtilen CSS dosyasını yükler ve Streamlit uygulamasına enjekte eder.
    """
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Stil dosyası '{file_name}' bulunamadı. Lütfen dosyanın doğru yolda olduğundan emin olun.")

# CSS'i yükle
load_css("style.css")

# --- Yan Menü (Sidebar) ---
with st.sidebar:
    # 1. Logo Ekleme
    st.image("C:\Projects\PhishingUrlDetector\.streamlit\logo1.png", width=150)
    st.header("Phishing URL Analiz Aracı")
    st.markdown("""
    Bu uygulama, girdiğiniz bir URL'in 'phishing' (oltalama) amaçlı olup olmadığını tahmin etmek için eğitilmiş bir **XGBoost** modeli kullanır.
    """)
    st.info("Bu model %100 doğruluk garantisi vermez. Sonuç ne olursa olsun, şüpheli linklere karşı her zaman dikkatli olun!")
    

# --- Ana Başlık ve Arayüz ---
st.title("Phishing URL Analiz Aracı 🛡️")
st.markdown("Bir URL'in güvenli olup olmadığını saniyeler içinde öğrenmek için aşağıya yapıştırın.")

# --- Model Yükleme ---
@st.cache_data
def load_model():
    """
    Eğitilmiş makine öğrenmesi modelini yükler.
    @st.cache_data decorator'ı sayesinde model sadece bir kez yüklenir.
    """
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# --- Özellik İsimleri (Analiz detayları için) ---
feature_names = [
    "IP Adresi Kullanımı", "URL Uzunluğu", "URL Kısaltma Servisi", "'@' Sembolü",
    "'//' Yönlendirmesi", "Ön-ek/Son-ek Kullanımı", "Alt Alan Adı Sayısı", "HTTPS Protokolü",
    "Domain Kayıt Süresi", "Favicon", "Standart Dışı Port", "Domainde HTTPS",
    "Request URL", "Anchor URL", "Script Taglerindeki Linkler", "Server Form Handler (SFH)",
    "Bilgilendirme Maili", "Anormal URL", "Website Yönlendirmesi", "Status Bar Değişikliği",
    "Sağ Tık Engelleme", "Popup Pencere Kullanımı", "Iframe Yönlendirmesi", "Domain Yaşı",
    "DNS Kaydı", "Web Sitesi Trafiği", "PageRank", "Google Index",
    "Sayfaya İşaret Eden Linkler", "İstatistik Raporu"
]

# --- Kullanıcı Girişi ve Tahmin ---
url_input = st.text_input("URL'i buraya girin", placeholder="https://www.google.com", label_visibility="collapsed")

if st.button("URL'i Analiz Et"):
    if url_input:
        with st.spinner('URL analiz ediliyor... Bu işlem birkaç saniye sürebilir.'):
            try:
                # Özellikleri çıkar ve modeli beslemek için doğru formata getir
                features_obj = FeatureExtraction(url_input)
                features = np.array(features_obj.getFeaturesList()).reshape(1, -1)
                prediction = model.predict(features)

                # --- Sonuçların Gösterimi ---
                st.write("---")
                st.header("Analiz Sonucu")

                # 2. Sonuçları Metrik Kartları ile Gösterme
                col1, col2 = st.columns([1, 2])
                with col1:
                    if prediction[0] == 1:
                        st.metric(label="URL Durumu", value="Güvenli", delta="Düşük Risk", delta_color="normal")
                    elif prediction[0] == 0:
                        st.metric(label="URL Durumu", value="Şüpheli", delta="Orta Risk", delta_color="inverse")
                    else:
                        st.metric(label="URL Durumu", value="ZARARLI", delta="Yüksek Risk", delta_color="inverse")

                with col2:
                    if prediction[0] == 1:
                        st.success("✅ Bu URL **Güvenli** olarak sınıflandırıldı.")
                        st.info("Yine de bağlantılara tıklarken her zaman dikkatli olmanız önerilir.")
                    elif prediction[0] == 0:
                        st.warning("⚠️ Bu URL **Şüpheli** olarak sınıflandırıldı. Bilinmeyen bir kaynaktan geldiyse açmamanız daha iyi olabilir.")
                    else:
                        st.error("❌ Bu URL **Zararlı (Phishing)** olarak sınıflandırıldı. Bu siteyi kesinlikle ziyaret etmeyin!")

                # --- Analiz Detayları ---
                with st.expander("Analiz Detaylarını Gör"):
                    st.subheader("Modelin Kararını Etkileyen Özellikler:")
                    cols = st.columns(2)
                    for i, name in enumerate(feature_names):
                        icon = "✅" if features[0, i] == 1 else ("⚠️" if features[0, i] == 0 else "❌")
                        (cols[0] if i < len(feature_names) / 2 else cols[1]).markdown(f"{icon} **{name}:** `{features[0, i]}`")

            except Exception as e:
                st.error(f"Analiz sırasında bir hata oluştu: {e}")
                st.info("Lütfen geçerli bir URL girdiğinizden emin olun (örn: https://www.google.com)")
    else:
        st.warning("Lütfen analiz etmek için bir URL girin.")
