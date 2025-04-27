# RFM Müşteri Segmentasyonu Projesi

Bu uygulama, RFM (Recency, Frequency, Monetary) değerlerine dayalı olarak müşteri segmentasyonu yapan bir web uygulaması ve API sunar.

## Özellikler

- **RFM Analizi**: Müşterileri RFM değerlerine göre segmentlere ayırır
- **Web Arayüzü**: Müşteri verilerinin girilmesi için kullanımı kolay form
- **API**: Programatik erişim için REST API
- **KMeans Kümeleme**: Müşteri segmentlerini belirlemek için gelişmiş makine öğrenimi algoritması

## Kurulum

1. Projeyi klonlayın veya indirin
2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

3. Online Retail veri setini (`OnlineRetail.xlsx` veya `Online Retail.xlsx`) proje klasörüne koyun

## Kullanım

### Uygulamayı Çalıştırma

Önce model eğitimini yapın:

```bash
python train_model.py
```

Sonra FastAPI sunucusunu başlatın:

```bash
uvicorn main:app --reload
```

Uygulama http://localhost:8000 adresinde erişilebilir olacaktır.

### Web Arayüzü Kullanımı

- Tarayıcınızda http://localhost:8000 adresine gidin
- Müşterinin RFM değerlerini girin:
  - **Recency**: Son alışverişten bu yana geçen gün sayısı (düşük değer daha iyidir)
  - **Frequency**: Toplam sipariş sayısı (yüksek değer daha iyidir)
  - **Monetary**: Toplam harcama miktarı (yüksek değer daha iyidir)
- "Müşteri Segmentini Tahmin Et" butonuna tıklayın
- Sonuçları görüntüleyin

### API Kullanımı

RFM değerlerini API üzerinden tahmin etmek için `/predict/` endpoint'ine POST isteği gönderebilirsiniz:

```bash
curl -X POST "http://localhost:8000/predict/" \
     -H "Content-Type: application/json" \
     -d '{"recency": 5, "frequency": 10, "monetary": 1500.00}'
```

Yanıt formatı:

```json
{
  "kume": 1,
  "aciklama": "Aktif Düzenli Müşteriler - Orta frequency, düşük recency (yakın zamanda), orta monetary değer",
  "musteri_verileri": {
    "recency": 5,
    "frequency": 10,
    "monetary": 1500.0
  }
}
```

## Müşteri Segmentleri

Uygulama, müşterileri 5 segmente ayırır:

- **Küme 0**: Uykudaki Müşteriler - Düşük frequency, yüksek recency (inaktif), düşük monetary değer
- **Küme 1**: Aktif Düzenli Müşteriler - Orta frequency, düşük recency (yakın zamanda), orta monetary değer
- **Küme 2**: VIP/Şampiyon Müşteriler - Yüksek frequency, çok düşük recency (çok yakın), yüksek monetary değer
- **Küme 3**: Risk Altındaki Müşteriler - Orta frequency, orta recency, orta monetary değer
- **Küme 4**: Kayıp Müşteriler - Düşük frequency, çok yüksek recency (uzun süredir inaktif), düşük monetary değer

## Teknik Detaylar

- **Veri Ön İşleme**: CustomerID null olan kayıtlar temizlenir, sadece UK verileri kullanılır
- **Kümeleme**: KMeans algoritması ile 5 segment oluşturulur
- **Standardizasyon**: RFM değerleri StandardScaler ile normalize edilir

## Eğitim Projesi

Bu uygulama, veri bilimi ve makine öğrenimi kavramlarını pratik bir şekilde öğrenmek için tasarlanmıştır. Öğrenciler bu projeyle:

1. RFM analizi ve müşteri segmentasyonu kavramlarını öğrenebilir
2. Sklearn kütüphanesi ve KMeans algoritmasını pratikte uygulayabilir
3. FastAPI kullanarak model servislerini nasıl oluşturacaklarını deneyimleyebilir
4. Web arayüzü ve API tasarımı konusunda pratik yapabilir

Eğitim amacıyla özgürce kullanabilir ve geliştirebilirsiniz. 