import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import datetime as dt

print("Model eğitim işlemi başlıyor...")

try:
    print("Excel dosyası yükleniyor...")
    try:
        df = pd.read_excel("OnlineRetail.xlsx")
    except:
        df = pd.read_excel("Online Retail.xlsx")
    
    print("Excel dosyası başarıyla yüklendi. Satır sayısı:", df.shape[0])
    
    print("Null değerler siliniyor...")
    df.dropna(subset=['CustomerID'], inplace=True)
    print("Null değerler silindikten sonra veri boyutu:", df.shape)
    
    df = df[df['Country'] == 'United Kingdom']
    print("İngiltere filtresi uygulandıktan sonra veri boyutu:", df.shape)
    
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    analiz_tarihi = df['InvoiceDate'].max() + dt.timedelta(days=1)
    print("Analiz tarihi:", analiz_tarihi)
    
    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (analiz_tarihi - x.max()).days,
        "InvoiceNo": "nunique",
        "TotalPrice": "sum"
    })
    
    rfm.columns = ["Recency", "Frequency", "Monetary"]
    print("RFM veri boyutu:", rfm.shape)
    
    print("Veriler standartlaştırılıyor...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])
    
    print("KMeans modeli eğitiliyor...")
    model = KMeans(n_clusters=5, random_state=42, n_init=10)
    model.fit(X_scaled)
    
    print("Model başarıyla eğitildi!")
    
    rfm['Cluster'] = model.labels_
    for i in range(5):
        cluster_data = rfm[rfm['Cluster'] == i]
        print(f"Cluster {i} - Ortalama değerler:")
        print(f"   Recency: {cluster_data['Recency'].mean():.2f} gün")
        print(f"   Frequency: {cluster_data['Frequency'].mean():.2f} sipariş")
        print(f"   Monetary: £{cluster_data['Monetary'].mean():.2f}")
        print(f"   Müşteri Sayısı: {cluster_data.shape[0]}")
    
    print("Model ve scaler kaydediliyor...")
    with open("kmeans_model.pkl", 'wb') as f:
        pickle.dump(model, f)
    with open("scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Eğitim tamamlandı, model ve scaler başarıyla kaydedildi.")

except Exception as e:
    print(f"Hata oluştu: {str(e)}")
