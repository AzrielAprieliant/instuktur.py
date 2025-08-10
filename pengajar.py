import streamlit as st
import pandas as pd

# =========================
# Konfigurasi halaman
# =========================
st.set_page_config(page_title="Dashboard Instruktur", layout="wide", initial_sidebar_state="collapsed")
st.title("📊 Dashboard Penilaian Instruktur")

# =========================
# Load data
# =========================
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Pastikan kolom yang diperlukan ada
df = df.rename(columns={
    "Nama": "Nama",
    "Nama Diklat": "Nama Diklat",
    "Mata Ajar": "Mata Ajar",
    "Nama Unit": "Nama Unit",
    "Tahun": "Tahun",
    "Rata-Rata": "Nilai"
})

# Perbaiki nilai agar tidak ada angka aneh
df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce")
df = df[df["Nilai"].between(0, 5)]  # Batasi nilai antara 0 dan 5

# =========================
# Filter
# =========================
# Pilih Nama Diklat
pilihan_diklat = st.selectbox("Pilih Nama Diklat", ["Semua"] + sorted(df["Nama Diklat"].unique().tolist()))

# Filter Nama Unit & Mata Ajar berdasarkan Diklat yang dipilih
if pilihan_diklat != "Semua":
    df_filtered = df[df["Nama Diklat"] == pilihan_diklat]
    pilihan_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df_filtered["Nama Unit"].unique().tolist()))
    pilihan_mata = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df_filtered["Mata Ajar"].unique().tolist()))
else:
    df_filtered = df.copy()
    pilihan_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df["Nama Unit"].unique().tolist()))
    pilihan_mata = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df["Mata Ajar"].unique().tolist()))

# Terapkan filter unit
if pilihan_unit != "Semua":
    df_filtered = df_filtered[df_filtered["Nama Unit"] == pilihan_unit]

# Terapkan filter mata ajar
if pilihan_mata != "Semua":
    df_filtered = df_filtered[df_filtered["Mata Ajar"] == pilihan_mata]

# =========================
# Ranking
# =========================
df_filtered = df_filtered.sort_values(by="Nilai", ascending=False)
df_filtered.insert(0, "Ranking", range(1, len(df_filtered) + 1))

# Urutkan kolom sesuai permintaan
df_filtered = df_filtered[["Ranking", "Nama", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Nilai"]]

# =========================
# Judul tabel
# =========================
st.subheader("📋 Data Instruktur Nilai Tertinggi")

# =========================
# Tampilkan tabel dengan border
# =========================
st.markdown("""
<style>
table {
    border-collapse: collapse;
    width: 100%;
    border: 2px solid white;
}
th, td {
    border: 1px solid white;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

st.dataframe(df_filtered, use_container_width=True)
