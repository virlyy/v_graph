import streamlit as st
import heapq
import random

st.set_page_config(
    page_title="Stasiun VY Junction",
    page_icon="🚆",
    layout="wide"
)

# ======================================
# CLASS LOGIN
# ======================================
class Login:

    def __init__(self, nama, no_hp, email):

        self.nama = nama
        self.no_hp = no_hp
        self.email = email


# ======================================
# CLASS E-WALLET
# ======================================
class EWallet:

    def __init__(self):

        self.saldo = 500000

    def topup(self, jumlah):

        self.saldo += jumlah

    def bayar(self, total):

        if self.saldo >= total:

            self.saldo -= total

            return True

        return False


# ======================================
# CLASS GRAPH KERETA
# ======================================
class GraphKereta:

    def __init__(self):

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
# SESSION STATE
# ======================================
if "wallet" not in st.session_state:
    st.session_state.wallet = EWallet()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "login" not in st.session_state:
    st.session_state.login = False

sistem = GraphKereta()

# ======================================
# LOGIN PAGE
# ======================================
if not st.session_state.login:

    st.title("🚆 Access By Train")

    st.subheader("Login Pengguna")

    nama = st.text_input("Nama")
    no_hp = st.text_input("No HP")
    email = st.text_input("Email")

    if st.button("Login"):

        if nama and no_hp and email:

            st.session_state.user = Login(
                nama,
                no_hp,
                email
            )

            st.session_state.login = True

            st.rerun()

        else:

            st.error("Semua data wajib diisi!")

# ======================================
# MAIN APP
# ======================================
else:

    user = st.session_state.user
    wallet = st.session_state.wallet

    st.sidebar.title("🚆 MENU")

    menu = st.sidebar.selectbox(
        "Pilih Menu",
        [
            "Beranda",
            "Lihat Rute",
            "Beli Tiket",
            "Cek Saldo",
            "Top Up Saldo",
            "Daftar Stasiun",
            "Graph Kereta",
            "Riwayat Tiket",
            "Logout"
        ]
    )

    st.title("🚆 Access By Train")

    st.success(f"Selamat Datang, {user.nama}")

    # ======================================
    # BERANDA
    # ======================================
    if menu == "Beranda":

        st.subheader("Informasi Pengguna")

        st.write(f"👤 Nama : {user.nama}")
        st.write(f"📱 No HP : {user.no_hp}")
        st.write(f"📧 Email : {user.email}")
        st.write(f"💰 Saldo : Rp{wallet.saldo}")

    # ======================================
    # LIHAT RUTE
    # ======================================
    elif menu == "Lihat Rute":

        st.subheader("🚉 Lihat Rute Kereta")

        stasiun = list(sistem.graf.keys())

        mulai = st.selectbox("Stasiun Awal", stasiun)

        tujuan = st.selectbox("Stasiun Tujuan", stasiun)

        if st.button("Cari Rute"):

            rute, total_jarak = sistem.dijkstra(
                mulai,
                tujuan
            )

            st.success("Rute Ditemukan!")

            st.write(f"🚆 Jalur : {' → '.join(rute)}")
            st.write(f"📍 Total Jarak : {total_jarak} KM")

    # ======================================
    # BELI TIKET
    # ======================================
    elif menu == "Beli Tiket":

        st.subheader("🎫 Pembelian Tiket")

        stasiun = list(sistem.graf.keys())

        mulai = st.selectbox("Stasiun Awal", stasiun)

        tujuan = st.selectbox("Stasiun Tujuan", stasiun)

        kelas = st.selectbox(
            "Pilih Kelas",
            [
                "Ekonomi",
                "Bisnis",
                "Eksekutif"
            ]
        )

        jumlah = st.number_input(
            "Jumlah Tiket",
            min_value=1,
            step=1
        )

        jadwal = st.selectbox(
            "Pilih Jadwal",
            [
                "08:00 WIB",
                "12:00 WIB",
                "18:00 WIB"
            ]
        )

        kursi = st.text_input("Pilih Kursi")

        if st.button("Pesan Tiket"):

            rute, total_jarak = sistem.dijkstra(
                mulai,
                tujuan
            )

            if kelas == "Ekonomi":
                harga = total_jarak * 1000

            elif kelas == "Bisnis":
                harga = total_jarak * 1500

            else:
                harga = total_jarak * 2000

            total = harga * jumlah

            st.write(f"🚆 Jalur : {' → '.join(rute)}")
            st.write(f"📍 Total Jarak : {total_jarak} KM")
            st.write(f"💵 Total Bayar : Rp{total}")

            if wallet.bayar(total):

                kode_tiket = random.randint(10000, 99999)

                data = {

                    "nama": user.nama,
                    "asal": mulai,
                    "tujuan": tujuan,
                    "kelas": kelas,
                    "harga": total
                }

                st.session_state.riwayat.append(data)

                st.success("✅ Pembayaran Berhasil!")

                st.info(f"Sisa Saldo : Rp{wallet.saldo}")

                st.code(f"""
==================================
        ACCESS BY TRAIN
==================================
Kode Tiket : {kode_tiket}
Nama       : {user.nama}
Dari       : {mulai}
Tujuan     : {tujuan}
Kelas      : {kelas}
Kursi      : {kursi}
Jadwal     : {jadwal}
Total      : Rp{total}
==================================
                """)

            else:

                st.error("❌ Saldo Tidak Cukup!")

    # ======================================
    # CEK SALDO
    # ======================================
    elif menu == "Cek Saldo":

        st.subheader("💰 Saldo E-Wallet")

        st.success(f"Saldo Anda : Rp{wallet.saldo}")

    # ======================================
    # TOP UP
    # ======================================
    elif menu == "Top Up Saldo":

        st.subheader("💳 Top Up Saldo")

        jumlah = st.number_input(
            "Masukkan Jumlah Top Up",
            min_value=1000,
            step=1000
        )

        if st.button("Top Up"):

            wallet.topup(jumlah)

            st.success("✅ Top Up Berhasil!")

            st.write(f"💰 Saldo Sekarang : Rp{wallet.saldo}")

    # ======================================
    # DAFTAR STASIUN
    # ======================================
    elif menu == "Daftar Stasiun":

        st.subheader("🚉 Daftar Stasiun")

        for stasiun in sistem.graf.keys():

            st.write(f"✅ {stasiun}")

    # ======================================
    # GRAPH KERETA
    # ======================================
    elif menu == "Graph Kereta":

        st.subheader("🗺️ Graph Rute Kereta")

        for stasiun in sistem.graf:

            st.markdown(f"### 🚉 {stasiun}")

            for tujuan, jarak in sistem.graf[stasiun]:

                st.write(f"➡️ {tujuan} ({jarak} KM)")

    # ======================================
    # RIWAYAT TIKET
    # ======================================
    elif menu == "Riwayat Tiket":

        st.subheader("📜 Riwayat Tiket")

        if len(st.session_state.riwayat) == 0:

            st.warning("Belum ada pembelian tiket.")

        else:

            for data in st.session_state.riwayat:

                st.info(f"""
👤 Nama    : {data['nama']}
🚉 Dari    : {data['asal']}
🚉 Ke      : {data['tujuan']}
🎫 Kelas   : {data['kelas']}
💵 Harga   : Rp{data['harga']}
                """)

    # ======================================
    # LOGOUT
    # ======================================
    elif menu == "Logout":

        st.session_state.login = False

        st.rerun()
