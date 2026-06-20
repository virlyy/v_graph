import streamlit as st
import heapq
import random

st.set_page_config(
    page_title="Stasiun VY Junction",
    page_icon="🚆",
    layout="wide"
)

# =========================
# CLASS LOGIN
# =========================
class Login:
    def __init__(self, nama, no_hp, email):
        self.nama = nama
        self.no_hp = no_hp
        self.email = email


# =========================
# GRAPH
# =========================
class GraphKereta:
    def __init__(self):
        self.graf = {
            "Jakarta": [("Bandung", 150), ("Bekasi", 35), ("Bogor", 60)],
            "Bandung": [("Jakarta", 150), ("Cimahi", 20), ("Yogyakarta", 390)],
            "Bekasi": [("Jakarta", 35), ("Karawang", 45)],
            "Bogor": [("Jakarta", 60)],
            "Cimahi": [("Bandung", 20)],
            "Karawang": [("Bekasi", 45)],
            "Yogyakarta": [("Bandung", 390)]
        }

    def dijkstra(self, start, end):
        dist = {n: float("inf") for n in self.graf}
        prev = {n: None for n in self.graf}

        dist[start] = 0
        pq = [(0, start)]

        while pq:
            d, node = heapq.heappop(pq)

            if node == end:
                break

            for nxt, w in self.graf[node]:
                nd = d + w
                if nd < dist[nxt]:
                    dist[nxt] = nd
                    prev[nxt] = node
                    heapq.heappush(pq, (nd, nxt))

        path = []
        cur = end
        while cur:
            path.insert(0, cur)
            cur = prev[cur]

        return path, dist[end]


kereta = GraphKereta()

# =========================
# SESSION STATE
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "menu" not in st.session_state:
    st.session_state.menu = "rute"
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "logout_confirm" not in st.session_state:
    st.session_state.logout_confirm = False


# =========================
# LOGIN PAGE (FIX)
# =========================
if not st.session_state.login:

    st.title("🚆 LOGIN VY JUNCTION")

    role = st.radio("Login sebagai:", ["User", "Admin"])

    nama = st.text_input("Nama")
    no_hp = st.text_input("No HP")
    email = st.text_input("Email")

    if st.button("Login"):

        if role == "Admin":

            if nama == "admin" and email == "admin@gmail.com":
                st.session_state.login = True
                st.session_state.role = "admin"
                st.session_state.nama = "Admin"
                st.rerun()

            else:
                st.error("Login admin salah!")

        else:

            if nama and no_hp and email:
                st.session_state.login = True
                st.session_state.role = "user"
                st.session_state.nama = nama
                st.rerun()

            else:
                st.error("Isi semua data!")

# =========================
# APP
# =========================
else:

    st.title("🚆 VY JUNCTION")
    st.success(f"Welcome {st.session_state.nama}")

    # =========================
    # LOGOUT CONFIRM
    # =========================
    if st.sidebar.button("Logout 🚪"):
        st.session_state.logout_confirm = True

    if st.session_state.logout_confirm:

        st.warning("Yakin mau logout?")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Ya"):
                st.session_state.login = False
                st.session_state.role = ""
                st.session_state.logout_confirm = False
                st.rerun()

        with c2:
            if st.button("Batal"):
                st.session_state.logout_confirm = False
                st.rerun()

    # =========================
    # MENU
    # =========================
    st.sidebar.title("MENU")

    if st.session_state.role == "user":

        if st.sidebar.button("Cari Rute"):
            st.session_state.menu = "rute"
        if st.sidebar.button("Beli Tiket"):
            st.session_state.menu = "beli"
        if st.sidebar.button("Riwayat"):
            st.session_state.menu = "riwayat"

    if st.session_state.role == "admin":

        if st.sidebar.button("Dashboard"):
            st.session_state.menu = "dashboard"
        if st.sidebar.button("Kelola Stasiun"):
            st.session_state.menu = "stasiun"
        if st.sidebar.button("Kelola Jalur"):
            st.session_state.menu = "jalur"
        if st.sidebar.button("Tiket"):
            st.session_state.menu = "tiket"
        if st.sidebar.button("Laporan"):
            st.session_state.menu = "laporan"


    # =========================
    # RUTE USER
    # =========================
    if st.session_state.menu == "rute":

        a = st.selectbox("Dari", list(kereta.graf.keys()))
        b = st.selectbox("Ke", list(kereta.graf.keys()))

        if st.button("Cari"):
            r, d = kereta.dijkstra(a, b)
            st.info(f"{' -> '.join(r)} | {d} KM")


    # =========================
    # BELI TIKET
    # =========================
    elif st.session_state.menu == "beli":

        a = st.selectbox("Dari", list(kereta.graf.keys()))
        b = st.selectbox("Ke", list(kereta.graf.keys()))

        if st.button("Bayar"):

            r, d = kereta.dijkstra(a, b)
            total = d * 1000

            st.session_state.riwayat.append({
                "nama": st.session_state.nama,
                "asal": a,
                "tujuan": b,
                "harga": total
            })

            st.success(f"Tiket berhasil Rp{total}")


    # =========================
    # RIWAYAT
    # =========================
    elif st.session_state.menu == "riwayat":

        for t in st.session_state.riwayat:
            st.write(t)


    # =========================
    # DASHBOARD ADMIN
    # =========================
    elif st.session_state.menu == "dashboard":

        st.metric("Total Tiket", len(st.session_state.riwayat))
        st.metric("Total Pendapatan", sum(t["harga"] for t in st.session_state.riwayat))


    # =========================
    # KELOLA STASIUN
    # =========================
    elif st.session_state.menu == "stasiun":

        nama = st.text_input("Stasiun baru")

        if st.button("Tambah"):
            if nama:
                kereta.graf[nama] = []
                st.success("Stasiun ditambah")

        st.write(list(kereta.graf.keys()))


    # =========================
    # KELOLA JALUR
    # =========================
    elif st.session_state.menu == "jalur":

        a = st.selectbox("Dari", list(kereta.graf.keys()))
        b = st.selectbox("Ke", list(kereta.graf.keys()))
        j = st.number_input("Jarak", 1)

        if st.button("Tambah"):
            kereta.graf[a].append((b, j))
            kereta.graf[b].append((a, j))
            st.success("Jalur ditambah")


    # =========================
    # TIKET ADMIN
    # =========================
    elif st.session_state.menu == "tiket":

        for t in st.session_state.riwayat:
            st.write(t)


    # =========================
    # LAPORAN
    # =========================
    elif st.session_state.menu == "laporan":

        st.write("Total:", sum(t["harga"] for t in st.session_state.riwayat))
