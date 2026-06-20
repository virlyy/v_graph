import streamlit as st
import heapq
import random

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="Stasiun VY Junction",
    page_icon="🚆",
    layout="wide"
)

# ==========================================
# LOGIN CLASS
# ==========================================
class Login:
    def __init__(self, nama, no_hp, email):
        self.nama = nama
        self.no_hp = no_hp
        self.email = email


# ==========================================
# GRAPH KERETA
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

# ==========================================
# SESSION STATE
# ==========================================
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


# ==========================================
# LOGIN PAGE
# ==========================================
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


# ==========================================
# APP
# ==========================================
else:

    st.title("🚆 VY JUNCTION")
    st.success(f"Welcome {st.session_state.nama}")

    # ==========================================
    # LOGOUT
    # ==========================================
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


    # ==========================================
    # MENU USER
    # ==========================================
    st.sidebar.title("MENU")

    if st.session_state.role == "user":
        if st.sidebar.button("🗺️ Rute"):
            st.session_state.menu = "rute"
        if st.sidebar.button("⚡ Tercepat"):
            st.session_state.menu = "tercepat"
        if st.sidebar.button("🎫 Beli Tiket"):
            st.session_state.menu = "beli"
        if st.sidebar.button("📜 Riwayat"):
            st.session_state.menu = "riwayat"
        if st.sidebar.button("🌐 Graph"):
            st.session_state.menu = "graph"


    # ==========================================
    # MENU ADMIN
    # ==========================================
    if st.session_state.role == "admin":
        if st.sidebar.button("📊 Dashboard"):
            st.session_state.menu = "dashboard"
        if st.sidebar.button("🚉 Kelola Stasiun"):
            st.session_state.menu = "stasiun"
        if st.sidebar.button("🔗 Kelola Jalur"):
            st.session_state.menu = "jalur"
        if st.sidebar.button("📜 Riwayat Tiket"):
            st.session_state.menu = "riwayat"


    # ==========================================
    # RUTE
    # ==========================================
    if st.session_state.menu == "rute":

        st.subheader("🗺️ Cari Rute")

        a = st.selectbox("Dari", list(kereta.graf.keys()))
        b = st.selectbox("Ke", list(kereta.graf.keys()))

        if st.button("Cari"):
            r, d = kereta.dijkstra(a, b)
            st.info(f"{' → '.join(r)} | {d} KM")


    # ==========================================
    # TERCEPAT
    # ==========================================
    elif st.session_state.menu == "tercepat":

        st.subheader("⚡ Jalur Tercepat")

        a = st.selectbox("Dari", list(kereta.graf.keys()), key="a")
        b = st.selectbox("Ke", list(kereta.graf.keys()), key="b")

        if st.button("Cari Cepat"):
            r, d = kereta.dijkstra(a, b)
            st.success(f"Jalur: {' → '.join(r)}")
            st.info(f"Jarak: {d} KM | Estimasi: {d//2} menit")


   # ==========================================
# BELI TIKET (VERSI E-WALLET + TRANSFER)
# ==========================================
elif st.session_state.menu == "beli":

    st.subheader("🎫 Pembelian Tiket")

    col1, col2 = st.columns(2)

    with col1:
        asal = st.selectbox("🚉 Stasiun Awal", list(kereta.graf.keys()), key="asal_beli")

    with col2:
        tujuan = st.selectbox("🚉 Stasiun Tujuan", list(kereta.graf.keys()), key="tujuan_beli")

    jalur = st.radio(
        "⚡ Pilih Jalur",
        ["Jalur Tercepat", "Jalur Reguler"]
    )

    kelas = st.selectbox(
        "🎫 Pilih Kelas",
        ["Ekonomi", "Bisnis", "Eksekutif"]
    )

    jumlah = st.number_input(
        "🎟️ Jumlah Tiket",
        min_value=1,
        value=1
    )

    jadwal = st.selectbox(
        "🕒 Pilih Jadwal",
        ["08:00 WIB", "12:00 WIB", "18:00 WIB"]
    )

    kursi = st.text_input(
        "🪑 Nomor Kursi",
        value="A1"
    )

    # =========================
    # PEMBAYARAN E-WALLET / TRANSFER
    # =========================
    metode = st.selectbox(
        "💳 Metode Pembayaran",
        [
            "DANA",
            "OVO",
            "GoPay",
            "ShopeePay",
            "Transfer BCA",
            "Transfer BRI",
            "Transfer BNI",
            "Transfer Mandiri"
        ]
    )

    nomor_ewallet = st.text_input("📱 Nomor / ID Pembayaran")

    if st.button("💳 Bayar Sekarang"):

        if not nomor_ewallet:
            st.error("❌ Masukkan nomor e-wallet / rekening terlebih dahulu!")
        else:

            rute, jarak = kereta.dijkstra(asal, tujuan)

            if kelas == "Ekonomi":
                harga_per_km = 1000
            elif kelas == "Bisnis":
                harga_per_km = 1500
            else:
                harga_per_km = 2000

            total = jarak * harga_per_km * jumlah
            kode = random.randint(10000, 99999)

            st.session_state.riwayat.append({
                "nama": st.session_state.nama,
                "asal": asal,
                "tujuan": tujuan,
                "jalur": jalur,
                "kelas": kelas,
                "jumlah": jumlah,
                "jadwal": jadwal,
                "kursi": kursi,
                "pembayaran": metode,
                "nomor": nomor_ewallet,
                "harga": total
            })

            st.success("✅ Pembayaran Berhasil!")

            st.code(f"""
══════════════════════════════
      🎫 E-TIKET KERETA
══════════════════════════════

🎟️ Kode Tiket : {kode}
👤 Nama       : {st.session_state.nama}
🚉 Dari       : {asal}
🚉 Tujuan     : {tujuan}
⚡ Jalur      : {jalur}
🚆 Rute       : {' → '.join(rute)}
🎫 Kelas      : {kelas}
🎟️ Jumlah     : {jumlah}
🪑 Kursi      : {kursi}
🕒 Jadwal     : {jadwal}
💳 Metode     : {metode}
📱 ID         : {nomor_ewallet}
💵 Total      : Rp{total:,}

══════════════════════════════
Selamat Menikmati Perjalanan 🚄
══════════════════════════════
""")


    # ==========================================
    # RIWAYAT
    # ==========================================
    elif st.session_state.menu == "riwayat":

        st.subheader("📜 Riwayat")

        for t in st.session_state.riwayat:
            st.write(t)


    # ==========================================
    # GRAPH
    # ==========================================
    elif st.session_state.menu == "graph":

        st.subheader("🌐 Graph Rute")

        for s in kereta.graf:
            st.write(f"{s} → {kereta.graf[s]}")


    # ==========================================
    # DASHBOARD ADMIN
    # ==========================================
    elif st.session_state.menu == "dashboard":

        st.metric("Total Tiket", len(st.session_state.riwayat))
        st.metric("Pendapatan", sum(t["harga"] for t in st.session_state.riwayat))


    # ==========================================
    # STASIUN ADMIN
    # ==========================================
    elif st.session_state.menu == "stasiun":

        nama = st.text_input("Tambah Stasiun Baru")

        if st.button("Tambah"):
            if nama:
                kereta.graf[nama] = []
                st.success("Stasiun ditambah")

        st.write(list(kereta.graf.keys()))


    # ==========================================
    # JALUR ADMIN
    # ==========================================
    elif st.session_state.menu == "jalur":

        a = st.selectbox("Dari", list(kereta.graf.keys()))
        b = st.selectbox("Ke", list(kereta.graf.keys()))
        jarak = st.number_input("Jarak", 1)

        if st.button("Tambah"):
            kereta.graf[a].append((b, jarak))
            kereta.graf[b].append((a, jarak))
            st.success("Jalur ditambah")
