import streamlit as st
import heapq
import random

# ==========================================
# CONFIG PAGE
# ==========================================
st.set_page_config(
    page_title="Stasiun VY Junction",
    page_icon="🚆",
    layout="wide"
)

# ==========================================
# CLASS LOGIN
# ==========================================
class Login:

    def __init__(self, nama, no_hp, email):

        self.nama = nama
        self.no_hp = no_hp
        self.email = email


# ==========================================
# CLASS E-WALLET
# ==========================================
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


# ==========================================
# CLASS GRAPH KERETA
# ==========================================
class GraphKereta:

    def __init__(self):

        self.graf = {

            "Jakarta": [
                ("Bandung", 150),
                ("Bekasi", 35),
                ("Bogor", 60)
            ],

            "Bandung": [
                ("Jakarta", 150),
                ("Tasikmalaya", 110),
                ("Yogyakarta", 390)
            ],

            "Bekasi": [
                ("Jakarta", 35),
                ("Karawang", 45)
            ],

            "Bogor": [
                ("Jakarta", 60),
                ("Sukabumi", 90)
            ],

            "Sukabumi": [
                ("Bogor", 90),
                ("Bandung", 100)
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
                ("Karawang", 140),
                ("Semarang", 250)
            ],

            "Semarang": [
                ("Cirebon", 250),
                ("Surabaya", 350)
            ],

            "Yogyakarta": [
                ("Bandung", 390),
                ("Surabaya", 320)
            ],

            "Surabaya": [
                ("Semarang", 350),
                ("Yogyakarta", 320)
            ]
        }

    # ==========================================
    # DIJKSTRA
    # ==========================================
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

    # ==========================================
    # TAMPIL GRAPH
    # ==========================================
    def tampil_graph(self):

        hasil = ""

        for stasiun in self.graf:

            hasil += f"\n🚉 {stasiun}\n"

            for tujuan, jarak in self.graf[stasiun]:

                hasil += f"   ➡️ {tujuan} ({jarak} KM)\n"

        return hasil


# ==========================================
# SESSION STATE
# ==========================================
if "login" not in st.session_state:

    st.session_state.login = False

if "wallet" not in st.session_state:

    st.session_state.wallet = EWallet()

if "riwayat" not in st.session_state:

    st.session_state.riwayat = []

# ==========================================
# OBJECT GRAPH
# ==========================================
kereta = GraphKereta()

# ==========================================
# LOGIN PAGE
# ==========================================
if st.session_state.login == False:

    st.title("🚆 LOGIN STASIUN VY JUNCTION")

    nama = st.text_input("Nama")
    no_hp = st.text_input("No HP")
    email = st.text_input("Email")

    if st.button("Login", type="primary"):

        if nama and no_hp and email:

            user = Login(nama, no_hp, email)

            st.session_state.login = True
            st.session_state.nama = user.nama

            st.rerun()

        else:

            st.error("❌ Semua data harus diisi!")

# ==========================================
# HALAMAN UTAMA
# ==========================================
else:

    st.title("🚆 STASIUN VY JUNCTION")

    st.success(f"Selamat Datang, {st.session_state.nama}")

    # ==========================================
    # MENU TAB
    # ==========================================
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([

        "📍 Lihat Rute",
        "🎫 Beli Tiket",
        "💰 E-Wallet",
        "🚉 Daftar Stasiun",
        "🔗 Koneksi",
        "📜 Riwayat",
        "🚪 Logout"
    ])

    # ==========================================
    # TAB LIHAT RUTE
    # ==========================================
    with tab1:

        st.subheader("Cek Rute Kereta")

        col1, col2 = st.columns(2)

        with col1:

            mulai = st.selectbox(
                "Stasiun Awal",
                list(kereta.graf.keys())
            )

        with col2:

            tujuan = st.selectbox(
                "Stasiun Tujuan",
                list(kereta.graf.keys())
            )

        if st.button("Lihat Rute"):

            rute, total_jarak = kereta.dijkstra(
                mulai,
                tujuan
            )

            st.success("Rute Ditemukan!")

            st.info(f"""
🚉 Dari : {mulai}

🚉 Ke : {tujuan}

🚆 Jalur : {' → '.join(rute)}

📍 Total Jarak : {total_jarak} KM
""")

    # ==========================================
    # TAB BELI TIKET
    # ==========================================
    with tab2:

        st.subheader("Pembelian Tiket")

        col1, col2 = st.columns(2)

        with col1:

            mulai2 = st.selectbox(
                "Stasiun Awal ",
                list(kereta.graf.keys())
            )

        with col2:

            tujuan2 = st.selectbox(
                "Stasiun Tujuan ",
                list(kereta.graf.keys())
            )

        kelas = st.selectbox(
            "Pilih Kelas",
            ["Ekonomi", "Bisnis", "Eksekutif"]
        )

        jumlah = st.number_input(
            "Jumlah Tiket",
            min_value=1,
            value=1
        )

        jadwal = st.selectbox(
            "Pilih Jadwal",
            ["08:00 WIB", "12:00 WIB", "18:00 WIB"]
        )

        kursi = st.text_input(
            "Nomor Kursi",
            value="A1"
        )

        if st.button("Pesan Tiket", type="primary"):

            rute, total_jarak = kereta.dijkstra(
                mulai2,
                tujuan2
            )

            if kelas == "Ekonomi":

                harga = total_jarak * 1000

            elif kelas == "Bisnis":

                harga = total_jarak * 1500

            else:

                harga = total_jarak * 2000

            total = harga * jumlah

            if st.session_state.wallet.bayar(total):

                kode = random.randint(10000, 99999)

                st.session_state.riwayat.append({

                    "nama": st.session_state.nama,
                    "asal": mulai2,
                    "tujuan": tujuan2,
                    "kelas": kelas,
                    "harga": total
                })

                st.success("✅ Pembayaran Berhasil!")

                st.code(f"""
══════════════════════════════
       ACCESS BY TRAIN 🚆
══════════════════════════════

Kode Tiket : {kode}
Nama       : {st.session_state.nama}
Dari       : {mulai2}
Tujuan     : {tujuan2}
Kelas      : {kelas}
Kursi      : {kursi}
Jadwal     : {jadwal}
Total      : Rp{total}

══════════════════════════════
""")

            else:

                st.error("❌ Saldo Tidak Cukup!")

                st.warning(f"""
💵 Total Bayar : Rp{total}

💰 Saldo Anda : Rp{st.session_state.wallet.saldo}
""")

    # ==========================================
    # TAB E-WALLET
    # ==========================================
    with tab3:

        st.subheader("E-Wallet")

        st.info(
            f"💰 Saldo Anda : Rp{st.session_state.wallet.saldo}"
        )

        topup = st.number_input(
            "Masukkan Jumlah Top Up",
            min_value=0
        )

        if st.button("Top Up"):

            st.session_state.wallet.topup(topup)

            st.success("✅ Top Up Berhasil!")

    # ==========================================
    # TAB DAFTAR STASIUN
    # ==========================================
    with tab4:

        st.subheader("Daftar Stasiun")

        for stasiun in kereta.graf:

            st.write(f"🚉 {stasiun}")

    # ==========================================
    # TAB KONEKSI
    # ==========================================
    with tab5:

        st.subheader("Koneksi Stasiun")

        pilih = st.selectbox(
            "Pilih Stasiun",
            list(kereta.graf.keys())
        )

        st.write(f"### 🚉 Koneksi Dari {pilih}")

        for tujuan, jarak in kereta.graf[pilih]:

            st.write(f"➡️ {tujuan} ({jarak} KM)")

    # ==========================================
    # TAB RIWAYAT
    # ==========================================
    with tab6:

        st.subheader("Riwayat Pembelian")

        if len(st.session_state.riwayat) == 0:

            st.warning("Belum ada pembelian tiket.")

        else:

            for data in st.session_state.riwayat:

                st.code(f"""
Nama   : {data['nama']}
Dari   : {data['asal']}
Tujuan : {data['tujuan']}
Kelas  : {data['kelas']}
Harga  : Rp{data['harga']}
""")

    # ==========================================
    # TAB LOGOUT
    # ==========================================
    with tab7:

        st.subheader("Logout Sistem")

        if st.button("Logout", type="primary"):

            st.session_state.login = False
            st.rerun()

