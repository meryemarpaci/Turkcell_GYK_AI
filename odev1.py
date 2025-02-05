## Banka Hesap Yönetimi

class Hesap:
    def __init__(self,hesap_sahibi,hesapNo, bakiye=0):
        self.hesap_sahibi = hesap_sahibi
        self.hesapNo=hesapNo
        self.__bakiye=bakiye

    def para_yatir(self, tutar):
        if tutar>0:
            self.__bakiye+=tutar
            print(tutar," TL yatırıldı. Mevcut Bakiyeniz:",self.__bakiye)
        else:
            print("geçersiz miktar, 0'dan küçük tutar yatırılamaz!") 

    def para_cek(self, tutar):
        if 0<tutar >= self.__bakiye:
            print("Yetersiz bakiye! Mevcut bakiyeniz: ",tutar)
        elif 0>tutar:
            print("Geçersiz bakiye") 
        else:
            self.__bakiye-=tutar  
            print(tutar,"TL Çekildi. Mevcut bakiyeniz: ",tutar) 

    def bakiye_goster(self):
        print()        
    def bakiye_getter(self):
        return self.__bakiye
    
class Vadesiz(Hesap):
    pass  
class Vadeli(Hesap):
    def __init__(self,sahip,hesapNo,bakiye=0,faizMiktari=0.2):
        super().__init__(sahip,hesapNo,bakiye)
        self.faizMiktari=faizMiktari  
    def faizHesapla(self):
        faiz=self.bakiye_getter() * self.faizMiktari
        print("yüzde ",self.faizMiktari*100,"faiz uygulandı.")
        return faiz
    def paraCek(self, miktar):
        super().para_cek(miktar)

a= Vadesiz("meryem","123",1000)
a.bakiye_goster()
a.para_yatir(350)
a.para_cek(10850)
a.bakiye_goster


## Kütüphane Yönetim Sistemi

class Kitap:
    def __init__(self, ad, yazar, sayfaNo, isbn):
        self.__ad = ad
        self.__yazar = yazar
        self.__sayfaNo = sayfaNo
        self.__isbn = isbn
    
    def getter_ad(self):
        return self.__ad
    
    def getter_yazar(self):
        return self.__yazar
    
    def getter_sayfaNo(self):
        return self.__sayfaNo
    
    def getter_isbn(self):
        return self.__isbn
    
    def __str__(self):
        return f"{self.__ad} - {self.__yazar} ({self.__sayfaNo} sayfa) - ISBN: {self.__isbn}"
    
class Kutuphane:
    def __init__(self):
        self.__kitaplar = {}
    
    def kitap_ekle(self, kitap):
        if kitap.get_isbn() in self.__kitaplar:
            raise Exception("bu kitap zaten kütüphanede mevcut!")
        self.__kitaplar[kitap.get_isbn()] = kitap
        print(kitap.get_ad(), " isimli kitap eklendi")
    
    def kitap_sil(self, isbn):
        if isbn not in self.__kitaplar:
            raise Exception("Silinmek istenen kitap bulunamadı!")
        silinen_kitap = self.__kitaplar.pop(isbn)
        print(silinen_kitap.get_ad()," isimli kitap silindi")
    
    def kitaplari_goster(self):
        if not self.__kitaplar:
            print("Kütüphane boş.")
        else:
            for kitap in self.__kitaplar.values():
                print(kitap)    


kutuphane = Kutuphane()
kitap1 = Kitap("Simyacı", "abc", 123, "1234")
kitap2 = Kitap("deneme", "ali", 132, "0987")

try:
    kutuphane.kitap_ekle(kitap1)
    kutuphane.kitap_ekle(kitap2)
    kutuphane.kitap_ekle(kitap1)  
except Exception as e:
    print("hata:", e)

kutuphane.kitaplari_goster()

try:
    kutuphane.kitap_sil("1234")
    kutuphane.kitap_sil("1111111111")  # Var olmayan bir kitabı silmeye çalışınca hata verecek
except Exception as e:
    print("Hata:", e)

kutuphane.kitaplari_goster()            