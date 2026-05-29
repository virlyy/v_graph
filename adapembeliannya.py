import streamlit as st
import heapq
import random

# ======================================
# CONFIG PAGE
# ======================================
st.set_page_config(
    page_title="Stasiun VY Junction",
    page_icon="🚆",
    layout="wide"
)

# ======================================
# CUSTOM CSS
# ======================================
st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# SESSION STATE
# ======================================
if "login" not in st.session_state:
    st.session_state.login = False

if "nama" not in st.session_state:
    st.session_state.nama = ""

if "saldo" not in st.session_state:
    st.session_state.saldo = 500000

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ======================================
# CLASS LOGIN
# ======================================
class Login:

    def __init__(self, nama, no_hp, email):

        self.nama = nama
        self.no_hp = no_hp
        self.email = email

# ======================================
# GRAPH KERETA
# ======================================
graf = {

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
def dijkstra(mulai, tujuan):

    jarak = {
        stasiun: float('inf')
        for stasiun in graf
    }

    jalur = {
        stasiun: None
        for stasiun in graf
    }

    jarak[mulai] = 0

    pq = [(0, mulai)]

    while pq:

        jarak_sekarang, stasiun_sekarang = heapq.heappop(pq)

        if stasiun_sekarang == tujuan:
            break

        for tetangga, bobot in graf[stasiun_sekarang]:

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
# LOGIN PAGE
# ======================================
if st.session_state.login == False:

    st.title("🚆 LOGIN STASIUN VY JUNCTION")

    nama = st.text_input("Nama")
    no_hp = st.text_input("No HP")
    email = st.text_input("Email")

    if st.button("Login"):

        if nama != "" and no_hp != "" and email != "":

            user = Login(nama, no_hp, email)

            st.session_state.login = True
            st.session_state.nama = nama

            st.rerun()

        else:

            st.error("❌ Semua data harus diisi!")

# ======================================
# HALAMAN UTAMA
# ======================================
else:

    st.title("🚆 STASIUN VY JUNCTION")

    st.success(f"Selamat Datang, {st.session_state.nama}")

    # ======================================
    # SIDEBAR MENU
    # ======================================
    menu = st.sidebar.selectbox(
        "Pilih Menu",
        [
            "Lihat Rute",
            "Beli Tiket",
            "Cek Saldo",
            "Top Up Saldo",
            "Daftar Stasiun",
            "Cek Koneksi Stasiun",
            "Riwayat Tiket",
            "Logout"
        ]
    )

    # ======================================
    # LIHAT RUTE
    # ======================================
    if menu == "Lihat Rute":

        st.subheader("📍 Cek Rute Kereta")

        col1, col2 = st.columns(2)

        with col1:
            mulai = st.selectbox(
                "Stasiun Awal",
                list(graf.keys())
            )

        with col2:
            tujuan = st.selectbox(
                "Stasiun Tujuan",
                list(graf.keys())
            )

        if st.button("Lihat Rute"):

            rute, total_jarak = dijkstra(mulai, tujuan)

            st.success("Rute Ditemukan!")

            st.write(f"🚉 Dari : {mulai}")
            st.write(f"🚉 Ke : {tujuan}")
            st.write(f"🚆 Jalur : {' → '.join(rute)}")
            st.write(f"📍 Total Jarak : {total_jarak} KM")

    # ======================================
    # BELI TIKET
    # ======================================
    elif menu == "Beli Tiket":

        st.subheader("🎫 Pembelian Tiket")

        col1, col2 = st.columns(2)

        with col1:
            mulai = st.selectbox(
                "Stasiun Awal",
                list(graf.keys())
            )

        with col2:
            tujuan = st.selectbox(
                "Stasiun Tujuan",
                list(graf.keys())
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

        kursi = st.text_input("Nomor Kursi", "A1")

        if st.button("Pesan Tiket"):

            rute, total_jarak = dijkstra(mulai, tujuan)

            if kelas == "Ekonomi":
                harga = total_jarak * 1000

            elif kelas == "Bisnis":
                harga = total_jarak * 1500

            else:
                harga = total_jarak * 2000

            total = harga * jumlah

            if st.session_state.saldo >= total:

                st.session_state.saldo -= total

                kode = random.randint(10000, 99999)

                st.session_state.riwayat.append({

                    "nama": st.session_state.nama,
                    "asal": mulai,
                    "tujuan": tujuan,
                    "kelas": kelas,
                    "harga": total

                })

                st.success("✅ Pembayaran Berhasil!")

                st.markdown(f"""
                ### 🎟️ DETAIL TIKET

                👤 Nama : {st.session_state.nama}

                🚉 Dari : {mulai}

                🚉 Ke : {tujuan}

                🚆 Jalur : {' → '.join(rute)}

                🎫 Kelas : {kelas}

                🪑 Kursi : {kursi}

                🕒 Jadwal : {jadwal}

                💵 Total : Rp{total}

                🔖 Kode Tiket : {kode}
                """)

            else:

                st.error("❌ Saldo Tidak Cukup!")

                st.markdown(f"""
                ### 💳 INFORMASI PEMBAYARAN

                💵 Total Harga Tiket : Rp{total}

                💰 Saldo Anda : Rp{st.session_state.saldo}

                ⚠️ Silakan lakukan top up saldo terlebih dahulu.
                """)

    # ======================================
    # CEK SALDO
    # ======================================
    elif menu == "Cek Saldo":

        st.subheader("💰 E-Wallet")

        st.info(f"Saldo Anda : Rp{st.session_state.saldo}")

    # ======================================
    # TOP UP SALDO
    # ======================================
    elif menu == "Top Up Saldo":

        st.subheader("➕ Top Up Saldo")

        topup = st.text_input(
            "Masukkan Jumlah Top Up"
        )

        if st.button("Top Up"):

            if topup.isdigit():

                st.session_state.saldo += int(topup)

                st.success("✅ Top Up Berhasil!")

                st.write(f"💰 Saldo Sekarang : Rp{st.session_state.saldo}")

            else:

                st.error("❌ Masukkan angka yang valid!")

    # ======================================
    # DAFTAR STASIUN
    # ======================================
    elif menu == "Daftar Stasiun":

        st.subheader("🚉 Daftar Stasiun")

        for stasiun in graf:
            st.write(f"✅ {stasiun}")

    # ======================================
    # CEK KONEKSI STASIUN
    # ======================================
    elif menu == "Cek Koneksi Stasiun":

        st.subheader("🔗 Koneksi Stasiun")

        stasiun = st.selectbox(
            "Pilih Stasiun",
            list(graf.keys())
        )

        st.write(f"### 🚉 Koneksi Dari {stasiun}")

        for tujuan, jarak in graf[stasiun]:

            st.write(f"➡️ {tujuan} ({jarak} KM)")

    # ======================================
    # RIWAYAT TIKET
    # ======================================
    elif menu == "Riwayat Tiket":

        st.subheader("📜 Riwayat Pembelian")

        if len(st.session_state.riwayat) == 0:

            st.warning("Belum ada pembelian tiket.")

        else:

            for data in st.session_state.riwayat:

                st.markdown(f"""
                ---
                👤 Nama : {data['nama']}

                🚉 Dari : {data['asal']}

                🚉 Ke : {data['tujuan']}

                🎫 Kelas : {data['kelas']}

                💵 Harga : Rp{data['harga']}
                """)

    # ======================================
    # LOGOUT
    # ======================================
    elif menu == "Logout":

        st.session_state.login = False
        st.rerun()
