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
            "Jakarta": [("Bandung", 150), ("Bekasi", 35), ("Bogor", 60), ("Cirebon", 220)],
            "Bekasi": [("Jakarta", 35), ("Karawang", 45), ("Depok", 30)],
            "Depok": [("Bekasi", 30), ("Bogor", 40)],
            "Bogor": [("Jakarta", 60), ("Sukabumi", 90), ("Depok", 40)],
            "Sukabumi": [("Bogor", 90), ("Bandung", 100)],
            "Bandung": [("Jakarta", 150), ("Tasikmalaya", 110), ("Garut", 70), ("Cimahi", 20), ("Yogyakarta", 390)],
            "Cimahi": [("Bandung", 20)],
            "Garut": [("Bandung", 70), ("Tasikmalaya", 60)],
            "Tasikmalaya": [("Bandung", 110), ("Banjar", 80)],
            "Banjar": [("Tasikmalaya", 80), ("Yogyakarta", 200)],
            "Karawang": [("Bekasi", 45), ("Cirebon", 140)],
            "Cirebon": [("Jakarta", 220), ("Karawang", 140), ("Purwokerto", 170), ("Semarang", 250)],
            "Purwokerto": [("Cirebon", 170), ("Yogyakarta", 180)],
            "Semarang": [("Cirebon", 250), ("Solo", 110), ("Surabaya", 350)],
            "Solo": [("Semarang", 110), ("Yogyakarta", 65), ("Madiun", 100)],
            "Madiun": [("Solo", 100), ("Kediri", 120)],
            "Kediri": [("Madiun", 120), ("Malang", 130)],
            "Yogyakarta": [("Bandung", 390), ("Solo", 65), ("Purwokerto", 180), ("Banjar", 200), ("Surabaya", 320)],
            "Surabaya": [("Semarang", 350), ("Yogyakarta", 320), ("Malang", 95), ("Jember", 200)],
            "Malang": [("Surabaya", 95), ("Kediri", 130)],
            "Jember": [("Surabaya", 200), ("Banyuwangi", 100)],
            "Banyuwangi": [("Jember", 100)]
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

if "menu" not in st.session_state:
    st.session_state.menu = "rute"

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "show_logout" not in st.session_state:
    st.session_state.show_logout = False


kereta = GraphKereta()

# ==========================================
# LOGIN
# ==========================================
if not st.session_state.login:

    st.title("🚆 LOGIN STASIUN VY JUNCTION")

    nama = st.text_input("👤 Nama")
    no_hp = st.text_input("📱 No HP")
    email = st.text_input("📧 Email")

    if st.button("🚪 Login"):
        if nama and no_hp and email:
            st.session_state.login = True
            st.session_state.nama = nama
            st.rerun()
        else:
            st.error("❌ Semua data harus diisi!")

# ==========================================
# MAIN APP
# ==========================================
else:

    st.title("🚆 STASIUN VY JUNCTION")
    st.success(f"Selamat datang, {st.session_state.nama}")

    # ==========================================
    # SIDEBAR MENU (HIGHLIGHT ACTIVE)
    # ==========================================
    st.sidebar.title("🚆 MENU")

    def menu_button(label, key):
        if st.session_state.menu == key:
            st.sidebar.success(f"👉 {label}")
        if st.sidebar.button(label, use_container_width=True):
            st.session_state.menu = key

    menu_button("🗺️ Lihat Rute", "rute")
    menu_button("🚄 Jalur Tercepat", "cepat")
    menu_button("🎫 Beli Tiket", "beli")
    menu_button("🌐 Graph Rute", "graph")
    menu_button("🚉 Daftar Stasiun", "stasiun")
    menu_button("🔗 Koneksi", "koneksi")
    menu_button("📜 Riwayat", "riwayat")

    # LOGOUT BUTTON
    if st.sidebar.button("🔒 Logout", use_container_width=True):
        st.session_state.show_logout = True

    # ==========================================
    # LOGOUT CONFIRMATION
    # ==========================================
    if st.session_state.show_logout:

        st.warning("⚠️ Apakah Anda ingin keluar?")

        col1, col2 = st.columns(2)

        if col1.button("✔ Yes, Logout"):
            st.session_state.login = False
            st.session_state.show_logout = False
            st.rerun()

        if col2.button("❌ No"):
            st.session_state.show_logout = False
            st.rerun()

    # ==========================================
    # MENU CONTENT
    # ==========================================

    if st.session_state.menu == "rute":

        st.subheader("🗺️ Lihat Rute")

        a = st.selectbox("🚉 Awal", list(kereta.graf.keys()))
        b = st.selectbox("🚉 Tujuan", list(kereta.graf.keys()))

        if st.button("Cari"):
            rute, jarak = kereta.jalur_pendek(a, b)
            st.info(f"🚆 {' → '.join(rute)}\n📍 {jarak} KM")

    elif st.session_state.menu == "cepat":

        st.subheader("🚄 Jalur Tercepat")

        a = st.selectbox("🚉 Awal", list(kereta.graf.keys()), key="a")
        b = st.selectbox("🚉 Tujuan", list(kereta.graf.keys()), key="b")

        if st.button("Cari Cepat"):
            rute, jarak = kereta.jalur_pendek(a, b)
            st.success(f"🚆 {' → '.join(rute)} | {jarak} KM")

    elif st.session_state.menu == "beli":

        st.subheader("🎫 Beli Tiket")

        a = st.selectbox("🚉 Awal", list(kereta.graf.keys()), key="c")
        b = st.selectbox("🚉 Tujuan", list(kereta.graf.keys()), key="d")

        kelas = st.selectbox("🎫 Kelas", ["Ekonomi", "Bisnis", "Eksekutif"])

        if st.button("Beli"):
            rute, jarak = kereta.jalur_pendek(a, b)
            harga = jarak * (1000 if kelas=="Ekonomi" else 1500 if kelas=="Bisnis" else 2000)

            st.session_state.riwayat.append({
                "asal": a,
                "tujuan": b,
                "kelas": kelas,
                "harga": harga
            })

            st.success(f"🎟️ Berhasil! Total Rp{harga}")

    elif st.session_state.menu == "graph":

        st.subheader("🌐 Graph Rute")

        for i in kereta.graf:
            st.write(f"🚉 {i}")
            for j, k in kereta.graf[i]:
                st.write(f"➡️ {j} ({k} KM)")

    elif st.session_state.menu == "stasiun":

        st.subheader("🚉 Daftar Stasiun")

        for i in kereta.graf:
            st.write(f"➡️ {i}")

    elif st.session_state.menu == "koneksi":

        st.subheader("🔗 Koneksi")

        x = st.selectbox("Pilih", list(kereta.graf.keys()))
        for j, k in kereta.graf[x]:
            st.write(f"➡️ {j} ({k} KM)")

    elif st.session_state.menu == "riwayat":

        st.subheader("📜 Riwayat")

        for i in st.session_state.riwayat:
            st.write(i)
