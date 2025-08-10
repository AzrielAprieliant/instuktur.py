import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="📊 Dashboard Penilaian Instruktur", layout="wide")

# Load data
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Bersihkan data Rata-Rata (hapus nilai terlalu besar)
df = df[df["Rata-Rata"] <= 10]  # anggap skala nilai maksimal 10

# Pilih Nama Diklat
nama_diklat_terpilih = st.selectbox(
    "Pilih Nama Diklat",
    sorted(df["Nama Diklat"].unique().tolist())
)

# Filter Nama Unit sesuai Nama Diklat yang dipilih
df_filtered_unit = df[df["Nama Diklat"] == nama_diklat_terpilih]
pilihan_unit = st.selectbox(
    "Pilih Nama Unit",
    sorted(df_filtered_unit["Nama Unit"].unique().tolist())
)

# Filter Mata Ajar sesuai Nama Diklat yang dipilih
df_filtered_mata_ajar = df_filtered_unit[df_filtered_unit["Nama Unit"] == pilihan_unit]
pilihan_mata_ajar = st.selectbox(
    "Pilih Mata Ajar",
    sorted(df_filtered_mata_ajar["Mata Ajar"].unique().tolist())
)

# Filter final berdasarkan semua pilihan
df_final = df_filtered_mata_ajar[df_filtered_mata_ajar["Mata Ajar"] == pilihan_mata_ajar]

# Tampilkan tabel dengan border box
st.markdown(
    """
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid #888;
        padding: 8px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.dataframe(df_final, use_container_width=True)
