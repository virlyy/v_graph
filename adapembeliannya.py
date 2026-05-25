import streamlit as st

# ======================================
# CLASS LOGIN
# ======================================
class Login:

    def __init__(self, nama, no_hp, email):

        self.nama = nama
        self.no_hp = no_hp
        self.email = email

    def welcome(self):

        print("\n==========================================")
        print(f" Selamat Datang di Access By Train 🚆")
        print(f" User : {self.nama}")
        print("==========================================")


# ======================================
# CLASS E-WALLET
# ======================================
class EWallet:

    def __init__(self):

        self.saldo = 500000

    def cek_saldo(self):

        print("\n========== E-WALLET ==========")

        print(f"💰 Saldo Anda : Rp{self.saldo}")

    def topup(self):

        jumlah = int(input("Masukkan Jumlah Top Up : Rp"))

        self.saldo += jumlah

        print("\n✅ Top Up Berhasil!")

        print(f"💰 Saldo Sekarang : Rp{self.saldo}")

    def bayar(self, total):

        if self.saldo >= total:

            self.saldo -= total

            return True

        else:

            return False


# ======================================
# CLASS GRAPH KERETA
# ======================================
class GraphKereta:

    def __init__(self):

        self.riwayat = []

        self.graf = {

            "Jakarta": [
                ("Bandung", 150),
                ("Bekasi", 35),
                ("Bogor", 60),
                ("Cirebon", 220)
            ],

            "Bekasi": [
                ("Jakarta", 35),
                ("Karawang", 45),
                ("Depok", 30)
            ],

            "Depok": [
                ("Bekasi", 30),
                ("Bogor", 40)
            ],

            "Bogor": [
                ("Jakarta", 60),
                ("Sukabumi", 90),
                ("Depok", 40)
            ],

            "Sukabumi": [
                ("Bogor", 90),
                ("Bandung", 100)
            ],

            "Bandung": [
                ("Jakarta", 150),
                ("Tasikmalaya", 110),
                ("Garut", 70),
                ("Cimahi", 20),
                ("Yogyakarta", 390)
            ],

            "Cimahi": [
                ("Bandung", 20)
            ],

            "Garut": [
                ("Bandung", 70),
                ("Tasikmalaya", 60)
            ],

            "Tasikmalaya": [
                ("Bandung", 110),
                ("Banjar", 80)
            ],

            "Banjar": [
                ("Tasikmalaya", 80),
                ("Yogyakarta", 200)
            ],

            "Karawang": [
                ("Bekasi", 45),
                ("Cirebon", 140)
            ],

            "Cirebon": [
                ("Jakarta", 220),
                ("Karawang", 140),
                ("Purwokerto", 170),
                ("Semarang", 250)
            ],

            "Purwokerto": [
                ("Cirebon", 170),
                ("Yogyakarta", 180)
            ],

            "Semarang": [
                ("Cirebon", 250),
                ("Solo", 110),
                ("Surabaya", 350)
            ],

            "Solo": [
                ("Semarang", 110),
                ("Yogyakarta", 65),
                ("Madiun", 100)
            ],

            "Madiun": [
                ("Solo", 100),
                ("Kediri", 120)
            ],

            "Kediri": [
                ("Madiun", 120),
                ("Malang", 130)
            ],

            "Yogyakarta": [
                ("Bandung", 390),
                ("Solo", 65),
                ("Purwokerto", 180),
                ("Banjar", 200),
                ("Surabaya", 320)
            ],

            "Surabaya": [
                ("Semarang", 350),
                ("Yogyakarta", 320),
                ("Malang", 95),
                ("Jember", 200)
            ],

            "Malang": [
                ("Surabaya", 95),
                ("Kediri", 130)
            ],

            "Jember": [
                ("Surabaya", 200),
                ("Banyuwangi", 100)
            ],

            "Banyuwangi": [
                ("Jember", 100)
            ]
        }

    # ======================================
    # ALGORITMA DIJKSTRA
    # ======================================
    def dijkstra(self, mulai, tujuan):

        jarak = {

            stasiun: float('inf')

            for stasiun in self.graf
        }

        jalur = {

            stasiun: None

            for stasiun in self.graf
        }

        jarak[mulai] = 0

        pq = [(0, mulai)]

        while pq:

            jarak_sekarang, stasiun_sekarang = heapq.heappop(pq)

            if stasiun_sekarang == tujuan:

                break

            for tetangga, bobot in self.graf[stasiun_sekarang]:

                jarak_baru = jarak_sekarang + bobot

                if jarak_baru < jarak[tetangga]:

                    jarak[tetangga] = jarak_baru

                    jalur[tetangga] = stasiun_sekarang

                    heapq.heappush(
                        pq,
                        (jarak_baru, tetangga)
                    )

        rute = []

        step = tujuan

        while step is not None:

            rute.insert(0, step)

            step = jalur[step]

        return rute, jarak[tujuan]

    # ======================================
    # TAMPIL STASIUN
    # ======================================
    def tampil_stasiun(self):

        print("\n========== DAFTAR STASIUN ==========")

        for stasiun in self.graf:

            print(f"🚉 {stasiun}")

    # ======================================
    # TAMPIL GRAPH
    # ======================================
    def tampil_graph(self):

        print("\n========== GRAPH RUTE ==========")

        for stasiun in self.graf:

            print(f"\n🚉 {stasiun}")

            for tujuan, jarak in self.graf[stasiun]:

                print(f"   ➡️ {tujuan} ({jarak} KM)")

    # ======================================
    # LIHAT RUTE
    # ======================================
    def lihat_rute(self):

        print("\n========== LIHAT RUTE ==========")

        mulai = input("Masukkan Stasiun Awal   : ").title()

        tujuan = input("Masukkan Stasiun Tujuan: ").title()

        if mulai not in self.graf or tujuan not in self.graf:

            print("\n❌ Stasiun tidak ditemukan!")

            return

        rute, total_jarak = self.dijkstra(mulai, tujuan)

        print("\n========== HASIL RUTE ==========")

        print(f"🚉 Dari : {mulai}")

        print(f"🚉 Ke    : {tujuan}")

        print(f"\n🚆 Jalur : {' -> '.join(rute)}")

        print(f"📍 Total Jarak : {total_jarak} KM")

    # ======================================
    # BELI TIKET
    # ======================================
    def beli_tiket(self, wallet, user):

        print("\n========== PEMBELIAN TIKET ==========")

        mulai = input("Masukkan Stasiun Awal   : ").title()

        tujuan = input("Masukkan Stasiun Tujuan: ").title()

        if mulai not in self.graf or tujuan not in self.graf:

            print("\n❌ Stasiun tidak ditemukan!")

            return

        rute, total_jarak = self.dijkstra(mulai, tujuan)

        print("\n========== PILIH KELAS ==========")

        print("1. Ekonomi")
        print("2. Bisnis")
        print("3. Eksekutif")

        kelas = input("Pilih Kelas : ")

        if kelas == "1":

            nama_kelas = "Ekonomi"

            harga = total_jarak * 1000

        elif kelas == "2":

            nama_kelas = "Bisnis"

            harga = total_jarak * 1500

        elif kelas == "3":

            nama_kelas = "Eksekutif"

            harga = total_jarak * 2000

        else:

            print("\n❌ Kelas tidak tersedia!")

            return

        jumlah = int(input("Jumlah Tiket : "))

        total = harga * jumlah

        jadwal = [
            "08:00 WIB",
            "12:00 WIB",
            "18:00 WIB"
        ]

        print("\n========== PILIH JADWAL ==========")

        for i in range(len(jadwal)):

            print(f"{i+1}. {jadwal[i]}")

        pilih_jadwal = int(input("Pilih Jadwal : "))

        jadwal_terpilih = jadwal[pilih_jadwal - 1]

        kursi = input("Pilih Kursi (Contoh A1) : ").upper()

        kode_tiket = random.randint(10000, 99999)

        print("\n========== DETAIL PEMBELIAN ==========")

        print(f"👤 Nama          : {user.nama}")

        print(f"🚉 Dari          : {mulai}")

        print(f"🚉 Ke            : {tujuan}")

        print(f"🚆 Jalur         : {' -> '.join(rute)}")

        print(f"🎫 Kelas         : {nama_kelas}")

        print(f"🪑 Kursi         : {kursi}")

        print(f"🕒 Jadwal        : {jadwal_terpilih}")

        print(f"🎟️ Jumlah Tiket  : {jumlah}")

        print(f"📍 Total Jarak   : {total_jarak} KM")

        print(f"💵 Total Bayar   : Rp{total}")

        print(f"💰 Saldo Anda    : Rp{wallet.saldo}")

        konfirmasi = input("\nLanjut Pembayaran? (y/n) : ")

        if konfirmasi.lower() == "y":

            if wallet.bayar(total):

                self.riwayat.append({

                    "nama": user.nama,
                    "asal": mulai,
                    "tujuan": tujuan,
                    "kelas": nama_kelas,
                    "harga": total
                })

                print("\n✅ PEMBAYARAN BERHASIL!")

                print(f"💰 Sisa Saldo : Rp{wallet.saldo}")

                print("""
╔══════════════════════════════════════╗
║         ACCESS BY TRAIN 🚆          ║
╠══════════════════════════════════════╣
""")

                print(f"║ Kode Tiket : {kode_tiket}")

                print(f"║ Nama       : {user.nama}")

                print(f"║ Dari       : {mulai}")

                print(f"║ Tujuan     : {tujuan}")

                print(f"║ Kelas      : {nama_kelas}")

                print(f"║ Kursi      : {kursi}")

                print(f"║ Jadwal     : {jadwal_terpilih}")

                print(f"║ Total      : Rp{total}")

                print("╚══════════════════════════════════════╝")

            else:

                print("\n❌ Saldo tidak cukup!")

        else:

            print("\n❌ Pembayaran dibatalkan!")

    # ======================================
    # RIWAYAT PEMBELIAN
    # ======================================
    def riwayat_tiket(self):

        print("\n========== RIWAYAT TIKET ==========")

        if len(self.riwayat) == 0:

            print("Belum ada pembelian tiket.")

        else:

            for data in self.riwayat:

                print(f"""
👤 Nama    : {data['nama']}
🚉 Dari    : {data['asal']}
🚉 Ke      : {data['tujuan']}
🎫 Kelas   : {data['kelas']}
💵 Harga   : Rp{data['harga']}
====================================
""")


# ======================================
# PROGRAM UTAMA
# ======================================
def main():

    print("========== LOGIN ==========")

    nama = input("Nama  : ")

    no_hp = input("No HP : ")

    email = input("Email : ")

    user = Login(nama, no_hp, email)

    user.welcome()

    sistem = GraphKereta()

    wallet = EWallet()

    while True:

        print("\n========== MENU ACCESS BY TRAIN ==========")

        print("1. Lihat Rute")
        print("2. Beli Tiket")
        print("3. Cek Saldo")
        print("4. Top Up Saldo")
        print("5. Tampilkan Graph")
        print("6. Daftar Stasiun")
        print("7. Riwayat Tiket")
        print("8. Logout")

        menu = input("Pilih Menu : ")

        if menu == "1":

            sistem.lihat_rute()

        elif menu == "2":

            sistem.beli_tiket(wallet, user)

        elif menu == "3":

            wallet.cek_saldo()

        elif menu == "4":

            wallet.topup()

        elif menu == "5":

            sistem.tampil_graph()

        elif menu == "6":

            sistem.tampil_stasiun()

        elif menu == "7":

            sistem.riwayat_tiket()

        elif menu == "8":

            print("\nTerima kasih telah menggunakan Access By Train 🚆")

            break

        else:

            print("\n❌ Menu tidak tersedia!")


# ======================================
# MENJALANKAN PROGRAM
# ======================================
main()

# ======================================
# MENJALANKAN PROGRAM
# ======================================
main()
