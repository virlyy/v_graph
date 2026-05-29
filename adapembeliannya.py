import streamlit as st
import heapq
import random

# ======================================
# CONFIG PAGE
# ======================================
st.set_page_config(
    page_title="Access By Train 🚆",
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

        self.metode = {

            "DANA": 500000,
            "OVO": 300000,
            "GoPay": 450000,
            "ShopeePay": 350000,
            "Bank BCA": 1000000,
            "Bank Mandiri": 750000

        }

    def bayar(self, metode, total):

        if self.metode[metode] >= total:

            self.metode[metode] -= total

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
    # DIJKSTRA
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
# SESSION
# ======================================
if "login" not in st.session_state:

    st.session_state.login = False

if "wallet" not in st.session_state:

    st.session_state.wallet = EWallet()

if "sistem" not in st.session_state:

    st.session_state.sistem = GraphKereta()

if "menu" not in st.session_state:

    st.session_state.menu = "rute"


# ======================================
# LOGIN PAGE
# ======================================
if st.session_state.login == False:

    st.title("🚆 STASIUN VY JUNCTION")

    st.subheader("🔐 LOGIN USER")

    nama = st.text_input("👤 Nama")

    no_hp = st.text_input("📱 No HP")

    email = st.text_input("📧 Email")

    if st.button("🚪 Login", use_container_width=True):

        if nama and no_hp and email:

            st.session_state.user = Login(
                nama,
                no_hp,
                email
            )

            st.session_state.login = True

            st.rerun()

        else:

            st.warning("⚠️ Lengkapi Data Login!")


# ======================================
# MENU UTAMA
# ======================================
else:

    user = st.session_state.user

    wallet = st.session_state.wallet

    sistem = st.session_state.sistem

    st.title("🚆 ACCESS BY TRAIN")

    st.success(f"Selamat Datang {user.nama}")

    st.markdown("## 📌 MENU ACCESS BY TRAIN")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🗺️ Lihat Rute", use_container_width=True):

            st.session_state.menu = "rute"

        if st.button("🌐 Tampilkan Graph", use_container_width=True):

            st.session_state.menu = "graph"

        if st.button("📜 Riwayat Tiket", use_container_width=True):

            st.session_state.menu = "riwayat"

    with col2:

        if st.button("🎫 Beli Tiket", use_container_width=True):

            st.session_state.menu = "beli"

        if st.button("🚉 Daftar Stasiun", use_container_width=True):

            st.session_state.menu = "stasiun"

    with col3:

        if st.button("🔗 Koneksi Stasiun", use_container_width=True):

            st.session_state.menu = "koneksi"

        if st.button("🔒 Logout", use_container_width=True):

            st.session_state.login = False

            st.rerun()

    # ======================================
    # LIHAT RUTE
    # ======================================
    if st.session_state.menu == "rute":

        st.header("🗺️ LIHAT RUTE")

        mulai = st.selectbox(
            "🚉 Stasiun Awal",
            list(sistem.graf.keys())
        )

        tujuan = st.selectbox(
            "🚉 Stasiun Tujuan",
            list(sistem.graf.keys())
        )

        if st.button("🔍 Cari Rute"):

            rute, jarak = sistem.dijkstra(
                mulai,
                tujuan
            )

            st.success("Rute Ditemukan!")

            st.write(f"🚆 Jalur : {' ➜ '.join(rute)}")

            st.write(f"📍 Total Jarak : {jarak} KM")

    # ======================================
    # BELI TIKET
    # ======================================
    elif st.session_state.menu == "beli":

        st.header("🎫 PEMBELIAN TIKET")

        mulai = st.selectbox(
            "🚉 Dari",
            list(sistem.graf.keys())
        )

        tujuan = st.selectbox(
            "🚉 Ke",
            list(sistem.graf.keys())
        )

        kelas = st.selectbox(

            "🎫 Pilih Kelas",

            [

                "Ekonomi",
                "Bisnis",
                "Eksekutif"

            ]
        )

        jumlah = st.number_input(
            "🎟️ Jumlah Tiket",
            1,
            10,
            1
        )

        jadwal = st.selectbox(

            "🕒 Jadwal",

            [

                "08:00 WIB",
                "12:00 WIB",
                "18:00 WIB"

            ]
        )

        kursi = st.text_input(
            "🪑 Nomor Kursi",
            "A1"
        )

        metode = st.selectbox(

            "💳 Metode Pembayaran",

            list(wallet.metode.keys())
        )

        if st.button("💰 Pesan Tiket"):

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

            st.info(f"💵 Total Bayar : Rp{total}")

            st.info(f"💰 Saldo {metode} : Rp{wallet.metode[metode]}")

            if wallet.bayar(metode, total):

                kode = random.randint(
                    10000,
                    99999
                )

                sistem.riwayat.append({

                    "nama": user.nama,
                    "asal": mulai,
                    "tujuan": tujuan,
                    "kelas": kelas,
                    "harga": total

                })

                st.success("✅ Pembayaran Berhasil!")

                st.code(f"""
══════════════════════════
ACCESS BY TRAIN 🚆
══════════════════════════
Kode Tiket : {kode}
Nama       : {user.nama}
Dari       : {mulai}
Tujuan     : {tujuan}
Kelas      : {kelas}
Kursi      : {kursi}
Jadwal     : {jadwal}
Pembayaran : {metode}
Total      : Rp{total}
══════════════════════════
""")

            else:

                st.error("❌ Saldo Tidak Cukup!")

    # ======================================
    # GRAPH
    # ======================================
    elif st.session_state.menu == "graph":

        st.header("🌐 GRAPH RUTE")

        for stasiun in sistem.graf:

            st.subheader(f"🚉 {stasiun}")

            for tujuan, jarak in sistem.graf[stasiun]:

                st.write(f"➡️ {tujuan} ({jarak} KM)")

    # ======================================
    # STASIUN
    # ======================================
    elif st.session_state.menu == "stasiun":

        st.header("🚉 DAFTAR STASIUN")

        for stasiun in sistem.graf:

            st.write(f"🚆 {stasiun}")

    # ======================================
    # KONEKSI
    # ======================================
    elif st.session_state.menu == "koneksi":

        st.header("🔗 KONEKSI STASIUN")

        pilih = st.selectbox(
            "🚉 Pilih Stasiun",
            list(sistem.graf.keys())
        )

        if st.button("📍 Lihat Koneksi"):

            for tujuan, jarak in sistem.graf[pilih]:

                st.write(f"➡️ {tujuan} ({jarak} KM)")

    # ======================================
    # RIWAYAT
    # ======================================
    elif st.session_state.menu == "riwayat":

        st.header("📜 RIWAYAT TIKET")

        if len(sistem.riwayat) == 0:

            st.warning("Belum ada pembelian tiket.")

        else:

            for data in sistem.riwayat:

                st.info(f"""
👤 Nama : {data['nama']}
🚉 Dari : {data['asal']}
🚉 Ke : {data['tujuan']}
🎫 Kelas : {data['kelas']}
💵 Harga : Rp{data['harga']}
""")
