# Kaotik Yörünge Kaydırma (COS) – Rastgele Sayı Üreteci  
*(Chaotic Orbit Shift Random Number Generator)*

Bu proje, **Bilgi Sistemleri Güvenliği** dersi kapsamında geliştirilmiş özgün bir  
**Rastgele Sayı Üreteci (RSÜ)** algoritmasıdır.

---

## 1. Algoritmanın Mantığı ve Çalışma Prensibi

Geliştirilen **COS (Chaotic Orbit Shift)** algoritması, doğrusal olmayan dinamik
sistemlerden ve **kaos teorisinden** esinlenmiştir. Standart algoritmaların
(örneğin LCG) aksine, bu algoritma tahmin edilebilirliği zorlaştırmak için
üç farklı **yörünge değişkeni (X, Y, Z)** kullanır.

### Algoritmanın temel yenilikleri:

- **Dinamik Bit Kaydırma:**  
  `X` değişkeninin sola döndürme miktarı sabit değildir; o anki  
  `Y mod 64` değerine göre her adımda değişir. Bu durum periyodik tekrarları engeller.

- **Çapraz Bağımlılık (Cross-Dependency):**  
  Değişkenler birbirini XOR, toplama ve çarpma gibi farklı matematiksel işlemlerle etkiler.  
  `X` değişkeni `Z`’den, `Y` değişkeni `X`’ten etkilenir.

- **Kaotik Sabitler:**  
  Altın oran (φ) ve irrasyonel sayılardan türetilmiş 64-bitlik büyük asal sabitler
  kullanılarak sayı uzayında homojen dağılım sağlanır.

---
## 2. Sözde Kod (Pseudocode)

```text
BAŞLAT
    GİRDİ: tohum (seed)
    SABİTLER:
        ASAL_1 = 0x9E3779B97F4A7C15
        ASAL_2 = 0xBF58476D1CE4E5B9

    X = tohum
    Y = (tohum * ASAL_1)
    Z = (tohum XOR ASAL_2) + X

    FONKSİYON RastgeleSayiUret():
        gecici_x = X

        donme_miktari = Y MOD 64
        X = (X SOLA_DÖNDÜR donme_miktari) XOR Z

        Y = ((Y XOR Z) * ASAL_2)
        Z = ((Z + gecici_x) * ASAL_1)

        SONUC = (X + Y + Z)
        DÖNDÜR SONUC
    SON
BİTİR
```

---

## 3. Akış Şeması (Flowchart)

Algoritmanın döngüsel yapısını gösteren şema aşağıdadır:

![Akış Şeması](https://raw.githubusercontent.com/Yusufarkn/Bilgi_Sistemleri_Guveligi_RSU/main/sema.png)

---

## 4. İstatistiksel Testler ve Güvenlik Analizi

Algoritmanın ürettiği sayıların rastgeleliğini doğrulamak için `main.py`
dosyası içerisinde aşağıdaki testler otomatik olarak yapılmaktadır:

### 🔹 Bit Dağılımı Testi (0–1 Eşitliği)
- Üretilen bitlerin %50’sinin `0`, %50’sinin `1` olması hedeflenir.  
- **Başarım Kriteri:** %49.9 – %50.1 aralığı

### 🔹 Shannon Entropisi
- Bilgi düzensizliğini ölçer.  
- 8-bit örnekleme için maksimum değer **8.0**’dır.  
- **Başarım Kriteri:** 7.99 üzeri

### 🔹 Ki-Kare (Chi-Square) Testi
- Dağılımın **uniform (eşit)** olup olmadığını ölçer.  
- Serbestlik derecesine yakın değerler, rastgeleliği destekler.

---

## 5. Örnek Çalışma Çıktısı ve Kanıt

Aşağıdaki çıktı, testlerin başarıyla geçtiğini göstermektedir:

![Test Sonuçları](https://raw.githubusercontent.com/Yusufarkn/Bilgi_Sistemleri_Guveligi_RSU/main/kanit.png)
