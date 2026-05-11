import random
from datetime import datetime

#araçların özelliklerini ve durumlarını tuttuğumuz temel sınıf
class Vehicle:
    def __init__(self, arac_id, marka, model, kategori, saatlik_fiyat):

#araçların temel kimlik bilgileri
        self.arac_id = arac_id
        self.marka = marka
        self.model = model
        self.kategori = kategori
        self.saatlik_fiyat = saatlik_fiyat
        self.musait_mi = True  # Başlangıçta tüm araçlar kiralanmaya müsait

#araçlara gerçekçilik katmak için özellikler
        self.km = random.randint(100, 25000) # Kilometresi 100 ile 25 bin arası olsun
        # Kategori motor değilse vites otomatik, motorsa sıralı vites
        self.vites = "Otomatik" if kategori != "Motor" else "Sıralı"

# kategori elektrikliyse yakıt elektrik değilse benzin hibrit
        self.yakit = "Elektrikli" if kategori == "Elektrikli" else "Benzin/Hibrit"
        self.hp = random.randint(150, 800) # Beygir gücü
        
# müşterilerin araca verdiği ortalama puanlar 
        self.degerlendirme = round(random.uniform(4.0, 5.0), 1)

# araba kiralandığında veya geri getirildiğinde müsaitlik durumunu değiştirir
    def arac_durumu_guncelle(self, durum):
        self.musait_mi = durum

# araç kullanıldıkça kilometresini artırmak için kullanılan fonksiyon
    def kilometre_guncelle(self, eklenen_km):
        self.km += eklenen_km


# mağaza kısmında satılacak ürünler için sınıf
class Product:
    def __init__(self, p_id, name, price, stock):
        self.p_id = p_id
        self.name = name
        self.price = price
        self.stock = stock # Stok takibi için önemli

# bir aracın kiralanma sürecini temsil eden sınıf
class Rental:
    def __init__(self, kiralama_id, arac, kullanici, saat_suresi, toplam_tutar):
        self.kiralama_id = kiralama_id
        self.arac = arac # hangi araç kiralandı
        self.kullanici = kullanici # kim kiraladı
        self.baslangic_saati = datetime.now() 
        self.bitis_saati = None 
        self.saat_suresi = saat_suresi
        self.toplam_tutar = toplam_tutar
        self.aktif_mi = True 

# süre dolduğunda veya araç teslim edildiğinde çalışacak fonksiyon
    def kiralama_bitir(self):
        self.bitis_saati = datetime.now() # bitiş saatini kaydet
        self.aktif_mi = False # kiralama durumunu bitir
        
# müşteri aracı kullandı rastgele kilometre yapmış oluyor
        kullanilan_km = random.randint(10, 300)
        self.arac.kilometre_guncelle(kullanilan_km) # aracın kilometresine ekle
        self.arac.arac_durumu_guncelle(True) # araç artık müsait
        self.arac.degerlendirme = round(random.uniform(4.0, 5.0), 1) # yeni puanı güncelle
        return kullanilan_km # ekrana "Şu kadar km yol yaptınız" yazdırıyor

# sisteme kayıt olan kullanıcıların bilgilerini tutan sınıf
class User:
    def __init__(self, kullanici_id, ad, sifre, adres):
        self.kullanici_id = kullanici_id
        self.ad = ad
        self.sifre = sifre
        self.adres = adres
        self.bakiye = 1000.0 # yeni üye olan herkese başlangıçta bakiye
        
# kullanıcının işlemlerini listelerde tutuluyor
        self.aktif_kiralamalar = []  # şu an kiraladığı araçlar
        self.kiralama_gecmisi = []   # eskiden kiralayıp teslim ettikleri
        self.siparisler = []         # mağazadan aldığı ürünler

# kullanıcı bir şey satın aldığında ya da kiraladığında parasını düşen fonksiyon
    def bakiye_dus(self, miktar):
        if self.bakiye >= miktar: # parası yetiyorsa
            self.bakiye -= miktar
            return True
        return False # parası yetmiyorsa işlemi reddediyor

# cüzdana para yükleme fonksiyonu
    def bakiye_ekle(self, miktar):
        self.bakiye += miktar


# uygulamanın ana sınıfı
class AppEngine:
    def __init__(self):

# başlangıçta test yapabilmek için sisteme 1 admin ve 1 normal kullanıcı ekledik
        self.users = {
            "admin": User("admin", "Sistem Yöneticisi", "123", "VRX Merkez"),
            "user": User("user", "Örnek Kullanıcı", "123", "İstanbul, İstanbul")
        }
# araç filosunu ve ürünleri başlatırken oluşturuyo
        self.vehicles = self._genis_filo_olustur()
        self.products = self._urunleri_olustur()
        
        self.current_user = None # şu an sisteme giriş yapmış olan kişi
        self.rental_counter = 1000 # kiralama ID'leri 1000'den başlıoı
        self.sistem_kasasi = 0.0 # toplam kazancı burada tutuyoruz

# sistem ilk açıldığında galeriyi dolduran yardımcı fonksiyon
    def _genis_filo_olustur(self):

# marka, model, kategori ve saatlik fiyat bilgileri
        veriler = [
            ("Porsche", "911 Turbo S", "Spor", 1500), ("Ferrari", "SF90", "Spor", 2500),
            ("Lamborghini", "Revuelto", "Spor", 3000), ("BMW", "M8 Competition", "Spor", 1200),
            ("Audi", "R8 V10", "Spor", 1400), ("McLaren", "720S", "Spor", 2200),
            
            ("Tesla", "Model S Plaid", "Elektrikli", 900), ("Porsche", "Taycan Turbo S", "Elektrikli", 1100),
            ("Lucid", "Air Sapphire", "Elektrikli", 1300), ("BMW", "i7 M70", "Elektrikli", 1000),
            ("Mercedes", "EQS 580", "Elektrikli", 950), ("Audi", "e-tron GT", "Elektrikli", 1050),
            
            ("Mercedes", "G63 AMG", "SUV", 1200), ("Range Rover", "P530", "SUV", 1100),
            ("Lamborghini", "Urus Performante", "SUV", 1800), ("BMW", "XM", "SUV", 1400),
            ("Rolls-Royce", "Cullinan", "SUV", 5000), ("Bentley", "Bentayga", "SUV", 3500),
            
            ("Ducati", "Panigale V4R", "Motor", 600), ("BMW", "S1000RR", "Motor", 500),
            ("Kawasaki", "Ninja H2R", "Motor", 800), ("Yamaha", "R1M", "Motor", 550),
            ("Honda", "CBR1000RR-R", "Motor", 500), ("Aprilia", "RSV4 Factory", "Motor", 520)
        ]

# list comprehension ile verilerdeki her bir aracı Vehicle nesnesine çeviriyoruz
        return [Vehicle(i, v[0], v[1], v[2], v[3]) for i, v in enumerate(veriler, 1)]

# sistem ilk açıldığında mağazayı dolduran yardımcı fonksiyon
    def _urunleri_olustur(self):
        return [
            Product(1, "VRX Karbon Kask", 4500, 10),
            Product(2, "Alpinestars Yarış Tulumu", 8000, 5),
            Product(3, "Fanatec Direksiyon Seti", 15000, 3),
            Product(4, "VRX Premium Anahtarlık", 250, 100),
            Product(5, "Yarış Eldiveni", 1200, 15),
            Product(6, "Motosiklet Montu", 6500, 8)
        ]

# kullanıcı girişi fonksiyonu
    def login(self, uid, pwd):

# kullanıcı ID'si sistemde varsa ve şifresi doğruysa
        if uid in self.users and self.users[uid].sifre == pwd:
            self.current_user = self.users[uid] # oturumu açan kişiyi sisteme tanıtıyor
            return True
        return False # yanlış şifreyse veya kullanıcı yoksa
        
# yeni kayıt olma fonksiyonu
    def register(self, uid, name, pwd, adr):
        if uid in self.users:
            return False #bu kullanıcı adı vs daha önce alınmış
        
# yeni bir user oluşturup sözlüğe ekliyoruz
        self.users[uid] = User(uid, name, pwd, adr)
        return True

# kiralama işleminin yapıldığı ana fonksiyon
    def kiralama_baslat(self, arac, saat):
        tutar = arac.saatlik_fiyat * saat # toplam ödenecek miktar hesaplandı
        
# kullanıcının hesabından parayı çekiyor
        if self.current_user.bakiye_dus(tutar):
            arac.arac_durumu_guncelle(False) #araç kiralandı
            self.rental_counter += 1 # bir sonraki kiralama için fiş no'sunu 1 artır
            
# kiralama kaydını oluştur
            yeni_kiralama = Rental(self.rental_counter, arac, self.current_user, saat, tutar)
            self.current_user.aktif_kiralamalar.append(yeni_kiralama) # kullanıcının listesine ekle
            
            self.sistem_kasasi += tutar #sistem kasasına ekle
            return True, "Başarılı"
            
# parası yetmediyse işlemi iptal et
        return False, "Yetersiz Bakiye"

    # kullanıcı aracı geri getirdiğinde çalışacak fonksiyon
    def kiralama_bitir(self, kiralama_nesnesi):
        # güvenlik kontrolü 
        if kiralama_nesnesi in self.current_user.aktif_kiralamalar:
            kullanilan_km = kiralama_nesnesi.kiralama_bitir() # işlemi sonlandır ve kmyi al
            
            # aktif kiralamalardan çıkarıp geçmiş kayıtlarına taşıyoruz
            self.current_user.aktif_kiralamalar.remove(kiralama_nesnesi)
            self.current_user.kiralama_gecmisi.append(kiralama_nesnesi)
            
            return True, kullanilan_km
        return False, 0
        
    # yalnızca adminlerin yeni araç ekleyebileceği fonksiyon
    def admin_arac_ekle(self, marka, model, kategori, fiyat):
        yeni_id = len(self.vehicles) + 1 # Son ID'yi bulup 1 ekliyoruz
        yeni_arac = Vehicle(yeni_id, marka, model, kategori, fiyat)
        self.vehicles.append(yeni_arac) # Yeni aracı garaja park ettik
        return True
