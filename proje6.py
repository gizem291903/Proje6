import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

# Film sınıfı
class tarif:
    def __init__(self, tarif_adi, malzemeler, tarif):
        self.tarif_adi = tarif_adi
        self.malzemeler = malzemeler
        self.tarif = tarif

# Kullanıcı sınıfı
class Kullanici:
    def __init__(self, kullanici_id, kullanici_adi, sifre):
        self.kullanici_id = kullanici_id
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre


class malzeme:
    def __init__(self, malzeme_adi, malzeme_miktari):
        self.malzeme_adi = malzeme_adi
        self.malzeme_miktari = malzeme_miktari


class TarifEklePenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarif Ekle")
        self.root.geometry("600x400")

        self.tarif_adi_label = tk.Label(root, text="Tarif Adı:")
        self.tarif_adi_label.pack()
        self.tarif_adi_entry = tk.Entry(root)
        self.tarif_adi_entry.pack()

        self.malzemeler_label = tk.Label(root, text="Malzemeler:")
        self.malzemeler_label.pack()
        self.malzemeler_entry = tk.Entry(root)
        self.malzemeler_entry.pack()

        self.tarif_label = tk.Label(root, text="Tarif:")
        self.tarif_label.pack()
        self.tarif_entry = tk.Entry(root)
        self.tarif_entry.pack()

        self.ekle_button = tk.Button(root, text="Ekle", command=self.tarif_ekle)
        self.ekle_button.pack()

    def tarif_ekle(self):
        tarif_adi = self.tarif_adi_entry.get()
        malzemeler = self.malzemeler_entry.get()
        tarif = self.tarif_entry.get()

        # Veritabanına film ekle
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Tarifler (tarif_adi, malzemeler, tarif) VALUES (?, ?, ?)", (tarif_adi, malzemeler, tarif))
        connection.commit()
        connection.close()

        tk.messagebox.showinfo("Başarılı", "Tarif başarıyla eklendi.")
        self.root.destroy()  # Pencereyi kapat


class TarifleriGoruntulePenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarifleri Görüntüle")
        self.root.geometry("800x400")

        self.arama_label = tk.Label(root, text="Tarif Adı:")
        self.arama_label.pack()
        self.arama_entry = tk.Entry(root)
        self.arama_entry.pack()

        self.ara_button = tk.Button(root, text="Ara", command=self.tarif_ara)
        self.ara_button.pack()

        # Tablo oluştur
        self.tarif_tree = ttk.Treeview(root, columns=("Tarif Adı", "Malzemeler", "Tarif"))
        self.tarif_tree.pack()

        # Sütunları yapılandır
        self.tarif_tree.heading("#0", text="")
        self.tarif_tree.heading("#1", text="Tarif Adı")
        self.tarif_tree.heading("#2", text="Malzemeler")
        self.tarif_tree.heading("#3", text="Tarif")

        # Veritabanındaki tüm tarifleri listele
        self.list_all_tarifs()

        # Tablo tıklama olayını bağla
        self.tarif_tree.bind("<Double-1>", self.show_tarif_details)

        self.favori_listeme_ekle_button = tk.Button(root, text="Favoriler Listeme Ekle", command=self.favori_listeme_ekle)
        self.favori_listeme_ekle_button.pack()

        self.geri_don_button = tk.Button(root, text="Geri Dön", command=self.geri_don)
        self.geri_don_button.pack()

    def list_all_tarifs(self):
        # Tüm tarifleri veritabanından al ve tabloya ekle
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT tarif_adi, malzemeler, tarif FROM tarifler")
        tarifler = cursor.fetchall()
        connection.close()

        for tarif in tarifler:
            self.tarif_tree.insert("", tk.END, values=tarif)



    def favori_listeme_ekle(self):
        selected_tarif = self.tarif_tree.item(self.tarif_tree.selection())['values'][0]

        # İzleme listesine film ekle
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO favorilerListesi (tarif_adi) VALUES (?)", (selected_tarif,))
        connection.commit()
        connection.close()

        tk.messagebox.showinfo("Favoriler Listeme Eklendi", "Favoriler listeme eklendi.")

    def geri_don(self):
        self.root.destroy()  # Pencereyi kapat

    def tarif_ara(self):
        tarif_adi = self.arama_entry.get()

        # Veritabanından tarifleri ara ve tabloya ekle
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT tarif_adi, malzemeler, tarif FROM tarifler WHERE tarif_adi LIKE ?",
                       ('%' + tarif_adi + '%',))
        tarifler = cursor.fetchall()
        connection.close()

        # Tabloyu temizle
        self.tarif_tree.delete(*self.tarif_tree.get_children())

        for tarif in tarifler:
            self.tarif_tree.insert("", tk.END, values=tarif)

    def show_tarif_details(self, event):
        # Seçilen tarifin detaylarını göster
        item = self.tarif_tree.selection()[0]
        tarif_details = self.tarif_tree.item(item, "values")
        messagebox.showinfo(tarif_details[0], f"Malzemeler: {tarif_details[1]}\nTarif: {tarif_details[2]}")


# İzleme listesi penceresi
class favorilerListesiPenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Favoriler Listem")
        self.root.geometry("600x400")

        self.favoriler_liste = tk.Listbox(root, width=50, height=15)
        self.favoriler_liste.pack()

        self.favoriler_liste.bind('<Double-Button-1>', self.yemek_detaylarini_goster)  # Çift tıklama olayı

        self.kaldir_button = tk.Button(root, text="Favoriler Listemden Kaldır", command=self.kaldir)
        self.kaldir_button.pack()

        self.geri_don_button = tk.Button(root, text="Geri Dön", command=self.geri_don)
        self.geri_don_button.pack()

        # İzleme listesini göster
        self.show_favoriler_listesi()

    def show_favoriler_listesi(self):
        # İzleme listesini veritabanından al ve göster
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT tarif_adi FROM favorilerListesi")
        favoriler_listesi = cursor.fetchall()
        connection.close()

        self.favoriler_liste.delete(0, tk.END)  # Önceki listeyi temizle
        for tarif in favoriler_listesi:
            self.favoriler_liste.insert(tk.END, tarif[0])

    def yemek_detaylarini_goster(self, event):
        # Çift tıklama olayında yemek detaylarını göster
        selected_tarif = self.favoriler_liste.get(tk.ACTIVE)

        # Yemeğin detaylarını veritabanından al
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tarifler WHERE tarif_adi=?", (selected_tarif,))
        yemek_detaylari = cursor.fetchone()
        connection.close()

        # Yemeğin detaylarını göster
        if yemek_detaylari:
            tk.messagebox.showinfo("Yemek Detayları", f"Yemek Adı: {yemek_detaylari[0]}\nMalzemeler: {yemek_detaylari[1]}\nTarif: {yemek_detaylari[2]}")
        else:
            tk.messagebox.showwarning("Uyarı", "Seçilen yemek bulunamadı.")

    def kaldir(self):
        selected_tarif = self.favoriler_liste.get(tk.ACTIVE)

        # İzleme listesinden filmi kaldır
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM favorilerListesi WHERE tarif_adi=?", (selected_tarif,))
        connection.commit()
        connection.close()

        tk.messagebox.showinfo("Favoriler Listemden Kaldır", "Favoriler listesinden kaldırıldı.")

    def geri_don(self):
        self.root.destroy()  # Pencereyi kapat

# Film değerlendirme penceresi
class tarifDegerlendirPenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarif Değerlendir")
        self.root.geometry("600x400")

        self.tarif_liste = tk.Listbox(root, width=50, height=10)
        self.tarif_liste.pack()

        self.degerlendir_button = tk.Button(root, text="Değerlendir", command=self.tarif_degerlendir)
        self.degerlendir_button.pack()

        self.puan_label = tk.Label(root, text="Puan Ver (1-10):")
        self.puan_label.pack()
        self.puan_entry = tk.Entry(root)
        self.puan_entry.pack()

        self.ortalama_label = tk.Label(root, text="Ortalama Puan:")
        self.ortalama_label.pack()
        self.ortalama_puan_label = tk.Label(root, text="")
        self.ortalama_puan_label.pack()

        # İzleme listesinden filmleri al ve listele
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT tarif_adi FROM tarifler")
        tarifler = cursor.fetchall()
        connection.close()

        for tarif in tarifler:
            self.tarif_liste.insert(tk.END, tarif[0])

    def tarif_degerlendir(self):
        selected_tarif = self.tarif_liste.get(tk.ACTIVE)
        puan = self.puan_entry.get()

        if puan.isdigit() and 1 <= int(puan) <= 10:
            # Puanı veritabanına kaydet
            connection = sqlite3.connect("tarif.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tarifDegerlendirme (tarif_adi, puan) VALUES (?, ?)", (selected_tarif, puan))
            connection.commit()

            # Ortalama puanı hesapla ve göster
            cursor.execute("SELECT AVG(puan) FROM tarifDegerlendirme WHERE tarif_adi=?", (selected_tarif,))
            ortalama_puan = cursor.fetchone()[0]
            connection.close()

            if ortalama_puan:
                self.ortalama_puan_label.config(text=f"Ortalama Puan: {ortalama_puan:.2f}")
            else:
                self.ortalama_puan_label.config(text="Henüz değerlendirme yapılmadı.")
        else:
            tk.messagebox.showerror("Hata", "Geçersiz puan. Lütfen 1 ile 10 arasında bir sayı girin.")


# İçerikleri görüntüleme penceresi
class malzemeleriGoruntulePenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Malzemeleri Görüntüle")
        self.root.geometry("600x400")

        self.arama_label = tk.Label(root, text="Tarif Adı:")
        self.arama_label.pack()
        self.arama_entry = tk.Entry(root)
        self.arama_entry.pack()

        self.ara_button = tk.Button(root, text="Ara", command=self.malzeme_ara)
        self.ara_button.pack()

        self.malzemeler_liste = tk.Listbox(root, width=50, height=15)
        self.malzemeler_liste.pack()

        self.geri_don_button = tk.Button(root, text="Geri Dön", command=self.geri_don)
        self.geri_don_button.pack()

        # Tüm içerikleri listele
        self.list_all_malzemeler()

    def list_all_malzemeler(self):
        # Tüm içerikleri veritabanından al ve listele
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT malzeme_adi, malzeme_miktari, tarif_adi FROM Malzeme")
        malzemeler = cursor.fetchall()
        connection.close()

        for malzeme in malzemeler:
            self.malzemeler_liste.insert(tk.END, f"{malzeme[0]} - {malzeme[1]} tane - {malzeme[2]}")

    def malzeme_ara(self):
        tarif_adi = self.arama_entry.get()

        # Veritabanından içerik ara
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT malzeme_adi, malzeme_miktari, tarif_adi FROM Malzeme WHERE tarif_adi LIKE ?", ('%' + tarif_adi + '%',))
        malzemeler = cursor.fetchall()
        connection.close()

        self.malzemeler_liste.delete(0, tk.END)  # Önceki listeyi temizle
        for malzeme in malzemeler:
            self.malzemeler_liste.insert(tk.END, f"{malzeme[0]} -  {malzeme[1]} tane -  {malzeme[2]}")

    def geri_don(self):
        self.root.destroy()  # Pencereyi kapat


# Ana sayfa
class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Ana Sayfa")
        self.root.geometry("500x400")

        # Butonların boyutunu ve yerleşimini ayarla
        button_width = 20
        button_height = 2

        self.tarif_ekle_button = tk.Button(root, text="Tarif Ekle", command=self.open_tarif_ekle_penceresi, width=button_width, height=button_height)
        self.tarif_ekle_button.place(relx=0.5, rely=0.2, anchor='center')

        self.tarifleri_goruntule_button = tk.Button(root, text="Tarifleri Görüntüle", command=self.open_tarifleri_goruntule_penceresi, width=button_width, height=button_height)
        self.tarifleri_goruntule_button.place(relx=0.5, rely=0.35, anchor='center')

        self.icerikleri_goruntule_button = tk.Button(root, text="Malzemeleri Görüntüle", command=self.open_malzemeleri_goruntule_penceresi, width=button_width, height=button_height)
        self.icerikleri_goruntule_button.place(relx=0.5, rely=0.5, anchor='center')

        self.favoriler_listem_button = tk.Button(root, text="Favoriler Listem", command=self.open_favoriler_listesi_penceresi, width=button_width, height=button_height)
        self.favoriler_listem_button.place(relx=0.5, rely=0.65, anchor='center')

        self.tarif_degerlendir_button = tk.Button(root, text="Tarif Değerlendir", command=self.open_tarif_degerlendir_penceresi, width=button_width, height=button_height)
        self.tarif_degerlendir_button.place(relx=0.5, rely=0.8, anchor='center')

        self.back_button = tk.Button(root, text="Geri Dön", command=self.go_back, width=button_width, height=button_height)
        self.back_button.place(relx=1, rely=1, anchor='se')


    def open_tarif_ekle_penceresi(self):
        tarif_ekle_penceresi = tk.Toplevel(self.root)
        TarifEklePenceresi(tarif_ekle_penceresi)

    def open_tarifleri_goruntule_penceresi(self):
        tarifleri_goruntule_penceresi = tk.Toplevel(self.root)
        TarifleriGoruntulePenceresi(tarifleri_goruntule_penceresi)

    def open_favoriler_listesi_penceresi(self):
        favoriler_listesi_penceresi = tk.Toplevel(self.root)
        favorilerListesiPenceresi(favoriler_listesi_penceresi)

    def open_tarif_degerlendir_penceresi(self):
        tarif_degerlendir_penceresi = tk.Toplevel(self.root)
        tarifDegerlendirPenceresi(tarif_degerlendir_penceresi)

    def open_malzemeleri_goruntule_penceresi(self):
        malzemeleri_goruntule_penceresi = tk.Toplevel(self.root)
        malzemeleriGoruntulePenceresi(malzemeleri_goruntule_penceresi)


    def go_back(self):
        self.root.destroy()  # Ana sayfayı kapat
        login_page = tk.Tk()
        UserLoginApp(login_page)
        login_page.mainloop()

# Kullanıcı Giriş Sayfası
class UserLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kullanıcı Giriş")
        self.root.geometry("400x300")

        self.username_label = tk.Label(root, text="Kullanıcı Adı:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Şifre:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Giriş Yap", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(root, text="Kayıt Ol", command=self.register)
        self.register_button.pack()

        self.help_button = tk.Button(root, text="Kullanım Kılavuzu", command=self.show_help)
        self.help_button.place(relx=0, rely=1, anchor='sw')

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kullanıcı adı ve şifre kontrolü
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            messagebox.showinfo("Giriş Başarılı", f"Hoş Geldiniz, {username}!")
            self.open_main_page()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kullanıcıyı veritabanına ekle
        connection = sqlite3.connect("tarif.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Kayıt işlemi başarıyla tamamlandı.")

    def open_main_page(self):
        # Ana sayfaya yönlendirme
        self.root.destroy()  # Giriş sayfasını kapat
        main_page = tk.Tk()
        MainPage(main_page)
        main_page.mainloop()

    def show_help(self):
        help_text = """
Kullanım Kılavuzu:

1. Kullanıcı Giriş Sayfası:
    - Kullanıcı adı ve şifrenizi ilgili alanlara girin.
    - "Giriş Yap" butonuna tıklayarak sisteme giriş yapın.
    - Eğer daha önce kayıt olmadıysanız, "Kayıt Ol" butonuna tıklayarak yeni bir hesap oluşturabilirsiniz.
    - Yardım almak için "Kullanım Kılavuzu" butonuna tıklayabilirsiniz.

2. Ana Sayfa:
    - "Tarif Ekle" butonuna tıklayarak yeni bir tarif ekleyebilirsiniz.
    - "Tarifleri Görüntüle" butonuna tıklayarak mevcut tarifleri listeleyebilir ve favoriler listenize ekleyebilirsiniz.
    - "Malzemeleri Görüntüle" butonuna tıklayarak yemeğinizin ıd'sine göre lazım olcak malzeme miktarını listeleyebilirsiniz.
    - "Favoriler Listem" butonuna tıklayarak favoriler listenizi görüntüleyebilir ve favoriler listesinden tarifleri kaldırabilirsiniz.
    - "Tarif Değerlendir" butonuna tıklayarak tarifleri değerlendirebilir ve puanlayabilirsiniz.
    - "Geri Dön" butonuna tıklayarak giriş sayfasına geri dönebilirsiniz.
        """
        messagebox.showinfo("Kullanım Kılavuzu", help_text)



if __name__ == "__main__":

    # Veritabanı bağlantısını oluştur
    connection = sqlite3.connect("tarif.db")
    cursor = connection.cursor()

    # Tabloları oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tarifler (
                     tarif_adi TEXT NOT NULL,
                     malzemeler TEXT NOT NULL,
                     tarif TEXT NOT NULL
                     )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Kullanicilar (
                     id INTEGER PRIMARY KEY,
                     kullanici_adi TEXT NOT NULL,
                     sifre TEXT NOT NULL
                     )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Malzeme (
                     tarif_adi TEXT NOT NULL,
                     malzeme_adi TEXT NOT NULL,
                     malzeme_miktari INTEGER NOT NULL,
                     FOREIGN KEY (tarif_adi) REFERENCES Tarifler(tarif_adi)
                     )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS favorilerListesi (
                         id INTEGER PRIMARY KEY,
                         tarif_adi TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tarifDegerlendirme (
                        id INTEGER PRIMARY KEY,
                        tarif_adi TEXT,
                        puan INTEGER
                    )''')

    # Örnek tarifler
    Tarifler = [
        ("Mercimek Çorbası", "Kırmızı mercimek, soğan, havuç, patates, su, tuz, karabiber, kimyon",
         "1 su bardağı kırmızı mercimeği yıkayıp süzün. Soğanı küçük küçük doğrayın. Havucu rendeleyin. Patatesleri küp küp doğrayın. Bir tencereye biraz yağ ekleyin. Soğanı ve havucu ekleyip kavurun. Ardından patatesleri ekleyip kavurmaya devam edin. Mercimeği ekleyin. Üzerine suyu ekleyin. Tuz ve baharatları ekleyin. Pişirin ve blenderdan geçirip sıcak servis yapın."),
        ("Tavuklu Pilav", "Pirinç, tavuk göğsü, tereyağı, su, tuz, karabiber",
         "Pirinci yıkayıp süzün. Tavuk göğsünü küp küp doğrayın. Tencerede tereyağını eritin. Tavukları ekleyip kavurun. Pirinci ekleyip kavurmaya devam edin. Üzerine suyu ekleyin. Tuz ve baharatları ekleyin. Pilav suyunu çekene kadar pişirin."),
        ("Izgara Balık", "Levrek, zeytinyağı, limon, tuz, karabiber, kekik",
         "Balıkları temizleyin ve fileto haline getirin. Zeytinyağı, limon suyu ve baharatlarla bir marinasyon hazırlayın. Balıkları marinasyona koyun ve buzdolabında bir süre dinlendirin. Ardından ızgarada her iki tarafını da güzelce pişirin."),
        ("Mantı", "Un, kıyma, soğan, yoğurt, sarımsak, tereyağı, nane, tuz",
         "Unu yoğurma kabına alın. Üzerine su ekleyerek kulak memesi yumuşaklığında bir hamur elde edene kadar yoğurun. Hamuru merdaneyle açın. Küçük kareler kesin. Kıyma, soğan ve baharatlarla harcı hazırlayın. Hamurların içine harçtan koyun. Mantıları kaynayan suya atın. Pişince süzün. Üzerine sarımsaklı yoğurt ve tereyağında kızdırılmış nane dökerek servis yapın."),
        ("Omlet", "Yumurta, süt, tereyağı, kaşar peyniri, domates, biber, tuz, karabiber",
         "Yumurtaları bir kasede çırpın. Süt ekleyin ve karıştırın. Tavaya tereyağını ekleyin. İnce doğranmış domates ve biberleri ekleyin. Biraz kavurduktan sonra üzerine yumurta karışımını dökün. Altını kısın ve üzerine rendelenmiş kaşar peynirini serpin. Omleti katlayıp pişirin."),
        ("Fırında Tavuk", "Tavuk but, zeytinyağı, limon, tuz, karabiber, kekik",
         "Tavuk butlarını yıkayın ve kurulayın. Zeytinyağı, limon suyu ve baharatlarla bir marinasyon hazırlayın. Tavuk butlarını marinasyona koyun ve buzdolabında bir süre dinlendirin. Ardından fırın tepsisine alın ve önceden ısıtılmış fırında pişirin."),
        ("Köfte", "Kıyma, soğan, maydanoz, ekmek içi, yumurta, tuz, karabiber, kimyon",
         "Kıymayı bir kaba alın. İnce doğranmış soğanı ekleyin. Maydanozu ince kıyın. Ekmek içini ıslatıp sıkarak ekleyin. Yumurta, tuz ve baharatları ekleyin. Malzemeleri iyice yoğurun. Köfte harcından parçalar alıp yuvarlayın ve şekil verin. Tavada veya ızgarada pişirin."),
        ("Makarna", "Makarna, su, tuz, su, zeytinyağı",
         "Bir tencerede suyu kaynatın. Kaynayan suya tuz ve biraz zeytinyağı ekleyin. Makarnayı ekleyip paketin üzerindeki süre kadar haşlayın. Haşlanan makarnayı süzün ve isteğe göre sosla servis yapın."),
        ("Sebzeli Kızartma", "Patates, havuç, kabak, sogan, biber, sıvıyağ, tuz, karabiber",
         "Patates, havuç ve kabakları soyun ve dilimleyin. Soğanı ve biberleri doğrayın. Bir tavada sıvıyağı kızdırın. Doğradığınız sebzeleri tavaya alın. Tuz ve karabiber ekleyin. Sebzeler yumuşayana kadar kızartın."),
        ("Pancake", "Un, süt, yumurta, şeker, tuz, tereyağı, bal veya akçaağaç şurubu",
         "Unu bir kaba alın. Üzerine süt, yumurta, şeker ve tuzu ekleyin. Karıştırarak kıvamlı bir hamur elde edin. Tavaya bir parça tereyağı ekleyin ve eritin. Hamurdan bir kepçe alıp tavaya dökün. Her iki tarafını da altın rengi olana kadar pişirin. Üzerine bal veya akçaağaç şurubu gezdirerek servis yapın."),
        ("Karides Güveç", "Karides, domates, biber, soğan, sarımsak, zeytinyağı, limon, tuz, karabiber",
         "Karidesleri temizleyin. Domatesleri ve biberleri doğrayın. Soğanı ve sarımsağı ince doğrayın. Güveç kaplarına sırasıyla karidesleri, domatesleri, biberleri, soğanı ve sarımsağı yerleştirin. Üzerlerine zeytinyağı, limon suyu, tuz ve karabiber serpin. Önceden ısıtılmış fırında pişirin."),
        ("Mantarlı Tavuk Sote", "Tavuk göğsü, mantar, soğan, sivri biber, sarımsak, tuz, karabiber, sıvıyağ",
         "Tavuk göğsünü küp küp doğrayın. Mantarları dilimleyin. Soğanı ve biberleri doğrayın. Bir tavada sıvıyağı kızdırın. Tavukları ekleyip kavurun. Ardından mantarları, soğanı ve biberleri ekleyin. Sarımsağı ezin ve ekleyin. Tuz ve karabiber ekleyip pişirin."),
        ("Salata", "Marul, domates, salatalık, biber, zeytinyağı, limon suyu, tuz",
         "Marulu, domatesi, salatalığı ve biberi doğrayın. Bir kasede zeytinyağı, limon suyu ve tuzu karıştırın. Doğranmış sebzeleri bu sosla karıştırın. Servis yapın."),
        ("Fırın Patates", "Patates, zeytinyağı, tuz, kekik",
         "Patatesleri yıkayın ve kurulayın. Dilimleyin. Bir kabın içinde zeytinyağı, tuz ve kekikle harmanlayın. Patates dilimlerini bu karışımla kaplayın. Önceden ısıtılmış fırında kızarana kadar pişirin."),
        ("Karnabahar Kızartması", "Karnabahar, un, yumurta, sıvıyağ, tuz",
         "Karnabaharı çiçeklerine ayırın ve yıkayın. Kaynar suda biraz haşlayın. Un, yumurta ve tuzu bir kasede çırpın. Haşlanmış karnabahar çiçeklerini bu karışıma bulayın. Tavada sıvıyağı kızdırın ve karnabaharları kızartın."),
        ("Sulu Köfte", "Kıyma, pirinç, soğan, tuz, karabiber, su",
         "Kıymayı bir kaba alın. İnce doğranmış soğanı, yıkanmış pirinci, tuz ve baharatları ekleyin. İyice yoğurun. Küçük köfteler yapın. Tencereye dizin. Üzerine su ekleyin. Pişirin."),
        ("Mısır Ekmeği", "Mısır unu, süt, yumurta, sıvıyağ, kabartma tozu, tuz",
         "Tüm malzemeleri bir kapta karıştırın. Kıvamı koyu olacak şekilde ayarlayın. Fırın tepsisine yağlı kağıt serin. Hamuru yayın. Önceden ısıtılmış fırında pişirin."),
        ("Zeytinyağlı Yaprak Sarma",
         "Asma yaprağı, pirinç, soğan, maydanoz, zeytinyağı, limon suyu, tuz, karabiber, nane",
         "Asma yapraklarını yıkayın ve sap kısımlarını kesin. Pirinci yıkayın ve süzün. İnce doğranmış soğanı, maydanozu ve baharatları ekleyin. Karıştırın. Her bir yaprağın içine biraz harç koyun ve sarın. Tencereye dizin. Üzerine zeytinyağı, limon suyu ve su ekleyin. Pişirin."),
        ("Fırında Kabak", "Kabak, sıvıyağ, tuz, kekik",
         "Kabakları yıkayın ve dilimleyin. Fırın tepsisine dizin. Üzerine sıvıyağ, tuz ve kekik serpin. Önceden ısıtılmış fırında kızarana kadar pişirin."),
        ("Çılbır", "Yumurta, yoğurt, sıvıyağ, sirke, tuz, pul biber",
         "Tavada sıvıyağı kızdırın. Yumurtaları tek tek kırın ve kızgın yağda hafifçe kızartın. Bir kasede yoğurt, tuz ve ezilmiş sarımsağı karıştırın. Yumurtaları servis tabağına alın. Üzerine yoğurtlu karışımı gezdirin. Tavada kalan sıvıyağa sirke ve pul biber ekleyin. Bu sosu da yumurtaların üzerine gezdirin."),
        ("Çorba", "Su, et suyu, sebzeler, tuz, karabiber, nane",
         "Et suyu ve suyu bir tencereye alın. Doğranmış sebzeleri ekleyin. Tuz ve baharatları ekleyin. Pişirin ve sıcak servis yapın.")
    ]

    # Örnek malzemeler
    malzemeler = [
        ("Kırmızı mercimek", 200, "Mercimek Çorbası"),
        ("Soğan", 1, "Mercimek Çorbası"),
        ("Havuç", 1, "Mercimek Çorbası"),
        ("Patates", 2, "Mercimek Çorbası"),

    ]

    # Tablolara veri ekleyin
    cursor.executemany("INSERT INTO Tarifler (tarif_adi, malzemeler, tarif) VALUES (?, ?, ?)", Tarifler)
    cursor.executemany("INSERT INTO Malzeme (malzeme_adi, malzeme_miktari, tarif_adi) VALUES (?, ?, ?)", malzemeler)

    # Değişiklikleri kaydedin ve bağlantıyı kapatın
    connection.commit()
    connection.close()

    # Ana uygulamayı başlat
    root = tk.Tk()
    app = UserLoginApp(root)
    root.mainloop()
