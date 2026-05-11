PROJE DOKÜMANTASYONU VE KULLANIM KILAVUZU
Arayüz Tasarımı: customtkinter kütüphanesini kullandım
Veri Yönetimi: projenin bu aşamasında harici bir veritabanı bağlamak yerine, verileri sınıflar (class) içerisinde listeler ve sözlükler yardımıyla hafızada tuttum
5 temel sınıf:
Vehicle : araçların markası modeli fiyatı ve o an müsait olup olmadığı gibi bilgileri tutar
Product : mağazadaki ürünlerin adını fiyatını ve stok bilgisini takip eder
User: müşterilerin bilgilerini cüzdan bakiyelerini aktif ve geçmiş kiralama listelerini ve siparişlerini barındırır
Rental: hangi aracı kimin aldığını saati ve toplam ücretini hesaplar
AppEngine: Tüm sistemi yöneten ana sınıf

 Sistem Kullanım Kılavuzu
Kurulum: Projeyi çalıştırmak için terminale pip install customtkinter yazılarak arayüz kütüphanesinin kurulması ve ana dosyanın çalıştırılması yeterlidir.

 Müşteri (User) Paneli
Normal bir kullanıcı sisteme girdiğinde soldaki menüden şu işlemleri yapabilir:

Araç Filosu: Garajdaki araçlar listelenir. Üst kısımdan kategoriye (Spor, SUV vb.) göre filtreleme yapılabilir veya kelimeyle arama yapılabilir. Araç müsaitse kiralama ekranı açılır. (Ekstra özellik: Kiralama ekranındaki kupon kısmına "VRX" yazılırsa sistem otomatik %20 indirim yapar.)

Kiralamalarım: Kullanıcı kiraladığı aracı burada görür. İşlemi bitirip "İade Et" dediğinde sistem rastgele bir km hesaplayıp aracı tekrar boşa çıkarır (müsait yapar).

VRX Store: Ürün satın alma kısmıdır. Ürünün stoğu bittiyse buton otomatik devre dışı kalır.

Profil ve Cüzdan: Kullanıcı kalan bakiyesini ve aldığı ürünlerin kargo durumunu görebilir. "Bakiye Yükle" diyerek sanal pos ekranı simülasyonu üzerinden hesaba para ekleyebilir. Yetersiz bakiye durumlarında sistem hata mesajı verir.

 Yönetici (Admin) Paneli
Sisteme admin olarak girildiğinde tamamen farklı bir arayüz açılır: Yönetici (Admin) girişi yapmak için Kullanıcı ID kısmına admin, şifre kısmına 123 yazılması yeterlidir.

Genel Özet: Sistemin o anki toplam cirosu, üye sayısı ve kiradaki araç sayısı gibi istatistikler görülür.

Üye Yönetimi: Kayıtlı üyeler incelenebilir ve istenilen üyenin hesabı sistemden silinebilir.

Araç Yönetimi: Admin, arızalanan veya bakıma girmesi gereken bir aracı "Bakıma Al" butonuna basarak kiralama ekranından geçici olarak gizleyebilir.

Yeni Araç Ekle: Forma marka, model ve fiyat girilerek sisteme anında yeni bir araç eklenebilir.

Mağaza Stokları: Mağazadaki ürünlerin stoğu azaldığında admin tek tıkla ürünlere "+5 Stok" eklemesi yapabilir.
