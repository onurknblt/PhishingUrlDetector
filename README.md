## Phishing URL Detection 🔎 ##



**📌 Giriş**
İnternet hayatımızın vazgeçilmez bir parçası haline geldi. Bununla birlikte kimlik avı (phishing) gibi kötü amaçlı faaliyetler de arttı. Kimlik avcıları sahte web siteleri oluşturarak kullanıcı adı, parola ve diğer kişisel bilgileri çalmaya çalışır.
Bu projede, makine öğrenmesi kullanılarak verilen bir URL’nin güvenli mi yoksa phishing amaçlı mı olduğunu tahmin eden bir sistem geliştirilmiştir.



**🚀 Kurulum**

**Projeyi bilgisayarınıza klonlayın:**
```
git clone https://github.com/kullaniciadiniz/PhishingUrlDetector.git
cd PhishingUrlDetector
```

**venv (sanal ortam) kurunuz ve aktive ediniz**
```
py -m venv venv
venv/Scripts/activate
```

**Gerekli kütüphaneleri yükleyin:**
```
pip install -r requirements.txt
```


**Uygulamayı başlatın:**
```
streamlit run app.py
```



## Klasör yapısı 
```
├── app.py (Uygulama (Streamlit/Flask giriş noktası)
├── feature.py (URL'den 30 özellik çıkaran sınıf)
├── model__training.ipynb (Model eğitimi ve analiz (Jupyter Notebook))
├── model.pkl (Eğitilmiş model (pickle))
├── phishing.csv (Örnek/altyapı veri seti)
├── requirements.txt (Proje bağımlılıkları)
├── README.md 
├── .gitignore (git için hariç tutulanlar)


```




**⚙️ Kullanılan Teknolojiler**
```
Flask         
streamlit       

# WSGI Sunucusu (Production için)
gunicorn       

# Makine Öğrenmesi ve Veri Bilimi
scikit-learn      
pandas           
numpy
matplotlib
seaborn
xgboost       

# Web İşlemleri ve Yardımcılar
beautifulsoup4   
requests        
python-whois
```


**📊 Model Sonuçları**

Eğitim sırasında test edilen makine öğrenmesi algoritmaları:

||ML Model|	Accuracy|  	f1_score|	Recall|	Precision|
|---|---|---|---|---|---|
0|	Gradient Boosting Classifier|	0.974|	0.977|	0.994|	0.986|
1|	CatBoost Classifier|	        0.972|	0.975|	0.994|	0.989|
2|	XGBoost Classifier| 	        0.969|	0.973|	0.993|	0.984|
3|	Multi-layer Perceptron|	        0.969|	0.973|	0.995|	0.981|
4|	Random Forest|	                0.967|	0.971|	0.993|	0.990|
5|	Support Vector Machine|	        0.964|	0.968|	0.980|	0.965|
6|	Decision Tree|      	        0.960|	0.964|	0.991|	0.993|
7|	K-Nearest Neighbors|        	0.956|	0.961|	0.991|	0.989|
8|	Logistic Regression|        	0.934|	0.941|	0.943|	0.927|
9|	Naive Bayes Classifier|     	0.605|	0.454|	0.292|	0.997|

📌 Sonuç: Gradient Boosting Classifier en iyi performansı göstermiştir.



## ✅ Sonuç ##

1. URL tabanlı phishing saldırıları yüksek doğrulukla tespit edilebilir.
2. feature.py içindeki 30 farklı özellik (ör. HTTPS varlığı, domain yaşı, Alexa rank, WHOIS bilgileri vb.) model için önemli girdiler sağlar.
3. Bu proje hem eğitim amaçlı hem de temel bir phishing URL tespit uygulaması olarak kullanılabilir.