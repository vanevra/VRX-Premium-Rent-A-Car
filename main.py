import customtkinter as ctk
from engine import AppEngine, User, Product

#premium hissi için genel temayı karanlık modda yaptım
ctk.set_appearance_mode("Dark")

#tüm pencereler ve ekranlar bu sınıfta
class VRXApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VRX Premium - Pro Console")
        self.geometry("1150x800")
        self.configure(fg_color="#000000") # Arka planı tamamen siyah yaparak şık bir görünüm sağladık
        
        # engine kısmını uygulamaya bağladık
        self.engine = AppEngine()
        self.show_login_screen()

    # ekranlar arası geçiş için önceki ekranı temizleyen fonksiyon
    def clear(self):
        for w in self.winfo_children(): w.destroy()

    # uygulama genelinde kullanılan uyarı pencereleri
    def show_vrx_msg(self, title, msg, color="#800000"):
        pop = ctk.CTkToplevel(self); pop.geometry("400x220"); pop.configure(fg_color="#0A0A0A")
        pop.attributes("-topmost", True) # Pencerenin hep en üstte kalmasını sağlar
        ctk.CTkLabel(pop, text=title, font=("Arial", 18, "bold"), text_color=color).pack(pady=15)
        ctk.CTkLabel(pop, text=msg, wraplength=320).pack(pady=10)
        ctk.CTkButton(pop, text="TAMAM", fg_color=color, command=pop.destroy).pack(pady=10)

    # güvenli ödeme simülasyonu
    def ask_payment(self, amount, callback, is_balance_load=False):
        pay_pop = ctk.CTkToplevel(self); pay_pop.geometry("400x500"); pay_pop.title("Güvenli Ödeme")
        pay_pop.attributes("-topmost", True); pay_pop.configure(fg_color="#0D0D0D")
        
        title_text = "BAKİYE YÜKLEME" if is_balance_load else "KREDİ KARTI ÖDEME"
        ctk.CTkLabel(pay_pop, text=title_text, font=("Arial", 22, "bold"), text_color="#800000").pack(pady=20)
        
        # kart bilgileri giriş alanları 
        ctk.CTkEntry(pay_pop, placeholder_text="Kart Sahibi Ad Soyad", width=320, height=40).pack(pady=5)
        ctk.CTkEntry(pay_pop, placeholder_text="0000 0000 0000 0000", width=320, height=40).pack(pady=5)
        
        f_row = ctk.CTkFrame(pay_pop, fg_color="transparent")
        f_row.pack(pady=5)
        ctk.CTkEntry(f_row, placeholder_text="AA/YY", width=155, height=40).pack(side="left", padx=5)
        ctk.CTkEntry(f_row, placeholder_text="CVV", width=155, height=40).pack(side="left", padx=5)
        
        action_text = f"Yüklenecek Tutar: {amount} TL" if is_balance_load else f"Ödenecek Tutar: {amount} TL"
        ctk.CTkLabel(pay_pop, text=action_text, font=("Arial", 18, "bold")).pack(pady=20)
        
        def process():
            pay_pop.destroy()
            callback() # ödeme onaylanınca yapılacak işleme geri döner
            if is_balance_load:
                self.show_vrx_msg("BAŞARILI", f"{amount} TL bakiyenize başarıyla yüklendi!", "green")

        ctk.CTkButton(pay_pop, text="İŞLEMİ ONAYLA", fg_color="#800000", height=45, width=320, command=process).pack(pady=10)

    # uygulamanın login ekranı
    def show_login_screen(self):
        self.clear()
        #VRX Logosu tasarımı
        ctk.CTkLabel(self, text="VRX", font=("Arial", 110, "bold"), text_color="#800000").pack(pady=(100, 0))
        ctk.CTkLabel(self, text="PREMIUM RENT A CAR", font=("Arial", 22, "bold"), text_color="#AAAAAA").pack(pady=(0, 30))
        
        # kullanıcı adı ve şifre giriş alanları
        self.u_ent = ctk.CTkEntry(self, placeholder_text="Kullanıcı ID", width=320, height=45); self.u_ent.pack(pady=5)
        self.p_ent = ctk.CTkEntry(self, placeholder_text="Şifre", show="*", width=320, height=45); self.p_ent.pack(pady=5)
        
        ctk.CTkButton(self, text="SİSTEME GİRİŞ", fg_color="#800000", width=320, height=50, command=self.handle_login).pack(pady=20)
        ctk.CTkButton(self, text="Hesap Oluştur", fg_color="transparent", text_color="#777", command=self.show_register_screen).pack()
        
        # admin girişi için kısayol butonu
        ctk.CTkButton(self, text="Admin Girişi", fg_color="transparent", text_color="#333", font=("Arial", 11),
                      command=lambda: [self.u_ent.delete(0, 'end'), self.u_ent.insert(0,"admin"), 
                                       self.p_ent.delete(0, 'end'), self.p_ent.insert(0,"123")]).pack(side="bottom", pady=10)

    # giriş bilgilerini kontrol eden ve yönlendiren fonksiyon
    def handle_login(self):
        uid, pwd = self.u_ent.get(), self.p_ent.get()
        if uid == "admin" and pwd == "123": self.show_admin_dashboard()
        elif self.engine.login(uid, pwd): self.show_user_dashboard()
        else: self.show_vrx_msg("HATA", "Giriş bilgileri hatalı!", "red")

    # yeni kullanıcı kayıt ekranı
    def show_register_screen(self):
        self.clear()
        ctk.CTkLabel(self, text="YENİ ÜYELİK", font=("Arial", 35, "bold"), text_color="#800000").pack(pady=40)
        uid = ctk.CTkEntry(self, placeholder_text="ID", width=300); uid.pack(pady=5)
        name = ctk.CTkEntry(self, placeholder_text="Ad Soyad", width=300); name.pack(pady=5)
        pwd = ctk.CTkEntry(self, placeholder_text="Şifre", show="*", width=300); pwd.pack(pady=5)
        adr = ctk.CTkEntry(self, placeholder_text="Açık Adres", width=300); adr.pack(pady=5)

        def do_reg():
            # yeni user nesnesini engine içindeki sözlüğe ekliyorz
            self.engine.users[uid.get()] = User(uid.get(), name.get(), pwd.get(), adr.get())
            self.show_vrx_msg("BAŞARILI", "Kaydınız oluşturuldu.")
            self.show_login_screen()
        ctk.CTkButton(self, text="KAYIT OL", fg_color="#800000", width=300, command=do_reg).pack(pady=20)

    # kullanıcı ana paneli 
    def show_user_dashboard(self):
        self.clear()
        # sol taraftaki menü
        side = ctk.CTkFrame(self, width=220, fg_color="#080808"); side.pack(side="left", fill="y")
        ctk.CTkLabel(side, text="VRX PREMIUM", font=("Arial", 22, "bold"), text_color="#800000").pack(pady=30)
        
        # içeriğin değiştiği scrollable alan
        self.cont = ctk.CTkScrollableFrame(self, fg_color="#000000"); self.cont.pack(side="right", expand=True, fill="both", padx=15, pady=15)
        
        m = [("Araç Filosu", self.show_fleet), ("VRX Store", self.show_store), ("Profil / Takip", self.show_profile), ("Çıkış", self.show_login_screen)]
        for t, c in m: ctk.CTkButton(side, text=t, fg_color="transparent", anchor="w", height=40, command=c).pack(fill="x", padx=10, pady=2)
        self.show_fleet() # varsayılan olarak filo ekranını açma

    # araçların listelendiği ve filtrelendiği ekran
    def show_fleet(self, f="Hepsi"):
        for w in self.cont.winfo_children(): w.destroy()
        bar = ctk.CTkFrame(self.cont, fg_color="transparent"); bar.pack(fill="x", pady=10)
        # filtreleme butonları kategorilere göre 
        for k in ["Hepsi", "Spor", "Elektrikli", "SUV", "Motor"]:
            ctk.CTkButton(bar, text=k, width=80, fg_color="#800000" if f==k else "#1A1A1A", command=lambda x=k: self.show_fleet(x)).pack(side="left", padx=2)

        for v in self.engine.vehicles:
            if f != "Hepsi" and v.kategori != f: continue
            # her bir araç için bir kart bilgisi oluşlturma
            card = ctk.CTkFrame(self.cont, fg_color="#0D0D0D", height=80); card.pack(fill="x", pady=4, padx=5)
            ctk.CTkLabel(card, text=f"{v.marka} {v.model}", font=("Arial", 16, "bold")).pack(side="left", padx=20)
            
            # aracın müsaitlik durumuna göre butonu pasif veya aktif yapıyor
            btn_text = "DETAYLAR" if v.musait_mi else "KİRADA"
            btn_color = "#333" if v.musait_mi else "#400000"
            btn_state = "normal" if v.musait_mi else "disabled"
            
            ctk.CTkButton(card, text=btn_text, width=100, fg_color=btn_color, state=btn_state,
                          command=lambda x=v: self.show_vehicle_details(x)).pack(side="right", padx=15)

    # seçilen aracın detaylarını gösteren pencere ve kiralama işlemi
    def show_vehicle_details(self, v):
        pop = ctk.CTkToplevel(self); pop.geometry("450x550"); pop.configure(fg_color="#080808"); pop.attributes("-topmost", True)
        ctk.CTkLabel(pop, text=f"{v.marka} {v.model}", font=("Arial", 24, "bold"), text_color="#800000").pack(pady=20)
        
        desc = f"Kategori: {v.kategori}\nMotor Gücü: {v.hp} HP\nYakıt: {v.yakit}\nKM: {v.km}\n\nSaatlik Fiyat: {v.saatlik_fiyat} TL"
        ctk.CTkLabel(pop, text=desc, font=("Arial", 16), justify="left").pack(pady=10)
        
        coupon_ent = ctk.CTkEntry(pop, placeholder_text="Kupon Kodu (Varsa)", width=200)
        coupon_ent.pack(pady=10)

        def rent():
            price = v.saatlik_fiyat
            # kupon kodu kontrolü 
            if coupon_ent.get() == "GIFT50":
                price -= 50
                self.show_vrx_msg("KUPON UYGULANDI", "GIFT50 kodu ile 50 TL indirim yapıldı!", "green")
            
            # bakiye kontrolü
            if self.engine.current_user.bakiye >= price:
                self.engine.current_user.bakiye -= price
                v.musait_mi = False #artık bu araç kiralanamaz
                self.engine.current_user.kiralanan_araclar.append(f"{v.marka} {v.model}")
                pop.destroy()
                self.show_vrx_msg("BAŞARILI", f"{v.marka} başarıyla kiralandı. Keyifli sürüşler!")
                self.show_fleet()
            else:
                self.show_vrx_msg("YETERSİZ BAKİYE", "Lütfen bakiye yükleyiniz.", "red")

        ctk.CTkButton(pop, text="KİRALAMAYI TAMAMLA", fg_color="#800000", height=45, command=rent).pack(pady=20)

    # mağaza sekmesi
    def show_store(self):
        for w in self.cont.winfo_children(): w.destroy()
        ctk.CTkLabel(self.cont, text="MAĞAZA VE EKİPMAN", font=("Arial", 25, "bold")).pack(pady=15)
        
        for p in self.engine.products:
            card = ctk.CTkFrame(self.cont, fg_color="#0D0D0D", height=100); card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=f"{p.name}\nStok: {p.stock}", font=("Arial", 15)).pack(side="left", padx=20)
            ctk.CTkLabel(card, text=f"{p.price} TL", font=("Arial", 18, "bold"), text_color="#800000").pack(side="left", padx=40)
            
            def buy_process(prod=p):
                # adres onayı penceresi
                adr_pop = ctk.CTkToplevel(self); adr_pop.geometry("350x300"); adr_pop.attributes("-topmost", True)
                ctk.CTkLabel(adr_pop, text="KARGO ADRES ONAYI", font=("Arial", 16, "bold")).pack(pady=15)
                ctk.CTkLabel(adr_pop, text=f"Teslimat Adresi:\n\n{self.engine.current_user.adres}", wraplength=300).pack(pady=10)
                
                def final():
                    adr_pop.destroy()
                    def complete_order():
                        self.show_vrx_msg("BAŞARILI", "Siparişiniz kargoya verilmek üzere hazırlandı!")
                        prod.stock -= 1 #stoktan düşüyor 
                        self.engine.current_user.siparisler.append({"urun": prod.name, "durum": "Hazırlanıyor"})
                        self.show_store()
                    # ödeme ekranı gelio 
                    self.ask_payment(prod.price, complete_order)
                
                ctk.CTkButton(adr_pop, text="BU ADRESE GÖNDER", fg_color="#800000", command=final).pack(pady=10)
                ctk.CTkButton(adr_pop, text="ADRESİ DEĞİŞTİR", fg_color="#333", command=lambda: [adr_pop.destroy(), self.show_profile()]).pack()

            ctk.CTkButton(card, text="SATIN AL", fg_color="#800000", command=buy_process if p.stock > 0 else None).pack(side="right", padx=20)

    # profil bakiye yükleme ve sipariş takibi ekranı
    def show_profile(self):
        for w in self.cont.winfo_children(): w.destroy()
        u = self.engine.current_user
        
        # üst kullanıcı paneli bilgileri
        top_frame = ctk.CTkFrame(self.cont, fg_color="#0A0A0A"); top_frame.pack(fill="x", pady=10, padx=5)
        ctk.CTkLabel(top_frame, text=f"Hesap: {u.ad}", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkLabel(top_frame, text=f"Mevcut Bakiye: {u.bakiye} TL", font=("Arial", 18), text_color="#800000").pack(pady=5)
        ctk.CTkLabel(top_frame, text=f"Kayıtlı Adres: {u.adres}", wraplength=500).pack(pady=10)
        
        # bakiye yükleme kısmı
        new_b = ctk.CTkEntry(top_frame, placeholder_text="Yüklenecek Tutar (TL)", width=200); new_b.pack(pady=5)
        def load_balance():
            val = new_b.get()
            if not val.isdigit():
                self.show_vrx_msg("HATA", "Lütfen geçerli bir tutar girin.", "red")
                return
            amount = float(val)
            # ödeme onayından sonra bakiyeyi güncellenio
            self.ask_payment(amount, lambda: [setattr(u, 'bakiye', u.bakiye + amount), self.show_profile()], is_balance_load=True)

        ctk.CTkButton(top_frame, text="KREDİ KARTI İLE BAKİYE YÜKLE", fg_color="#800000", command=load_balance).pack(pady=10)

        # kiralama ve kargo için alt takip paneli
        bottom_frame = ctk.CTkFrame(self.cont, fg_color="transparent"); bottom_frame.pack(fill="both", expand=True, pady=10)
        
        # aktif kiralamalar listesi
        left_f = ctk.CTkFrame(bottom_frame, fg_color="#0D0D0D"); left_f.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(left_f, text="AKTİF KİRALAMALARIM", font=("Arial", 16, "bold"), text_color="#800000").pack(pady=10)
        if not u.kiralanan_araclar:
            ctk.CTkLabel(left_f, text="Şu an kiraladığınız bir araç yok.", text_color="#777").pack(pady=5)
        else:
            for arac in u.kiralanan_araclar:
                ctk.CTkLabel(left_f, text=f"🚘 {arac} (Kullanımda)").pack(pady=2)

        # kargo sipariş takibi listesi
        right_f = ctk.CTkFrame(bottom_frame, fg_color="#0D0D0D"); right_f.pack(side="right", fill="both", expand=True, padx=5)
        ctk.CTkLabel(right_f, text="KARGO & SİPARİŞ TAKİBİ", font=("Arial", 16, "bold"), text_color="#800000").pack(pady=10)
        if not u.siparisler:
            ctk.CTkLabel(right_f, text="Henüz bir siparişiniz bulunmuyor.", text_color="#777").pack(pady=5)
        else:
            for siparis in u.siparisler:
                ctk.CTkLabel(right_f, text=f"📦 {siparis['urun']} - Durum: {siparis['durum']}", text_color="green").pack(pady=2)

    # admin paneli
    def show_admin_dashboard(self):
        self.clear()
        side = ctk.CTkFrame(self, width=220, fg_color="#080808"); side.pack(side="left", fill="y")
        ctk.CTkLabel(side, text="ADMİN KONTROL", font=("Arial", 20, "bold"), text_color="#800000").pack(pady=30)
        
        self.a_cont = ctk.CTkScrollableFrame(self, fg_color="#000000"); self.a_cont.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        # üye Listesi ve silme Yetkisi
        def adm_users():
            for w in self.a_cont.winfo_children(): w.destroy()
            ctk.CTkLabel(self.a_cont, text="ÜYE LİSTESİ", font=("Arial", 18, "bold")).pack(pady=10)
            for uid, u in list(self.engine.users.items()):
                f = ctk.CTkFrame(self.a_cont, fg_color="#0D0D0D"); f.pack(fill="x", pady=2)
                ctk.CTkLabel(f, text=f"{u.ad} - {uid}").pack(side="left", padx=10)
                if uid != "admin": # Admin kendini silemez
                    ctk.CTkButton(f, text="ÜYEYİ SİL", fg_color="red", width=80, command=lambda k=uid: [self.engine.users.pop(k), adm_users()]).pack(side="right", padx=5)

        #ürün stok güncelleme
        def adm_store():
            for w in self.a_cont.winfo_children(): w.destroy()
            ctk.CTkLabel(self.a_cont, text="MAĞAZA STOK YÖNETİMİ", font=("Arial", 18, "bold")).pack(pady=10)
            for p in self.engine.products:
                f = ctk.CTkFrame(self.a_cont, fg_color="#0D0D0D"); f.pack(fill="x", pady=2)
                ctk.CTkLabel(f, text=f"{p.name} (Stok: {p.stock})").pack(side="left", padx=10)
                ctk.CTkButton(f, text="+1 EKLE", width=60, command=lambda x=p: [setattr(x, 'stock', x.stock+1), adm_store()]).pack(side="right", padx=5)

        # araçların müsaitliğini değiştirme 
        def adm_vehicles():
            for w in self.a_cont.winfo_children(): w.destroy()
            ctk.CTkLabel(self.a_cont, text="ARAÇ MÜSAİTLİK YÖNETİMİ", font=("Arial", 18, "bold")).pack(pady=10)
            for v in self.engine.vehicles:
                f = ctk.CTkFrame(self.a_cont, fg_color="#0D0D0D"); f.pack(fill="x", pady=2)
                ctk.CTkLabel(f, text=f"{v.marka} {v.model}").pack(side="left", padx=10)
                
                status_text = "Müsait" if v.musait_mi else "Kirada"
                status_color = "green" if v.musait_mi else "red"
                ctk.CTkLabel(f, text=status_text, text_color=status_color).pack(side="left", padx=20)
                
                def toggle_status(veh=v):
                    veh.musait_mi = not veh.musait_mi
                    adm_vehicles()
                
                btn_text = "Kirada Yap" if v.musait_mi else "Müsait Yap"
                btn_color = "#660000" if v.musait_mi else "#006600"
                ctk.CTkButton(f, text=btn_text, width=90, fg_color=btn_color, command=toggle_status).pack(side="right", padx=10)

        # admin yan menüsü
        ctk.CTkButton(side, text="Üyeleri Yönet", command=adm_users, fg_color="transparent", anchor="w").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(side, text="Mağaza & Stok", command=adm_store, fg_color="transparent", anchor="w").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(side, text="Araçları Yönet", command=adm_vehicles, fg_color="transparent", anchor="w").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(side, text="Sistemden Çık", command=self.show_login_screen, fg_color="#444").pack(side="bottom", pady=20, fill="x", padx=10)
        
        adm_users() # ilk açılışta üye listesini gösterior

# uygulamayı başlatmak için ana döngü
if __name__ == "__main__":
    app = VRXApp(); app.mainloop()