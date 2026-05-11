PROJE DOKÜMANTASYONU VE KULLANIM KILAVUZU
1. Projenin Amacı ve Özeti
Bu proje, araç kiralama ve ekipman satışını bir araya getiren bir masaüstü otomasyonudur. Projedeki temel amacım, derste öğrendiğimiz Nesne Yönelimli Programlama (OOP) mantığını gerçek bir senaryoda uygulamak ve kullanıcıların rahatça kullanabileceği modern bir arayüz geliştirmekti. Sistemde müşteri ve sistem yöneticisi (admin) olmak üzere iki farklı yetki türü bulunmaktadır.

2. Kullanılan Teknolojiler
Dil: Python

Arayüz Tasarımı: Klasik Tkinter yerine daha modern ve "Dark Mode" destekli bir görünüm sunan customtkinter kütüphanesini kullandım.

Veri Yönetimi: Projenin bu aşamasında harici bir veritabanı bağlamak yerine, verileri (araçlar, kullanıcılar, siparişler) sınıflar (class) içerisinde listeler ve sözlükler yardımıyla hafızada (in-memory) tuttum.

3. Sınıf (Class) Yapısı ve OOP Kullanımı
Projenin arka plan kodları (engine.py) sistemin beyni olarak çalışır ve 5 temel sınıftan oluşur:

Vehicle (Araç): Araçların markası, modeli, fiyatı ve o an müsait olup olmadığı gibi bilgileri tutar.

Product (Ürün): Mağazadaki ürünlerin adını, fiyatını ve stok bilgisini takip eder.

User (Kullanıcı): Müşterilerin bilgilerini, cüzdan bakiyelerini, aktif/geçmiş kiralama listelerini ve siparişlerini barındırır.

Rental (Kiralama İşlemi): Kiralama yapıldığında oluşan fiş gibi düşünülebilir. Hangi aracı kimin aldığını, saati ve toplam ücreti hesaplar.

AppEngine (Ana Motor): Tüm sistemi yöneten ana sınıftır. Giriş-çıkış kontrolleri, ciro hesaplamaları ve listelerin (araç listesi, üye listesi vb.) yönetimi bu sınıf üzerinden yapılır. Sınıflar arası iletişim burada sağlanır.

4. Sistem Kullanım Kılavuzu
Kurulum: Projeyi çalıştırmak için terminale pip install customtkinter yazılarak arayüz kütüphanesinin kurulması ve ana dosyanın çalıştırılması yeterlidir.

Sisteme Giriş:

Uygulama açıldığında testleri kolayca yapabilmek için yeni kayıt olan her kullanıcıya otomatik olarak 5000 TL bakiye tanımlanacak şekilde ayarladım.

Yönetici (Admin) girişi yapmak için Kullanıcı ID kısmına admin, şifre kısmına 123 yazılması yeterlidir.

4.1. Müşteri (User) Paneli
Normal bir kullanıcı sisteme girdiğinde soldaki menüden şu işlemleri yapabilir:

Araç Filosu: Garajdaki araçlar listelenir. Üst kısımdan kategoriye (Spor, SUV vb.) göre filtreleme yapılabilir veya kelimeyle arama yapılabilir. Araç müsaitse kiralama ekranı açılır. (Ekstra özellik: Kiralama ekranındaki kupon kısmına "VRXPRO" yazılırsa sistem otomatik %20 indirim yapar.)

Kiralamalarım: Kullanıcı kiraladığı aracı burada görür. İşlemi bitirip "İade Et" dediğinde sistem rastgele bir km hesaplayıp aracı tekrar boşa çıkarır (müsait yapar).

VRX Store: Ürün satın alma kısmıdır. Ürünün stoğu bittiyse buton otomatik devre dışı kalır.

Profil ve Cüzdan: Kullanıcı kalan bakiyesini ve aldığı ürünlerin kargo durumunu görebilir. "Bakiye Yükle" diyerek sanal pos ekranı simülasyonu üzerinden hesaba para ekleyebilir. Yetersiz bakiye durumlarında sistem hata mesajı verir.

4.2. Yönetici (Admin) Paneli
Sisteme admin olarak girildiğinde tamamen farklı bir arayüz açılır:

Genel Özet: Sistemin o anki toplam cirosu, üye sayısı ve kiradaki araç sayısı gibi istatistikler görülür.

Üye Yönetimi: Kayıtlı üyeler incelenebilir ve istenilen üyenin hesabı sistemden silinebilir.

Araç Yönetimi: Admin, arızalanan veya bakıma girmesi gereken bir aracı "Bakıma Al" butonuna basarak kiralama ekranından geçici olarak gizleyebilir.

Yeni Araç Ekle: Forma marka, model ve fiyat girilerek sisteme anında yeni bir araç eklenebilir.

Mağaza Stokları: Mağazadaki ürünlerin stoğu azaldığında admin tek tıkla ürünlere "+5 Stok" eklemesi yapabilir.

5. Sonuç
Bu projeyle, birbirinden bağımsız çalışan sınıfların (OOP) birbiriyle uyum içinde nasıl haberleştiğini ve arka plandaki bu mantığın görsel bir arayüze nasıl bağlanacağını uygulamalı olarak öğrenmiş oldum. Uygulamanın çökmemesi için yetersiz bakiye, yanlış şifre ve boş veri girme gibi durumlara karşı hata kontrollerini de ekleyerek projeyi tamamladım.
