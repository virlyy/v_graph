import streamlit as st
import heapq
import random

# ==========================================
# KONFIGURASI HALAMAN 
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
# CLASS GRAPH KERETA
# ==========================================
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

    def jalur_pendek(self, mulai, tujuan):

        jarak = {stasiun: float('inf') for stasiun in self.graf}
        jalur = {stasiun: None for stasiun in self.graf}

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

                    heapq.heappush(pq, (jarak_baru, tetangga))

        rute = []
        step = tujuan

        while step is not None:
            rute.insert(0, step)
            step = jalur[step]

        return rute, jarak[tujuan]


# ==========================================
# SESSION STATE
# ==========================================
if "login" not in st.session_state:
    st.session_state.login = False

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "menu" not in st.session_state:
    st.session_state.menu = "rute"

if "konfirmasi_logout" not in st.session_state:
    st.session_state.konfirmasi_logout = False

# ==========================================
# OBJECT
# ==========================================
kereta = GraphKereta()

# ==========================================
# LOGIN PAGE
# ==========================================
if st.session_state.login == False:

    st.title("🚆 LOGIN STASIUN VY JUNCTION")

    nama = st.text_input("👤 Nama")
    no_hp = st.text_input("📱 No HP")
    email = st.text_input("📧 Email")

    if st.button("🚪 Login"):

        if nama and no_hp and email:

            user = Login(nama, no_hp, email)

            st.session_state.login = True
            st.session_state.nama = user.nama

            st.rerun()

        else:
            st.error("❌ Semua data harus diisi!")

# ==========================================
# MAIN PAGE
# ==========================================
else:

    st.title("🚆 STASIUN VY JUNCTION")
    st.success(f"✅ Selamat Datang, {st.session_state.nama}")

    st.sidebar.title("🚆 MENU")

    if st.sidebar.button("🗺️ Lihat Rute", use_container_width=True):
        st.session_state.menu = "rute"

    if st.sidebar.button("🚄 Cari Jalur Tercepat", use_container_width=True):
        st.session_state.menu = "tercepat"

    if st.sidebar.button("🎫 Beli Tiket", use_container_width=True):
        st.session_state.menu = "beli"

    if st.sidebar.button("🌐 Jaringan Rute Kereta", use_container_width=True):
        st.session_state.menu = "graph"

    if st.sidebar.button("🚉 Daftar Stasiun", use_container_width=True):
        st.session_state.menu = "stasiun"

    if st.sidebar.button("🔗 Koneksi Stasiun", use_container_width=True):
        st.session_state.menu = "koneksi"

    if st.sidebar.button("📜 Riwayat Tiket", use_container_width=True):
        st.session_state.menu = "riwayat"

    # ===================== LOGOUT FIX =====================
    if st.sidebar.button("🔒 Logout", use_container_width=True):
        st.session_state.konfirmasi_logout = True

    if st.session_state.konfirmasi_logout:

        st.warning("⚠️ Apakah Anda yakin ingin keluar?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✔️ Ya"):
                st.session_state.login = False
                st.session_state.menu = "rute"
                st.session_state.konfirmasi_logout = False
                st.rerun()

        with col2:
            if st.button("❌ Tidak"):
                st.session_state.konfirmasi_logout = False
                st.rerun()

    # ==========================================
    # MENU RUTE
    # ==========================================
    if st.session_state.menu == "rute":

        st.subheader("🗺️ Lihat Rute Kereta")

        col1, col2 = st.columns(2)

        with col1:
            mulai = st.selectbox("🚉 Stasiun Awal", list(kereta.graf.keys()))

        with col2:
            tujuan = st.selectbox("🚉 Stasiun Tujuan", list(kereta.graf.keys()))

        if st.button("🔍 Cari Rute"):

            rute, total_jarak = kereta.jalur_pendek(mulai, tujuan)

            st.success("✅ Rute Ditemukan!")
            st.info(f"🚆 {' → '.join(rute)}\n📍 {total_jarak} KM")
