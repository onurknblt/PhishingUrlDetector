import streamlit as st
import pickle
from feature import FeatureExtraction

# Modeli yükle
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("URL Tahmin Uygulaması")
st.write("Bir URL girin ve modelin tahminini görün:")

# Kullanıcıdan URL al
url_input = st.text_input("URL girin (örn: https://example.com)")

if st.button("Tahmin Et"):
    if url_input:
        try:
            # Özellikleri çıkar
            features_obj = FeatureExtraction(url_input)
            features = features_obj.getFeaturesList()

            # Model tahmini
            prediction = model.predict([features])
            st.success(f"Tahmin: {prediction[0]}")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
    else:
        st.warning("Lütfen bir URL girin.")
