import random

# sistemdeki her bir aracı temsil eden sınıf
class Vehicle:
    def __init__(self, arac_id, marka, model, kategori, saatlik_fiyat):
        self.arac_id = arac_id
        self.marka = marka
        self.model = model
        self.kategori = kategori
        self.saatlik_fiyat = saatlik_fiyat
        # araç ilk oluşturulduğunda varsayılan olarak müsait gelior
        self.musait_mi = True
        
        # gerçekçilik katmak için KM, vites ve HP gibi değerleri rastgele veya şartlı olarak atandı
        self.km = random.randint(100, 25000)
        # eğer kategori Motor ise sıralı vites, değilse otomatik vites 
        self.vites = "Otomatik" if kategori != "Motor" else "Sıralı"
        # elektrikli kategorisi dışındaki her şey benzin/hibrit 
        self.yakit = "Elektrikli" if kategori == "Elektrikli" else "Benzin/Hibrit"
        self.hp = random.randint(150, 800)

# mağazadaki ekipmanları (kask, tulum vb.) tanımlayan sınıf
class Product:
    def __init__(self, p_id, name, price, stock):
        self.p_id = p_id
        self.name = name
        self.price = price
        self.stock = stock

# kullanıcı bilgilerini ve cüzdan/sipariş geçmişini tutan sınıf
class User:
    def __init__(self, kullanici_id, ad, sifre, adres):
        self.kullanici_id = kullanici_id
        self.ad = ad
        self.sifre = sifre
        self.adres = adres
        # her kullanıcıya başlangıçta 5000 TL sanal bakiye yüklenior
        self.bakiye = 5000.0
        
        # kullanıcının yaptığı kiralama ve alışverişleri takip etmek için listeler
        self.kiralanan_araclar = []  
        self.siparisler = []         

#veri saklama ve giriş işlemlerini yönetiyor
class AppEngine:
    def __init__(self):
        # kullanıcıları hızlı bulabilmek için dictionary yapısı kullannıldı
        self.users = {
            "admin": User("admin", "Sistem Yöneticisi", "123", "VRX Merkez"),
            "user": User("user", "Örnek Kullanıcı", "123", "Kadıköy, İstanbul")
        }
        # araç ve ürün listesi
        self.vehicles = self._genis_filo_olustur()
        self.products = [
            Product(1, "VRX Karbon Kask", 4500, 10),
            Product(2, "Yarış Tulumu", 8000, 5),
            Product(3, "Direksiyon Seti", 15000, 3),
            Product(4, "VRX Anahtarlık", 250, 100)
        ]
        # a an sisteme giriş yapmış olan kullanıcıyı burada tutuyoruz
        self.current_user = None

    # kodun kalabalık durmaması için filo verilerini bu metodda koyuyoruz
    def _genis_filo_olustur(self):
        veriler = [
            # marka, model, kategori, saatlikücret şeklinde tuple listesi
            ("Porsche", "911 Turbo S", "Spor", 1500), ("Ferrari", "SF90", "Spor", 2500),
            ("Lamborghini", "Revuelto", "Spor", 3000), ("BMW", "M8 Competition", "Spor", 1200),
            ("Audi", "R8 V10", "Spor", 1400),
            
            ("Tesla", "Model S Plaid", "Elektrikli", 900), ("Porsche", "Taycan Turbo S", "Elektrikli", 1100),
            ("Lucid", "Air Sapphire", "Elektrikli", 1300), ("BMW", "i7 M70", "Elektrikli", 1000),
            ("Mercedes", "EQS 580", "Elektrikli", 950),
            
            ("Mercedes", "G63 AMG", "SUV", 1200), ("Range Rover", "P530", "SUV", 1100),
            ("Lamborghini", "Urus Performante", "SUV", 1800), ("BMW", "XM", "SUV", 1400),
            ("Rolls-Royce", "Cullinan", "SUV", 5000),
            
            ("Ducati", "Panigale V4R", "Motor", 600), ("BMW", "S1000RR", "Motor", 500),
            ("Kawasaki", "Ninja H2R", "Motor", 800), ("Yamaha", "R1M", "Motor", 550),
            ("Honda", "CBR1000RR-R", "Motor", 500)
        ]
        #döngüyle vehicle nesnelerine çevirip liste olarak döndürülüyot
        return [Vehicle(i, v[0], v[1], v[2], v[3]) for i, v in enumerate(veriler, 1)]

    # kullanıcı adı ve şifre kontrolü yapan metod
    def login(self, uid, pwd):
        # kullanıcı sözlükte var mı ve şifresi doğru mu die bakıyor
        if uid in self.users and self.users[uid].sifre == pwd:
            self.current_user = self.users[uid] # giriş başarılıysa aktif kullanıcıyı atıyoruz
            return True
        return False