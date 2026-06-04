import streamlit as st
import heapq
import random

st.set_page_config(page_title="Stasiun VY Junction", page_icon="🚆", layout="wide")

# ==========================================
# LOGIN CLASS
# ==========================================
class Login:
    def __init__(self, nama, no_hp, email):
        self.nama = nama
        self.no_hp = no_hp
        self.email = email


# ==========================================
# GRAPH
# ==========================================
class GraphKereta:
    def __init__(self):
        self.graf = {
            "Jakarta": [("Bandung", 150), ("Bekasi", 35), ("Bogor", 60), ("Cirebon", 220)],
            "Bandung": [("Jakarta", 150), ("Tasikmalaya", 110), ("Yogyakarta", 390)],
            "Bekasi": [("Jakarta", 35), ("Karawang", 45)],
            "Bogor": [("Jakarta", 60), ("Sukabumi", 90)],
            "Sukabumi": [("Bogor", 90), ("Bandung", 100)],
            "Tasikmalaya": [("Bandung", 110), ("Banjar", 80)],
            "Banjar": [("Tasikmalaya", 80), ("Yogyakarta", 200)],
            "Karawang": [("Bekasi", 45), ("Cirebon", 140)],
            "Cirebon": [("Karawang", 140), ("Semarang", 250)],
            "Semarang": [("Cirebon", 250), ("Surabaya", 350)],
            "Yogyakarta": [("Bandung", 390), ("Surabaya", 320)],
            "Surabaya": [("Semarang", 350), ("Yogyakarta", 320)]
        }

    def jalur_pendek(self, mulai, tujuan):
        jarak = {i: float("inf") for i in self.graf}
        jalur = {i: None for i in self.graf}

        jarak[mulai] = 0
        pq = [(0, mulai)]

        while pq:
            dist, node = heapq.heappop(pq)

            if node == tujuan:
                break

            for nxt, w in self.graf[node]:
                new = dist + w
                if new < jarak[nxt]:
                    jarak[nxt] = new
                    jalur[nxt] = node
                    heapq.heappush(pq, (new, nxt))

        rute = []
        cur = tujuan
        while cur:
            rute.insert(0, cur)
            cur = jalur[cur]

        return rute, jarak[tujuan]


# ==========================================
# SESSION
# ==========================================
if "login" not in st.session_state:
    st.session_state.login = False

if "menu" not in st.session_state:
    st.session_state.menu = "rute"

if "show_logout" not in st.session_state:
    st.session_state.show_logout = False

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

kereta = GraphKereta()

# ==========================================
# LOGIN
# ==========================================
if not st.session_state.login:

    st.title("🚆 LOGIN STASIUN VY JUNCTION")

    nama = st.text_input("👤 Nama")
    no_hp = st.text_input("📱 No HP")
    email = st.text_input("📧 Email")

    if st.button("Login 🚪"):
        if nama and no_hp and email:
            st.session_state.login = True
            st.session_state.nama = nama
            st.rerun()
        else:
            st.error("Isi semua data!")

# ==========================================
# APP
# ==========================================
else:

    st.title("🚆 VY JUNCTION")
    st.success(f"Halo {st.session_state.nama}")

    # ================= SIDEBAR =================
    st.sidebar.title("MENU 🚆")

    if st.sidebar.button("🗺️ Rute"):
        st.session_state.menu = "rute"

    if st.sidebar.button("🚄 Cepat"):
        st.session_state.menu = "cepat"

    if st.sidebar.button("🎫 Tiket"):
        st.session_state.menu = "tiket"

    if st.sidebar.button("🌐 Graph"):
        st.session_state.menu = "graph"

    if st.sidebar.button("🚉 Stasiun"):
        st.session_state.menu = "stasiun"

    if st.sidebar.button("🔗 Koneksi"):
        st.session_state.menu = "koneksi"

    if st.sidebar.button("📜 Riwayat"):
        st.session_state.menu = "riwayat"

    if st.sidebar.button("🚪 Logout"):
        st.session_state.show_logout = True


    # ================= LOGOUT POPUP =================
    if st.session_state.show_logout:

        with st.container():
            st.warning("Mau keluar dari sistem?")

            c1, c2 = st.columns(2)

            if c1.button("✔ Ya keluar"):
                st.session_state.login = False
                st.session_state.show_logout = False
                st.rerun()

            if c2.button("❌ Tidak"):
                st.session_state.show_logout = False
                st.rerun()


    # ================= MENU CONTENT =================
    if st.session_state.menu == "rute":

        st.subheader("🗺️ Rute")

        a = st.selectbox("Awal", list(kereta.graf.keys()))
        b = st.selectbox("Tujuan", list(kereta.graf.keys()))

        if st.button("Cari"):
            rute, jarak = kereta.jalur_pendek(a, b)
            st.info(" → ".join(rute) + f"\n{jarak} KM")


    elif st.session_state.menu == "cepat":

        st.subheader("🚄 Cepat")

        a = st.selectbox("Awal", list(kereta.graf.keys()), key="a")
        b = st.selectbox("Tujuan", list(kereta.graf.keys()), key="b")

        if st.button("Cari"):
            rute, jarak = kereta.jalur_pendek(a, b)
            st.success(f"{' → '.join(rute)} | {jarak} KM")


    elif st.session_state.menu == "tiket":

        st.subheader("🎫 Tiket")

        a = st.selectbox("Awal", list(kereta.graf.keys()), key="c")
        b = st.selectbox("Tujuan", list(kereta.graf.keys()), key="d")

        if st.button("Beli"):
            rute, jarak = kereta.jalur_pendek(a, b)
            total = jarak * 1000

            st.session_state.riwayat.append({
                "asal": a,
                "tujuan": b,
                "harga": total
            })

            st.success(f"Berhasil Rp{total}")


    elif st.session_state.menu == "graph":

        st.subheader("🌐 Graph")

        for i in kereta.graf:
            st.write(f"🚉 {i}")
            for j, k in kereta.graf[i]:
                st.write(f"➡️ {j} ({k})")


    elif st.session_state.menu == "stasiun":

        st.subheader("🚉 Stasiun")

        for i in kereta.graf:
            st.write("➡️", i)


    elif st.session_state.menu == "koneksi":

        st.subheader("🔗 Koneksi")

        x = st.selectbox("Pilih", list(kereta.graf.keys()))
        for j, k in kereta.graf[x]:
            st.write(f"➡️ {j} ({k})")


    elif st.session_state.menu == "riwayat":

        st.subheader("📜 Riwayat")

        for i in st.session_state.riwayat:
            st.write(i)
