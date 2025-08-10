import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Nilai Pengajar", layout="wide")

# CSS untuk background putih dan judul hitam
st.markdown(
    """
    <style>
        .stApp {
            background-color: white;
        }
        h1, h2, h3, h4, h5, h6, p {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul dashboard
st.title("📊 Dashboard Nilai Pengajar Tertinggi")

# Baca file Excel langsung
file_path = "Penilaian Gabung dengan Nama Unit.xlsx"
df = pd.read_excel(file_path)

# Pastikan kolom yang dibutuhkan ada
required_columns = ["Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]
if not all(col in df.columns for col in required_columns):
    st.error("Kolom yang diperlukan tidak ditemukan di file.")
else:
    # Filter nilai maksimal 5
    df = df[df["Rata-Rata"] <= 5]

    # Dropdown filter
    nama_diklat = st.selectbox("Pilih Nama Diklat", sorted(df["Nama Diklat"].dropna().unique().tolist()))
    nama_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df["Nama Unit"].dropna().unique().tolist()))
    mata_ajar = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df["Mata Ajar"].dropna().unique().tolist()))

    # Filter data
    filtered_df = df[df["Nama Diklat"] == nama_diklat]
    if nama_unit != "Semua":
        filtered_df = filtered_df[filtered_df["Nama Unit"] == nama_unit]
    if mata_ajar != "Semua":
        filtered_df = filtered_df[filtered_df["Mata Ajar"] == mata_ajar]

    # Urutkan berdasarkan Rata-Rata tertinggi
    filtered_df = filtered_df.sort_values(by="Rata-Rata", ascending=False)

    filtered_df.insert(0, "Ranking", range(1, len(filtered_df) + 1))

    # Pilih kolom yang ditampilkan
    show_df = filtered_df[["Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]]

    # Judul sebelum tabel
    st.subheader("📋 Hasil Data")

    # Tampilkan tabel
    st.dataframe(show_df, use_container_width=True)

    # Download hasil
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    st.download_button(
        label="📥 Unduh Hasil sebagai Excel",
        data=convert_df(show_df),
        file_name="nilai_pengajar_tertinggi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
