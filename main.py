import time
import math
from collections import Counter

class KaotikYorungeRNG:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time() * 1000)
        
        # 64-bit maskeleme için
        self.MASK = 0xFFFFFFFFFFFFFFFF
        
        # Büyük asal sabitler (Hex formatında)
        self.ASAL_1 = 0x9E3779B97F4A7C15
        self.ASAL_2 = 0xBF58476D1CE4E5B9
        
        # Durum değişkenlerini başlat
        self.x = seed & self.MASK
        self.y = (seed * self.ASAL_1) & self.MASK
        self.z = ((seed ^ self.ASAL_2) + self.x) & self.MASK

    def _rol(self, val, shift):
        """Bitwise Rotate Left (Sola Döndürme)"""
        shift %= 64
        return ((val << shift) & self.MASK) | (val >> (64 - shift))

    def next_int(self):
        """Rastgele 64-bit tamsayı üretir"""
        tmp_x = self.x
        
        # 1. Dinamik Yörünge Kaydırma
        shift_amount = self.y & 63
        self.x = self._rol(self.x, shift_amount) ^ self.z
        
        # 2. Kaotik Karıştırma
        self.y = ((self.y ^ self.z) * self.ASAL_2) & self.MASK
        
        # 3. Geri Besleme
        self.z = ((self.z + tmp_x) * self.ASAL_1) & self.MASK
        
        # Sonuç
        result = (self.x + self.y + self.z) & self.MASK
        return result

# --- İSTATİSTİKSEL TEST FONKSİYONLARI ---

def bit_dagilimi_testi(sayilar):
    """
    0 ve 1'lerin dağılımını (Monobit Test benzeri) kontrol eder.
    Amaç: %50'ye ne kadar yakın?
    """
    toplam_bit = 0
    birler = 0
    
    for sayi in sayilar:
        binary = bin(sayi)[2:].zfill(64) # 64 bite tamamla
        toplam_bit += 64
        birler += binary.count('1')
        
    oran = (birler / toplam_bit) * 100
    return toplam_bit, birler, oran

def ki_kare_testi(sayilar):
    """
    Sayilarin dağılımının rastgele olup olmadığını ölçer.
    Burada sayıları mod 256 ile byte'lara bölüp dağılıma bakacağız.
    """
    gozlenen = Counter()
    toplam_ornek = len(sayilar)
    
    # Sayıları 0-255 arasına indirge (mod 256)
    for sayi in sayilar:
        gozlenen[sayi % 256] += 1
        
    beklenen = toplam_ornek / 256
    ki_kare_degeri = 0
    
    for i in range(256):
        fark = gozlenen[i] - beklenen
        ki_kare_degeri += (fark * fark) / beklenen
        
    return ki_kare_degeri

def entropi_hesapla(sayilar):
    """Shannon Entropisi: Rastgelelik miktarını ölçer (Max: 8 bit)"""
    toplam = len(sayilar)
    frekanslar = Counter([s % 256 for s in sayilar])
    
    entropi = 0
    for count in frekanslar.values():
        p_x = count / toplam
        entropi += - p_x * math.log2(p_x)
        
    return entropi

# --- ANA PROGRAM VE RAPORLAMA ---

if __name__ == "__main__":
    print("--- KAOTİK YÖRÜNGE KAYDIRMA (COS) ALGORİTMASI TESTİ ---\n")
    
    # 1. Üreteci Başlat
    rng = KaotikYorungeRNG(seed=123456) # Sabit seed ile test edilebilirliği sağla
    
    # 2. Veri Üretimi (Test için 100.000 sayı üretelim)
    URETIM_MIKTARI = 100000
    print(f"{URETIM_MIKTARI} adet rastgele sayı üretiliyor...")
    
    sayilar = []
    for _ in range(URETIM_MIKTARI):
        sayilar.append(rng.next_int())
        
    # 3. Örnek Çıktılar (İlk 5 tanesi)
    print("\n[ÖRNEK ÇIKTILAR]")
    print(f"{'Sıra':<5} | {'Hex Değer':<20} | {'Decimal Değer'}")
    print("-" * 50)
    for i in range(5):
        print(f"{i+1:<5} | {hex(sayilar[i]):<20} | {sayilar[i]}")

    # 4. İstatistiksel Test Sonuçları
    print("\n--- İSTATİSTİKSEL ANALİZ RAPORU ---")
    
    # A) Bit Dağılımı (0-1 Eşitliği)
    toplam, birler, oran = bit_dagilimi_testi(sayilar)
    print(f"\n1) BIT DAĞILIMI TESTİ (0-1 Eşitliği):")
    print(f"   Toplam Bit: {toplam}")
    print(f"   '1' Sayısı: {birler}")
    print(f"   Oran      : %{oran:.4f}")
    if 49.9 < oran < 50.1:
        print("   SONUÇ     : MÜKEMMEL (0 ve 1'ler neredeyse eşit)")
    else:
        print("   SONUÇ     : KABUL EDİLEBİLİR")

    # B) Entropi
    ent = entropi_hesapla(sayilar)
    print(f"\n2) SHANNON ENTROPİSİ:")
    print(f"   Değer     : {ent:.5f} bit (İdeal: 8.0 bit)")
    if ent > 7.99:
        print("   SONUÇ     : YÜKSEK RASTGELELİK")
    
    # C) Ki-Kare Testi
    ki_kare = ki_kare_testi(sayilar)
    print(f"\n3) Kİ-KARE (CHI-SQUARE) TESTİ:")
    print(f"   Değer     : {ki_kare:.2f}")
    # Serbestlik derecesi 255 için %95 güven aralığı yaklaşık 210-300 arasıdır (basitleştirilmiş)
    # Değer ne kadar düşükse (aşırı düşük olmamak kaydıyla) dağılım o kadar düzgündür.
    print("   Yorum     : Değer 255 civarında olmalıdır. Çok yüksekse rastgelelik bozulur.")
    
    print("\n--- TEST SONU ---")
