from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pickle
import numpy as np
from pydantic import BaseModel
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

app = FastAPI(title="RFM Müşteri Segmentasyonu")

os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

MODEL_YOLU = "kmeans_model.pkl"
SCALER_YOLU = "scaler.pkl"

try:
    with open(MODEL_YOLU, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_YOLU, 'rb') as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    print("Model dosyaları bulunamadı. Yeni model oluşturuluyor...")
    
    try:
        df = pd.read_excel("OnlineRetail.xlsx")
        df.dropna(subset=['CustomerID'], inplace=True)
        df = df[df['Country'] == 'United Kingdom']
        
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        
        import datetime as dt
        analiz_tarihi = df['InvoiceDate'].max() + dt.timedelta(days=1)
        
        rfm = df.groupby("CustomerID").agg({
            "InvoiceDate": lambda x: (analiz_tarihi - x.max()).days,
            "InvoiceNo": "nunique",
            "TotalPrice": "sum"
        })
        
        rfm.columns = ["Recency", "Frequency", "Monetary"]
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])
        
        model = KMeans(n_clusters=5, random_state=42)
        model.fit(X_scaled)
        
        with open(MODEL_YOLU, 'wb') as f:
            pickle.dump(model, f)
        with open(SCALER_YOLU, 'wb') as f:
            pickle.dump(scaler, f)
    except Exception as e:
        print(f"Model oluşturma hatası: {e}")
        
        sample_data = np.array([[10, 5, 1000], [5, 10, 5000], [100, 2, 500], 
                               [20, 3, 2000], [15, 4, 1500]])
        
        scaler = StandardScaler()
        scaled_sample_data = scaler.fit_transform(sample_data)
        
        model = KMeans(n_clusters=5, random_state=42)
        model.fit(scaled_sample_data)
        
        try:
            with open(MODEL_YOLU, 'wb') as f:
                pickle.dump(model, f)
            with open(SCALER_YOLU, 'wb') as f:
                pickle.dump(scaler, f)
            print("Örnek veri ile model oluşturuldu ve kaydedildi")
        except Exception as e:
            print(f"Örnek model kaydetme hatası: {e}")

class MusteriVerisi(BaseModel):
    recency: int
    frequency: int
    monetary: float

KUME_ACIKLAMALARI = {
    0: "Uykudaki Müşteriler - Düşük frequency, yüksek recency (inaktif), düşük monetary değer",
    1: "Aktif Düzenli Müşteriler - Orta frequency, düşük recency (yakın zamanda), orta monetary değer",
    2: "VIP/Şampiyon Müşteriler - Yüksek frequency, çok düşük recency (çok yakın), yüksek monetary değer",
    3: "Risk Altındaki Müşteriler - Orta frequency, orta recency, orta monetary değer",
    4: "Kayıp Müşteriler - Düşük frequency, çok yüksek recency (uzun süredir inaktif), düşük monetary değer"
}

@app.get("/", response_class=HTMLResponse)
async def anasayfa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/")
async def tahmin_et(musteri: MusteriVerisi):
    try:
        veri = np.array([[musteri.recency, musteri.frequency, musteri.monetary]])
        
        olcekli_veri = scaler.transform(veri)
        
        kume = model.predict(olcekli_veri)[0]
        
        return {
            "kume": int(kume),
            "aciklama": KUME_ACIKLAMALARI.get(int(kume), "Bilinmeyen Segment"),
            "musteri_verileri": {
                "recency": musteri.recency,
                "frequency": musteri.frequency,
                "monetary": musteri.monetary
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

@app.post("/predict_form/", response_class=HTMLResponse)
async def form_tahmin(
    request: Request,
    recency: int = Form(...),
    frequency: int = Form(...),
    monetary: float = Form(...)
):
    try:
        veri = np.array([[recency, frequency, monetary]])
        
        olcekli_veri = scaler.transform(veri)
        
        kume = model.predict(olcekli_veri)[0]
        
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request,
                "sonuc": True,
                "kume": int(kume),
                "aciklama": KUME_ACIKLAMALARI.get(int(kume), "Bilinmeyen Segment"),
                "recency": recency,
                "frequency": frequency,
                "monetary": monetary
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request,
                "hata": f"Tahmin hatası: {str(e)}"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 