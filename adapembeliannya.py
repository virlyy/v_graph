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

    # ==========================================
    # ALGORITMA DIJKSTRA
    # ==========================================
    def dijkstra(self, mulai, tujuan):

        jarak = {
            stasiun: float("inf")
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
# OBJECT GRAPH
# ==========================================
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

    role = st.radio(
        "Login Sebagai",
        ["User", "Admin"]
    )

    nama = st.text_input("👤 Nama")
    no_hp = st.text_input("📱 No HP")
    email = st.text_input("📧 Email")

    if st.button("🚪 Login"):

        if role == "Admin":

            if nama == "admin" and email == "admin@gmail.com":

                st.session_state.login = True
                st.session_state.role = "admin"
                st.session_state.nama = "Admin"

                st.rerun()

            else:
                st.error("❌ Login admin salah")

        else:

            if nama and no_hp and email:

                user = Login(
                    nama,
                    no_hp,
                    email
                )

                st.session_state.login = True
                st.session_state.role = "user"
                st.session_state.nama = user.nama

                st.rerun()

            else:
                st.error("❌ Semua data harus diisi")


# ==========================================
# HALAMAN UTAMA
# ==========================================
else:

    st.title("🚆 STASIUN VY JUNCTION")

    st.success(
        f"Selamat Datang, {st.session_state.nama}"
    )

    # ==========================================
    # LOGOUT
    # ==========================================
    if st.sidebar.button("🔒 Logout"):

        st.session_state.logout_confirm = True

    if st.session_state.logout_confirm:

        st.warning("Yakin ingin logout?")

        col1, col2 = st.columns(2)

        with col1:

            if st.button("Ya"):

                st.session_state.login = False
                st.session_state.role = ""
                st.session_state.logout_confirm = False

                st.rerun()

        with col2:

            if st.button("Batal"):

                st.session_state.logout_confirm = False
                st.rerun()

    # ==========================================
    # MENU SIDEBAR
    # ==========================================
    st.sidebar.title("🚆 MENU")

    if st.session_state.role == "user":

        if st.sidebar.button("🗺️ Lihat Rute"):
            st.session_state.menu = "rute"

        if st.sidebar.button("⚡ Jalur Tercepat"):
            st.session_state.menu = "tercepat"

        if st.sidebar.button("🎫 Beli Tiket"):
            st.session_state.menu = "beli"

        if st.sidebar.button("🌐 Jaringan Rute"):
            st.session_state.menu = "graph"

        if st.sidebar.button("🚉 Daftar Stasiun"):
            st.session_state.menu = "stasiun_user"

        if st.sidebar.button("🔗 Koneksi Stasiun"):
            st.session_state.menu = "koneksi"

        if st.sidebar.button("📜 Riwayat Tiket"):
            st.session_state.menu = "riwayat"

    elif st.session_state.role == "admin":

        if st.sidebar.button("📊 Dashboard"):
            st.session_state.menu = "dashboard"

        if st.sidebar.button("🚉 Kelola Stasiun"):
            st.session_state.menu = "stasiun"

        if st.sidebar.button("🔗 Kelola Jalur"):
            st.session_state.menu = "jalur"

        if st.sidebar.button("🎫 Data Tiket"):
            st.session_state.menu = "tiket"

        if st.sidebar.button("💰 Laporan"):
            st.session_state.menu = "laporan"

    # ==========================================
    # LIHAT RUTE
    # ==========================================
    if st.session_state.menu == "rute":

        st.subheader("🗺️ Cari Rute Kereta")

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

        if st.button("🔍 Cari Rute"):

            rute, total_jarak = kereta.dijkstra(
                mulai,
                tujuan
            )

            st.success("Rute ditemukan")

            st.info(
                f"{' → '.join(rute)} | {total_jarak} KM"
            )

    # ==========================================
    # JALUR TERCEPAT
    # ==========================================
    elif st.session_state.menu == "tercepat":

        st.subheader("⚡ Cari Jalur Tercepat")

        col1, col2 = st.columns(2)

        with col1:

            mulai = st.selectbox(
                "Stasiun Awal",
                list(kereta.graf.keys()),
                key="awal_cepat"
            )

        with col2:

            tujuan = st.selectbox(
                "Stasiun Tujuan",
                list(kereta.graf.keys()),
                key="tujuan_cepat"
            )

        if st.button("⚡ Cari Jalur"):

            rute, total_jarak = kereta.dijkstra(
                mulai,
                tujuan
            )

            estimasi = total_jarak // 2

            st.success("Jalur tercepat ditemukan")
            st.info(f"""
🚉 Dari          : {mulai}

🚉 Tujuan        : {tujuan}

🚆 Jalur         : {' → '.join(rute)}

📍 Jarak Minimum : {total_jarak} KM

⏱️ Estimasi      : {estimasi} Menit
""")

    # ==========================================
    # BELI TIKET
    # ==========================================
    elif st.session_state.menu == "beli":

        st.subheader("🎫 Pembelian Tiket")

        col1, col2 = st.columns(2)

        with col1:

            mulai2 = st.selectbox(
                "🚉 Stasiun Awal",
                list(kereta.graf.keys())
            )

        with col2:

            tujuan2 = st.selectbox(
                "🚉 Stasiun Tujuan",
                list(kereta.graf.keys())
            )

        jalur = st.radio(
            "⚡ Pilih Jalur",
            [
                "Jalur Tercepat",
                "Jalur Reguler"
            ]
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
            min_value=1,
            value=1
        )

        jadwal = st.selectbox(
            "🕒 Jadwal Keberangkatan",
            [
                "08:00 WIB",
                "12:00 WIB",
                "18:00 WIB"
            ]
        )

        kursi = st.text_input(
            "🪑 Nomor Kursi",
            value="A1"
        )

        pembayaran = st.selectbox(
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

        if st.button("💳 Bayar Sekarang"):

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

            kode = random.randint(
                10000,
                99999
            )

            st.session_state.riwayat.append({

                "nama": st.session_state.nama,
                "asal": mulai2,
                "tujuan": tujuan2,
                "kelas": kelas,
                "jalur": jalur,
                "jadwal": jadwal,
                "kursi": kursi,
                "bayar": pembayaran,
                "harga": total

            })

            st.success(
                "✅ Pembayaran Berhasil"
            )

            st.code(f"""
══════════════════════════════
       🎫 E-TIKET KERETA
══════════════════════════════

🎟️ Kode Tiket : {kode}
👤 Nama       : {st.session_state.nama}

🚉 Asal       : {mulai2}
🚉 Tujuan     : {tujuan2}

⚡ Jalur      : {jalur}

🚆 Rute       :
{' -> '.join(rute)}

🎫 Kelas      : {kelas}
🪑 Kursi      : {kursi}

🕒 Jadwal     : {jadwal}

💳 Pembayaran :
{pembayaran}

💵 Total :
Rp{total:,}

══════════════════════════════
 Selamat Menikmati Perjalanan
══════════════════════════════
""")

    # ==========================================
    # RIWAYAT TIKET
    # ==========================================
    elif st.session_state.menu == "riwayat":

        st.subheader(
            "📜 Riwayat Pembelian"
        )

        if len(
            st.session_state.riwayat
        ) == 0:

            st.warning(
                "Belum ada transaksi"
            )

        else:

            for data in st.session_state.riwayat:

                st.code(f"""
👤 Nama   : {data['nama']}

🚉 Asal   : {data['asal']}

🚉 Tujuan : {data['tujuan']}

🎫 Kelas  : {data['kelas']}

💳 Bayar  : {data['bayar']}

💵 Harga  : Rp{data['harga']:,}
""")

    # ==========================================
    # JARINGAN GRAPH
    # ==========================================
    elif st.session_state.menu == "graph":

        st.subheader(
            "🌐 Jaringan Rute Kereta"
        )

        for stasiun in kereta.graf:

            st.write(
                f"## 🚉 {stasiun}"
            )

            for tujuan, jarak in kereta.graf[stasiun]:

                st.write(
                    f"➡️ {tujuan} ({jarak} KM)"
                )

    # ==========================================
    # DAFTAR STASIUN
    # ==========================================
    elif st.session_state.menu == "stasiun_user":

        st.subheader(
            "🚉 Daftar Stasiun"
        )

        for stasiun in kereta.graf.keys():

            st.write(
                f"➡️ {stasiun}"
            )

    # ==========================================
    # KONEKSI STASIUN
    # ==========================================
    elif st.session_state.menu == "koneksi":

        st.subheader(
            "🔗 Koneksi Stasiun"
        )

        pilih = st.selectbox(
            "Pilih Stasiun",
            list(
                kereta.graf.keys()
            )
        )

        st.write(
            f"### 🚉 {pilih}"
        )

        for tujuan, jarak in kereta.graf[pilih]:

            st.write(
                f"➡️ {tujuan} ({jarak} KM)"
            )

    # ==========================================
    # DASHBOARD ADMIN
    # ==========================================
    elif st.session_state.menu == "dashboard":

        st.subheader(
            "📊 Dashboard Admin"
        )

        total_tiket = len(
            st.session_state.riwayat
        )

        total_pendapatan = sum(
            tiket["harga"]
            for tiket
            in st.session_state.riwayat
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Tiket",
                total_tiket
            )

        with col2:

            st.metric(
                "Pendapatan",
                f"Rp{total_pendapatan:,}"
            )

    # ==========================================
    # KELOLA STASIUN
    # ==========================================
    elif st.session_state.menu == "stasiun":

        st.subheader(
            "🚉 Kelola Stasiun"
        )
    # ==========================================
    # TAMBAH STASIUN
    # ==========================================
        nama_baru = st.text_input("Nama Stasiun Baru")

        if st.button("Tambah Stasiun"):

            if nama_baru:

                if nama_baru not in kereta.graf:

                    kereta.graf[nama_baru] = []
                    st.success("Stasiun berhasil ditambah")

                else:
                    st.warning("Stasiun sudah ada")

        st.divider()
    # ==========================================
    # EDIT STASIUN
    # ==========================================
        st.write("### ✏️ Edit Stasiun")

        daftar_stasiun = list(kereta.graf.keys())

        if daftar_stasiun:

            stasiun_lama = st.selectbox(
                "Pilih stasiun yang mau diedit",
                daftar_stasiun
            )

            nama_baru_edit = st.text_input("Nama baru stasiun")

            if st.button("Update Nama Stasiun"):

                if nama_baru_edit:

                    kereta.graf[nama_baru_edit] = kereta.graf.pop(stasiun_lama)
                    st.success("Nama stasiun berhasil diubah")

        st.divider()
    # ==========================================
    # HAPUS STASIUN
    # ==========================================
        st.write("### 🗑️ Hapus Stasiun")

        if daftar_stasiun:

            stasiun_hapus = st.selectbox(
                "Pilih stasiun yang mau dihapus",
                daftar_stasiun,
                key="hapus"
            )

            if st.button("Hapus Stasiun"):

                del kereta.graf[stasiun_hapus]
                st.success("Stasiun berhasil dihapus")

        st.divider()

        # =========================
        # TAMPILKAN
        # =========================
        st.write("### 📍 Daftar Stasiun")

        st.write(list(kereta.graf.keys()))
    # ==========================================
    # KELOLA JALUR
    # ==========================================
    elif st.session_state.menu == "jalur":

        st.subheader(
            "🔗 Kelola Jalur"
        )

        asal = st.selectbox(
            "Dari",
            list(
                kereta.graf.keys()
            )
        )

        tujuan = st.selectbox(
            "Ke",
            list(
                kereta.graf.keys()
            )
        )

        jarak = st.number_input(
            "Jarak (KM)",
            min_value=1
        )

        if st.button(
            "Tambah Jalur"
        ):

            kereta.graf[asal].append(
                (
                    tujuan,
                    jarak
                )
            )

            kereta.graf[tujuan].append(
                (
                    asal,
                    jarak
                )
            )

            st.success(
                "Jalur berhasil ditambahkan"
            )

    # ==========================================
    # DATA TIKET ADMIN
    # ==========================================
    elif st.session_state.menu == "tiket":

        st.subheader(
            "🎫 Data Tiket"
        )

        if len(
            st.session_state.riwayat
        ) == 0:

            st.warning(
                "Belum ada tiket"
            )

        else:

            for data in st.session_state.riwayat:

                st.code(f"""
Nama      : {data['nama']}
Asal      : {data['asal']}
Tujuan    : {data['tujuan']}
Kelas     : {data['kelas']}
Pembayaran: {data['bayar']}
Harga     : Rp{data['harga']:,}
""")

    # ==========================================
    # LAPORAN
    # ==========================================
    elif st.session_state.menu == "laporan":

        st.subheader(
            "💰 Laporan Pendapatan"
        )

        total_tiket = len(
            st.session_state.riwayat
        )

        total_pendapatan = sum(
            tiket["harga"]
            for tiket
            in st.session_state.riwayat
        )

        st.metric(
            "Total Tiket Terjual",
            total_tiket
        )

        st.metric(
            "Total Pendapatan",
            f"Rp{total_pendapatan:,}"
        )
