import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from PIL import Image
from engine import AppEngine

# uygulamanın genel teması
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ana uygulama penceresini temsil eden sınıf
class VRXApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # pencere başlığı ve boyutları
        self.title("VRX Premium - Pro Console")
        self.geometry("1280x850")
        self.configure(fg_color="#050505") # Arka planı simsiyah yaptık
        
        # uygulamanın verileri fonksiyonları burada başlatıyoruz
        self.engine = AppEngine()
        
        # grid sistemini pencere büyüyüp küçüldüğünde ekranı kaplayacak şekilde esnek olması için
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # tüm sayfaları içine koycaz
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # uygulama açılır açılmaz giriş ekranını göster
        self.show_login_screen()

    # sayfa değiştirirken ekranı temizlemek için
    def clear(self):
        for w in self.main_container.winfo_children(): 
            w.destroy() # ekrandaki her şeyi yok et



    # uyarı pencereleri
    def show_vrx_msg(self, title, msg, color="#800000"):
        pop = ctk.CTkToplevel(self) # Yeni bir küçük pencere aç
        pop.geometry("450x250")
        pop.title(title)
        pop.configure(fg_color="#0F0F0F")
        pop.attributes("-topmost", True) # her zaman diğer pencerelerin en üstünde dursun
        
        # başlık ve mesaj metinleri
        ctk.CTkLabel(pop, text=title, font=("Arial", 20, "bold"), text_color=color).pack(pady=(25,10))
        ctk.CTkLabel(pop, text=msg, font=("Arial", 14), wraplength=380).pack(pady=15)
        # Kapatma butonu
        ctk.CTkButton(pop, text="TAMAM", fg_color=color, font=("Arial", 14, "bold"), height=40, command=pop.destroy).pack(pady=15)

    # ödeme yaparken veya bakiye yüklerken çıkan snal pos ekranı
    def ask_payment(self, amount, callback, is_balance_load=False):
        pay_pop = ctk.CTkToplevel(self)
        pay_pop.geometry("420x550")
        pay_pop.title("Güvenli Ödeme Geçidi")
        pay_pop.attributes("-topmost", True)
        pay_pop.configure(fg_color="#121212")
        
        # başlık duruma göre değişiyo
        title_text = "BAKİYE YÜKLEME" if is_balance_load else "KREDİ KARTI ÖDEME"
        ctk.CTkLabel(pay_pop, text=title_text, font=("Arial", 24, "bold"), text_color="#800000").pack(pady=25)
        
        # kart bilgileri için giriş yerleri
        ctk.CTkEntry(pay_pop, placeholder_text="Kart Sahibi Ad Soyad", width=340, height=45).pack(pady=10)
        ctk.CTkEntry(pay_pop, placeholder_text="0000 0000 0000 0000", width=340, height=45).pack(pady=10)
        
        # tarih ve CVV yan yana dursun diye yeni bir çerçeve
        f_row = ctk.CTkFrame(pay_pop, fg_color="transparent")
        f_row.pack(pady=10)
        ctk.CTkEntry(f_row, placeholder_text="AA/YY", width=165, height=45).pack(side="left", padx=(0,5))
        ctk.CTkEntry(f_row, placeholder_text="CVV", width=165, height=45).pack(side="left", padx=(5,0))
        
        action_text = f"İşlem Tutarı: {amount} TL"
        ctk.CTkLabel(pay_pop, text=action_text, font=("Arial", 20, "bold")).pack(pady=30)
        
        # ödemeyi onaylayınca çalışıcak fonksiyon
        def process():
            pay_pop.destroy() # ödeme ekranını kapat
            callback() # başarılıysa yapılması gereken asıl işi yap 
            if is_balance_load:
                self.show_vrx_msg("BAŞARILI", f"{amount} TL bakiyenize başarıyla yüklendi!", "green")

        ctk.CTkButton(pay_pop, text="İŞLEMİ ONAYLA", fg_color="#800000", font=("Arial", 16, "bold"), height=50, width=340, command=process).pack(pady=10)

 #giriş ve kayıt ekranları
    def show_login_screen(self):
        self.clear() # ekranı temizle
        self.current_screen = "login"

#sabit arka plan
        try:
            bg_pil = Image.open("vrx_bg.png")
            
            # görseli sürekli yeniden boyutlandırmak yerine, yüksek çözünürlükte sabitliyoruz
            self.bg_image = ctk.CTkImage(light_image=bg_pil, size=(1920, 1080))
            
            # görseli label içine koyup ekranın ortasına yerleştirdik
            self.bg_label = ctk.CTkLabel(self.main_container, image=self.bg_image, text="")
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")
            
        except Exception as e:
            print("Arka plan yüklenemedi:", e)
            self.bg_image = None
            self.bg_label = None

        # giriş katmanı
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center") 
        
        ctk.CTkLabel(frame, text="VRX", font=("Arial", 90, "bold"), text_color="#CC0000").pack(pady=(0, 0)) 
        ctk.CTkLabel(frame, text="PREMIUM RENT A CAR", font=("Arial", 20, "bold"), text_color="#FFFFFF").pack(pady=(0, 30))
        
        self.u_ent = ctk.CTkEntry(frame, placeholder_text="Kullanıcı ID", width=350, height=50, font=("Arial", 14), 
                                  fg_color="#0A0A0A", border_color="#333")
        self.u_ent.pack(pady=10)
        
        self.p_ent = ctk.CTkEntry(frame, placeholder_text="Şifre", show="*", width=350, height=50, font=("Arial", 14),
                                  fg_color="#0A0A0A", border_color="#333")
        self.p_ent.pack(pady=10)
        
        ctk.CTkButton(frame, text="SİSTEME GİRİŞ YAP", fg_color="#800000", font=("Arial", 16, "bold"), width=350, height=55, command=self.handle_login).pack(pady=25)
        ctk.CTkButton(frame, text="Yeni Hesap Oluştur", fg_color="transparent", text_color="#FFFFFF", font=("Arial", 14), command=self.show_register_screen).pack()
        
        # admin butonu
        ctk.CTkButton(frame, text="Admin Paneli", fg_color="transparent", text_color="#555", font=("Arial", 12),
                      command=lambda: [self.u_ent.delete(0, 'end'), self.u_ent.insert(0,"admin"), 
                                       self.p_ent.delete(0, 'end'), self.p_ent.insert(0,"123")]).pack(pady=20)
    # giriş yapma kontrolü
    def handle_login(self):
        uid, pwd = self.u_ent.get(), self.p_ent.get()
        if uid == "admin" and pwd == "123": # adminse admin paneline yönlendir
            self.engine.current_user = self.engine.users["admin"]
            self.show_admin_dashboard()
        elif self.engine.login(uid, pwd): # kullanıcıysa yönlendir
            self.show_user_dashboard()
        else: # yanlış şifreyse uyar
            self.show_vrx_msg("HATA", "Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.", "red")

    # yeni üyelik ekranı
    def show_register_screen(self):
        self.clear()
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(frame, text="YENİ ÜYELİK", font=("Arial", 40, "bold"), text_color="#800000").pack(pady=40)
        
        uid = ctk.CTkEntry(frame, placeholder_text="Kullanıcı ID (Örn: ali_yilmaz)", width=350, height=45); uid.pack(pady=8)
        name = ctk.CTkEntry(frame, placeholder_text="Ad Soyad", width=350, height=45); name.pack(pady=8)
        pwd = ctk.CTkEntry(frame, placeholder_text="Şifre Oluştur", show="*", width=350, height=45); pwd.pack(pady=8)
        adr = ctk.CTkEntry(frame, placeholder_text="Açık Adres", width=350, height=45); adr.pack(pady=8)

        def do_reg():
            # tüm kutular doldurulmuş mu kontrolü
            if not all([uid.get(), name.get(), pwd.get(), adr.get()]):
                self.show_vrx_msg("UYARI", "Lütfen tüm alanları doldurun.", "red")
                return
            
            # kayıt başarılıysa giriş ekranına at değilse uyar
            if self.engine.register(uid.get(), name.get(), pwd.get(), adr.get()):
                self.show_vrx_msg("BAŞARILI", "Kaydınız başarıyla oluşturuldu. Giriş yapabilirsiniz.", "green")
                self.show_login_screen()
            else:
                self.show_vrx_msg("HATA", "Bu Kullanıcı ID zaten sistemde mevcut.", "red")

        ctk.CTkButton(frame, text="KAYIT OL", fg_color="#800000", font=("Arial", 16, "bold"), height=50, width=350, command=do_reg).pack(pady=25)
        ctk.CTkButton(frame, text="İptal Et ve Geri Dön", fg_color="transparent", text_color="#888", command=self.show_login_screen).pack()

    #müşteri paneli
    
    def show_user_dashboard(self):
        self.clear()
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # sol taraftaki menü barı
        side = ctk.CTkFrame(self.main_container, width=250, fg_color="#0A0A0A", corner_radius=0)
        side.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(side, text="VRX PREMIUM", font=("Arial", 24, "bold"), text_color="#800000").pack(pady=(40, 30))
        
        # sağ taraftaki içeriklerin gösterileceği alan
        self.cont = ctk.CTkFrame(self.main_container, fg_color="#050505")
        self.cont.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # menü seçeneklerini liste içinde tutuyoruz
        menus = [
            ("🚘 Araç Filosu", self.show_fleet), 
            ("🔑 Kiralamalarım", self.show_my_rentals),
            ("🛒 VRX Store", self.show_store), 
            ("👤 Profil & Cüzdan", self.show_profile), 
            ("🚪 Çıkış Yap", self.show_login_screen)
        ]
        
        # menüdeki butonlar
        for text, command in menus: 
            btn = ctk.CTkButton(side, text=text, fg_color="transparent", anchor="w", font=("Arial", 16), height=50, command=command)
            btn.pack(fill="x", padx=15, pady=5)
            
        self.show_fleet() # panel açıldığında ilk olarak araç filosu sayfası gelsin

    # araçların listelendiği ana sayfa
    def show_fleet(self, kategori_filtresi="Hepsi", arama_metni=""):
        for w in self.cont.winfo_children(): w.destroy()
        
        # üst taraftaki arama ve kategori filtreleme alanı
        top_bar = ctk.CTkFrame(self.cont, fg_color="transparent", height=60)
        top_bar.pack(fill="x", pady=(0, 15))
        
        search_ent = ctk.CTkEntry(top_bar, placeholder_text="Marka veya Model Ara...", width=300, height=40)
        search_ent.pack(side="left", padx=(0, 10))
        search_ent.insert(0, arama_metni) # aramayı korumak için son arananı içine yazıyoruz
        
        ctk.CTkButton(top_bar, text="Ara", width=80, height=40, fg_color="#333", 
                      command=lambda: self.show_fleet(kategori_filtresi, search_ent.get())).pack(side="left")

        # kategori ayrımları
        cat_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        cat_frame.pack(side="right")
        
        for k in ["Hepsi", "Spor", "Elektrikli", "SUV", "Motor"]:
            btn_color = "#800000" if kategori_filtresi == k else "#1A1A1A"
            ctk.CTkButton(cat_frame, text=k, width=90, height=40, fg_color=btn_color, font=("Arial", 13, "bold"),
                          command=lambda x=k: self.show_fleet(x, search_ent.get())).pack(side="left", padx=3)

        # fare tekerleğiyle kaydırılabilir araç listesi alanı
        scroll = ctk.CTkScrollableFrame(self.cont, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for v in self.engine.vehicles:
            # filtreleme 
            if kategori_filtresi != "Hepsi" and v.kategori != kategori_filtresi: continue
            if arama_metni.lower() not in (v.marka + " " + v.model).lower(): continue
            
            # her bir araç için yatay kart
            card = ctk.CTkFrame(scroll, fg_color="#121212", corner_radius=10)
            card.pack(fill="x", pady=8, padx=5, ipady=10)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", padx=20, fill="both", expand=True)
            
            # aracın temel bilgileri
            ctk.CTkLabel(info_frame, text=f"{v.marka} {v.model}", font=("Arial", 20, "bold"), text_color="#FFF").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"{v.hp} HP • {v.vites} • ⭐ {v.degerlendirme}", font=("Arial", 14), text_color="#AAA").pack(anchor="w", pady=(5,0))
            
            price_frame = ctk.CTkFrame(card, fg_color="transparent")
            price_frame.pack(side="right", padx=20)
            
            ctk.CTkLabel(price_frame, text=f"{v.saatlik_fiyat} TL / Saat", font=("Arial", 18, "bold"), text_color="#800000").pack(side="left", padx=20)
            
            # araç kiradaysa butonu pasif yapıyoruz
            btn_text = "HEMEN KİRALA" if v.musait_mi else "ŞU AN KİRADA"
            btn_color = "#800000" if v.musait_mi else "#333"
            btn_state = "normal" if v.musait_mi else "disabled"
            
            # butona basılınca aracın detay kiralama sayfasını aç.ar
            ctk.CTkButton(price_frame, text=btn_text, width=140, height=45, font=("Arial", 14, "bold"), 
                          fg_color=btn_color, state=btn_state, command=lambda x=v: self.show_vehicle_details(x)).pack(side="right")

    # kiralama detay ve onay penceresi
    def show_vehicle_details(self, v):
        pop = ctk.CTkToplevel(self)
        pop.geometry("500x650")
        pop.title("Araç Kiralama")
        pop.configure(fg_color="#0D0D0D")
        pop.attributes("-topmost", True)
        
        ctk.CTkLabel(pop, text=f"{v.marka} {v.model}", font=("Arial", 28, "bold"), text_color="#800000").pack(pady=(30,10))
        
        # araç teknik özellikleri
        details = f"""
Kategori: {v.kategori}
Motor Gücü: {v.hp} HP
Vites Tipi: {v.vites}
Yakıt Tipi: {v.yakit}
Mevcut Kilometre: {v.km:,} KM
Müşteri Puanı: {v.degerlendirme} / 5.0
        """
        ctk.CTkLabel(pop, text=details, font=("Arial", 16), justify="left", bg_color="#151515", corner_radius=8, width=400).pack(pady=15, ipady=10)
        
        ctk.CTkLabel(pop, text="Kiralama Süresi Seçin:", font=("Arial", 14, "bold")).pack(pady=(10,5))
        
        # kiralama süresini seçtirdiğimiz açılır menü 
        saat_var = ctk.StringVar(value="1 Saat")
        saat_menu = ctk.CTkOptionMenu(pop, values=["1 Saat", "3 Saat", "6 Saat", "12 Saat", "24 Saat (1 Gün)", "48 Saat (2 Gün)"], variable=saat_var, width=250, height=40)
        saat_menu.pack(pady=5)
        
        # kupon kodu alanı
        coupon_ent = ctk.CTkEntry(pop, placeholder_text="İndirim Kodu (İsteğe Bağlı)", width=250, height=40)
        coupon_ent.pack(pady=10)

        def rent_vehicle():
            # menüden seçilen değeri al boşluktan böl ve ilk elemanı alıp int'e çevir
            saat_str = saat_var.get().split()[0]
            saat = int(saat_str)
            
            toplam_tutar = v.saatlik_fiyat * saat
            indirim = 0
            
            # kupon
            if coupon_ent.get().upper() == "VRX":
                indirim = toplam_tutar * 0.20
                toplam_tutar -= indirim
                messagebox.showinfo("Kupon", "%20 İndirim Uygulandı!", parent=pop)

            # onaylama sorusu
            onay = messagebox.askyesno("Onay", f"Toplam Tutar: {toplam_tutar} TL\nOnaylıyor musunuz?", parent=pop)
            if onay:
                #engine e isteği gönder işlemi yaparsa basarili=True döner
                basarili, mesaj = self.engine.kiralama_baslat(v, saat)
                if basarili:
                    pop.destroy()
                    self.show_vrx_msg("İŞLEM BAŞARILI", f"{v.marka} {v.model} aracını {saat} saatliğine kiraladınız. Lütfen süresi bitmeden iade ediniz.", "green")
                    self.show_fleet() # sayfayı yeniler
                else:
                    self.show_vrx_msg("HATA", "Yetersiz bakiye. Lütfen cüzdanınıza para yükleyin.", "red")

        ctk.CTkLabel(pop, text=f"Saatlik Ücret: {v.saatlik_fiyat} TL", font=("Arial", 16)).pack(pady=10)
        ctk.CTkButton(pop, text="ÖDEME YAP VE KİRALA", fg_color="#800000", font=("Arial", 16, "bold"), height=50, width=300, command=rent_vehicle).pack(pady=20)

    # kullanıcının aktif ve geçmiş kiralamalarını gördüğü sayfa
    def show_my_rentals(self):
        for w in self.cont.winfo_children(): w.destroy()
        
        ctk.CTkLabel(self.cont, text="KİRALAMA YÖNETİMİ", font=("Arial", 26, "bold")).pack(pady=15, anchor="w")
        
        # sekmeli görünüm
        tab_view = ctk.CTkTabview(self.cont, fg_color="transparent")
        tab_view.pack(fill="both", expand=True)
        
        tab_aktif = tab_view.add("Aktif Kiralamalar")
        tab_gecmis = tab_view.add("Geçmiş İşlemler")
        
        u = self.engine.current_user
        
        # aktif kiralamalar
        if not u.aktif_kiralamalar:
            ctk.CTkLabel(tab_aktif, text="Şu anda aktif bir kiralamanız bulunmuyor.", font=("Arial", 16), text_color="#777").pack(pady=40)
        else:
            for r in u.aktif_kiralamalar:
                card = ctk.CTkFrame(tab_aktif, fg_color="#151515", height=100)
                card.pack(fill="x", pady=5, padx=10, ipady=10)
                
                info = f"🚘 {r.arac.marka} {r.arac.model} | Süre: {r.saat_suresi} Saat | Ödenen: {r.toplam_tutar} TL\nBaşlangıç: {r.baslangic_saati.strftime('%Y-%m-%d %H:%M')}"
                ctk.CTkLabel(card, text=info, font=("Arial", 15), justify="left").pack(side="left", padx=20)
                
                # aracı geri verme işlemi
                def iade_et(kiralama=r):
                    onay = messagebox.askyesno("İade İşlemi", "Aracı iade etmek istediğinize emin misiniz?")
                    if onay:
                        basarili, km = self.engine.kiralama_bitir(kiralama)
                        if basarili:
                            self.show_vrx_msg("İADE BAŞARILI", f"Araç başarıyla iade edildi. Bu sürüşte {km} km yol yaptınız.", "green")
                            self.show_my_rentals() # sayfayı yeniler

                ctk.CTkButton(card, text="ARACI İADE ET", fg_color="#006600", font=("Arial", 14, "bold"), height=40, command=iade_et).pack(side="right", padx=20)

        # geçmiş kiralamalar
        if not u.kiralama_gecmisi:
            ctk.CTkLabel(tab_gecmis, text="Henüz tamamlanmış bir kiralamanız yok.", font=("Arial", 16), text_color="#777").pack(pady=40)
        else:
            # reversed ile listeyi ters çevirdik en son iade edilen en üstte görünsün die
            for r in reversed(u.kiralama_gecmisi): 
                card = ctk.CTkFrame(tab_gecmis, fg_color="#0A0A0A", height=80)
                card.pack(fill="x", pady=5, padx=10, ipady=5)
                zaman = r.bitis_saati.strftime('%Y-%m-%d %H:%M') if r.bitis_saati else "Bilinmiyor"
                ctk.CTkLabel(card, text=f"✅ {r.arac.marka} {r.arac.model} - İade Edildi ({zaman})", font=("Arial", 14), text_color="#888").pack(anchor="w", padx=20, pady=10)

    # ekipman satış mağazası
    def show_store(self):
        for w in self.cont.winfo_children(): w.destroy()
        ctk.CTkLabel(self.cont, text="VRX STORE - LİSANSLI EKİPMANLAR", font=("Arial", 26, "bold")).pack(pady=(15,25), anchor="w")
        
        scroll = ctk.CTkScrollableFrame(self.cont, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        for p in self.engine.products:
            card = ctk.CTkFrame(scroll, fg_color="#121212", corner_radius=8)
            card.pack(fill="x", pady=6, padx=10, ipady=15)
            
            # ürün görselleri
            img_frame = ctk.CTkFrame(card, fg_color="transparent")
            img_frame.pack(side="left", padx=(20, 0))
            
            try:
                # ürün ID sine göre klasörden görseli çekiyor
                foto_yolu = f"urun_{p.p_id}.png"
                prod_img = ctk.CTkImage(light_image=Image.open(foto_yolu), size=(60, 60))
            except FileNotFoundError:
                    prod_img = None # O da yoksa boş bırakır

            if prod_img:
                ctk.CTkLabel(img_frame, image=prod_img, text="").pack()
            
            # ürün bilgileri
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(info_frame, text=f"{p.name}", font=("Arial", 18, "bold")).pack(anchor="w", padx=20)
            ctk.CTkLabel(info_frame, text=f"Kalan Stok: {p.stock} Adet", font=("Arial", 14), text_color="#AAA").pack(anchor="w", padx=20)
            
            # fiyat ve satın alma
            price_frame = ctk.CTkFrame(card, fg_color="transparent")
            price_frame.pack(side="right", padx=20)
            ctk.CTkLabel(price_frame, text=f"{p.price} TL", font=("Arial", 20, "bold"), text_color="#800000").pack(side="left", padx=20)
            
            def buy_process(prod=p):
                adr_pop = ctk.CTkToplevel(self)
                adr_pop.geometry("400x300")
                adr_pop.title("Kargo Onayı")
                adr_pop.attributes("-topmost", True)
                
                ctk.CTkLabel(adr_pop, text="KARGO ADRES ONAYI", font=("Arial", 18, "bold")).pack(pady=20)
                ctk.CTkLabel(adr_pop, text=f"Güncel Teslimat Adresiniz:\n\n{self.engine.current_user.adres}", font=("Arial", 14), wraplength=350).pack(pady=10)
                
                def final():
                    adr_pop.destroy()
                    def complete_order():
                        prod.stock -= 1
                        self.engine.current_user.siparisler.append({"urun": prod.name, "durum": "Hazırlanıyor", "tarih": datetime.now().strftime("%d/%m/%Y")})
                        self.show_vrx_msg("SİPARİŞ ALINDI", f"{prod.name} siparişiniz başarıyla alındı.", "green")
                        self.show_store() 
                    self.ask_payment(prod.price, complete_order)
                
                ctk.CTkButton(adr_pop, text="BU ADRESE GÖNDER", fg_color="#800000", height=45, command=final).pack(pady=15)

            btn_text = "SATIN AL" if p.stock > 0 else "TÜKENDİ"
            btn_state = "normal" if p.stock > 0 else "disabled"
            ctk.CTkButton(price_frame, text=btn_text, fg_color="#800000", font=("Arial", 14, "bold"), height=40, state=btn_state, command=buy_process).pack(side="right")

  
    # kullanıcının kendi bilgilerini ve cüzdanını gördüğü yer
    def show_profile(self):
        for w in self.cont.winfo_children(): w.destroy()
        u = self.engine.current_user
        
        ctk.CTkLabel(self.cont, text="PROFİL VE CÜZDAN", font=("Arial", 26, "bold")).pack(pady=15, anchor="w")
        
        top_frame = ctk.CTkFrame(self.cont, fg_color="#111", corner_radius=10)
        top_frame.pack(fill="x", pady=10, ipady=15)
        
        # profil görseli
        avatar_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        avatar_frame.pack(side="left", padx=(30, 10))
        
        try:
            avatar_img = ctk.CTkImage(light_image=Image.open("avatar.png"), size=(80, 80))
            ctk.CTkLabel(avatar_frame, image=avatar_img, text="").pack()
        except FileNotFoundError:
            pass # eğer avatar görseli yoksa boş geçer

        info_f = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_f.pack(side="left", padx=10)
        
        ctk.CTkLabel(info_f, text=f"{u.ad}", font=("Arial", 22, "bold")).pack(anchor="w", pady=2)
        ctk.CTkLabel(info_f, text=f"🆔 ID: {u.kullanici_id}", font=("Arial", 16), text_color="#888").pack(anchor="w", pady=2)
        ctk.CTkLabel(info_f, text=f"📍 Adres: {u.adres}", font=("Arial", 16), text_color="#888").pack(anchor="w", pady=2)
        
        # cüzdan bilgileri ve bakiye yükleme
        wallet_f = ctk.CTkFrame(top_frame, fg_color="#1A1A1A", corner_radius=10)
        wallet_f.pack(side="right", padx=30, ipadx=20, ipady=10)
        
        ctk.CTkLabel(wallet_f, text="Mevcut Bakiye", font=("Arial", 14)).pack()
        ctk.CTkLabel(wallet_f, text=f"{u.bakiye:,.2f} TL", font=("Arial", 28, "bold"), text_color="#00AA00").pack(pady=5)
        
        new_b = ctk.CTkEntry(wallet_f, placeholder_text="Tutar (TL)", width=150)
        new_b.pack(pady=5)
        
        def load_balance():
            val = new_b.get()
            if not val.isdigit() or int(val) <= 0: # girilen şey düzgün bir sayı mı kontrolü
                self.show_vrx_msg("HATA", "Lütfen geçerli pozitif bir tutar girin.", "red")
                return
            amount = float(val)
            #sSanal pos ekranını çağırır başarılıysa bakiye eklee ve sayfayı yeniler
            self.ask_payment(amount, lambda: [u.bakiye_ekle(amount), self.show_profile()], is_balance_load=True)

        ctk.CTkButton(wallet_f, text="BAKİYE YÜKLE", fg_color="#800000", command=load_balance).pack(pady=5)

        # altta mağaza siparişlerini listeliyoruz
        order_frame = ctk.CTkFrame(self.cont, fg_color="#0A0A0A")
        order_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(order_frame, text="📦 Mağaza Siparişlerim", font=("Arial", 18, "bold")).pack(pady=10, anchor="w", padx=20)
        
        if not u.siparisler:
            ctk.CTkLabel(order_frame, text="Henüz mağazadan ürün sipariş etmediniz.", text_color="#777").pack(pady=20)
        else:
            for siparis in u.siparisler:
                f = ctk.CTkFrame(order_frame, fg_color="#151515")
                f.pack(fill="x", padx=20, pady=5)
                ctk.CTkLabel(f, text=f"{siparis['tarih']} - {siparis['urun']} | Durum: {siparis['durum']}", font=("Arial", 15)).pack(side="left", padx=15, pady=10)

    # admin paneli
    
    def show_admin_dashboard(self):
        # yönetici için özel sol menü
        self.clear()
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # menü rengi
        side = ctk.CTkFrame(self.main_container, width=250, fg_color="#110000", corner_radius=0)
        side.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(side, text="ADMIN PANEL", font=("Arial", 24, "bold"), text_color="#FF4444").pack(pady=(40, 30))
        
        self.a_cont = ctk.CTkFrame(self.main_container, fg_color="#050505")
        self.a_cont.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        menus = [
            ("📊 Genel Özet", self.adm_overview),
            ("👥 Üye Yönetimi", self.adm_users), 
            ("🚘 Araç Yönetimi", self.adm_vehicles),
            ("➕ Yeni Araç Ekle", self.adm_add_vehicle),
            ("🛒 Mağaza Stokları", self.adm_store), 
            ("🚪 Sistemden Çık", self.show_login_screen)
        ]
        
        for text, command in menus: 
            btn_color = "#FF2222" if text == "🚪 Sistemden Çık" else "transparent"
            btn = ctk.CTkButton(side, text=text, fg_color=btn_color, anchor="w", font=("Arial", 16), height=50, command=command)
            btn.pack(fill="x", padx=15, pady=5)
            
        self.adm_overview()

    # özet sayfası
    def adm_overview(self):
        for w in self.a_cont.winfo_children(): w.destroy()
        ctk.CTkLabel(self.a_cont, text="SİSTEM GENEL ÖZETİ", font=("Arial", 26, "bold")).pack(pady=20, anchor="w")
        
        grid_f = ctk.CTkFrame(self.a_cont, fg_color="transparent")
        grid_f.pack(fill="x", pady=20)
        
        # widget oluşturmak için yardımcı fonksiyon
        def create_stat_box(parent, title, value, color):
            box = ctk.CTkFrame(parent, fg_color="#111", corner_radius=10, width=200, height=120)
            box.pack(side="left", padx=10, expand=True, fill="both")
            ctk.CTkLabel(box, text=title, font=("Arial", 16, "bold"), text_color="#888").pack(pady=(20,5))
            ctk.CTkLabel(box, text=value, font=("Arial", 30, "bold"), text_color=color).pack(pady=(0,20))

        toplam_arac = len(self.engine.vehicles)
        musait_arac = sum(1 for v in self.engine.vehicles if v.musait_mi)
        toplam_uye = len(self.engine.users) - 1 # admini saymıoz
        
        create_stat_box(grid_f, "Toplam Ciro", f"{self.engine.sistem_kasasi:,.2f} TL", "#00FF00")
        create_stat_box(grid_f, "Kayıtlı Üye", str(toplam_uye), "#FFF")
        create_stat_box(grid_f, "Filo Büyüklüğü", str(toplam_arac), "#FFF")
        create_stat_box(grid_f, "Kiradaki Araç", str(toplam_arac - musait_arac), "#FF4444")

    # müşterileri görüp silebildiğimiz kısım
    def adm_users(self):
        for w in self.a_cont.winfo_children(): w.destroy()
        ctk.CTkLabel(self.a_cont, text="ÜYE YÖNETİMİ", font=("Arial", 26, "bold")).pack(pady=20, anchor="w")
        
        scroll = ctk.CTkScrollableFrame(self.a_cont, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for uid, u in list(self.engine.users.items()):
            f = ctk.CTkFrame(scroll, fg_color="#121212"); f.pack(fill="x", pady=5, ipady=10)
            ctk.CTkLabel(f, text=f"👤 {u.ad} (ID: {uid})", font=("Arial", 16)).pack(side="left", padx=20)
            ctk.CTkLabel(f, text=f"Bakiye: {u.bakiye} TL", font=("Arial", 14), text_color="#00AA00").pack(side="left", padx=20)
            
            # admin hesabını silme butonu koymadık
            if uid != "admin": 
                ctk.CTkButton(f, text="ÜYEYİ SİL", fg_color="#800000", width=100, 
                              command=lambda k=uid: [self.engine.users.pop(k), self.adm_users()]).pack(side="right", padx=20)

    # filodaki araçları zorla bakıma alıp veya müsait yapabildiğimiz yönetici paneli
    def adm_vehicles(self):
        for w in self.a_cont.winfo_children(): w.destroy()
        ctk.CTkLabel(self.a_cont, text="ARAÇ DURUM YÖNETİMİ", font=("Arial", 26, "bold")).pack(pady=20, anchor="w")
        
        scroll = ctk.CTkScrollableFrame(self.a_cont, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for v in self.engine.vehicles:
            f = ctk.CTkFrame(scroll, fg_color="#121212"); f.pack(fill="x", pady=5, ipady=10)
            ctk.CTkLabel(f, text=f"{v.marka} {v.model}", font=("Arial", 16, "bold")).pack(side="left", padx=20)
            
            status_text = "MÜSAİT" if v.musait_mi else "KİRADA"
            status_color = "#00AA00" if v.musait_mi else "#AA0000"
            ctk.CTkLabel(f, text=status_text, font=("Arial", 14, "bold"), text_color=status_color).pack(side="left", padx=30)
            
            def toggle_status(veh=v):
                veh.musait_mi = not veh.musait_mi
                self.adm_vehicles()
            
            btn_text = "Bakıma Al (Gizle)" if v.musait_mi else "Müsait Yap"
            ctk.CTkButton(f, text=btn_text, width=120, fg_color="#444", command=toggle_status).pack(side="right", padx=20)

    # veritabanına yeni araba kaydettiğimiz form
    def adm_add_vehicle(self):
        for w in self.a_cont.winfo_children(): w.destroy()
        ctk.CTkLabel(self.a_cont, text="YENİ ARAÇ EKLE", font=("Arial", 26, "bold")).pack(pady=20, anchor="w")
        
        form_f = ctk.CTkFrame(self.a_cont, fg_color="#111", corner_radius=10)
        form_f.pack(fill="x", padx=50, pady=20, ipady=30)
        
        marka_ent = ctk.CTkEntry(form_f, placeholder_text="Marka (Örn: Porsche)", width=400, height=45); marka_ent.pack(pady=10)
        model_ent = ctk.CTkEntry(form_f, placeholder_text="Model (Örn: 911 GT3)", width=400, height=45); model_ent.pack(pady=10)
        
        kat_var = ctk.StringVar(value="Spor")
        kat_menu = ctk.CTkOptionMenu(form_f, values=["Spor", "Elektrikli", "SUV", "Motor"], variable=kat_var, width=400, height=45)
        kat_menu.pack(pady=10)
        
        fiyat_ent = ctk.CTkEntry(form_f, placeholder_text="Saatlik Fiyat (TL)", width=400, height=45); fiyat_ent.pack(pady=10)
        
        def add_car():
            if not all([marka_ent.get(), model_ent.get(), fiyat_ent.get()]):
                self.show_vrx_msg("HATA", "Lütfen tüm alanları doldurun.", "red")
                return
            try:
                # fiyata harf girilirse sistem tekrar deneme
                fiyat = float(fiyat_ent.get())
                self.engine.admin_arac_ekle(marka_ent.get(), model_ent.get(), kat_var.get(), fiyat)
                self.show_vrx_msg("BAŞARILI", "Araç filoya eklendi.", "green")
                self.adm_vehicles() # ekledikten sonra araç listesi sayfasına yönlendir
            except ValueError:
                self.show_vrx_msg("HATA", "Fiyat sadece rakam olmalıdır.", "red")

        ctk.CTkButton(form_f, text="FİLOYA EKLE", fg_color="#00AA00", font=("Arial", 16, "bold"), height=50, width=400, command=add_car).pack(pady=20)

    # mağaza için ürün stoku ekleme sayfası
    def adm_store(self):
        for w in self.a_cont.winfo_children(): w.destroy()
        ctk.CTkLabel(self.a_cont, text="MAĞAZA VE STOK YÖNETİMİ", font=("Arial", 26, "bold")).pack(pady=20, anchor="w")
        
        for p in self.engine.products:
            f = ctk.CTkFrame(self.a_cont, fg_color="#121212"); f.pack(fill="x", pady=5, ipady=10)
            ctk.CTkLabel(f, text=f"{p.name}", font=("Arial", 16)).pack(side="left", padx=20)
            ctk.CTkLabel(f, text=f"Stok: {p.stock}", font=("Arial", 16, "bold"), text_color="#FFDD00").pack(side="left", padx=30)
            
            # stoğu artırıp sayfayı güncelletiyoruz
            ctk.CTkButton(f, text="+5 STOK EKLE", width=120, fg_color="#228B22", 
                          command=lambda x=p: [setattr(x, 'stock', x.stock+5), self.adm_store()]).pack(side="right", padx=20)

# dosya çalıştırıldığında uygulamayı başlat
if __name__ == "__main__":
    app = VRXApp()
    app.mainloop()
