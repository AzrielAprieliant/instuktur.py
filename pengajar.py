import streamlit as st
import pandas as pd

# =====================
# KONFIGURASI TEMA PUTIH
# =====================
st.set_page_config(
    page_title="Dashboard Pengajar Nilai Tertinggi",
    layout="wide"
)

# CSS untuk memastikan background putih
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# =====================
# LOAD DATA
# =====================
# Ganti file ini dengan file Excel kamu
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Pastikan kolom sesuai
# Contoh kolom: Nama Diklat, Nama Unit, Mata Ajar, Pengajar, Rata-Rata
# Ubah sesuai nama kolom sebenarnya di file Excel kamu
df["Rata-Rata"] = pd.to_numeric(df["Rata-Rata"], errors="coerce")

# =====================
# FILTER DROPDOWN
# =====================
col1, col2, col3 = st.columns(3)

# 1. Nama Diklat (tidak memfilter)
with col1:
    nama_diklat = st.selectbox(
        "Nama Diklat",
        sorted(df["Nama Diklat"].unique())
    )

# 2. Nama Unit (memfilter)
with col2:
    unit_options = ["Semua"] + sorted(df["Nama Unit"].unique())
    nama_unit = st.selectbox("Nama Unit", unit_options)

# 3. Mata Ajar (memfilter)
with col3:
    mata_ajar_options = ["Semua"] + sorted(df["Mata Ajar"].unique())
    mata_ajar = st.selectbox("Mata Ajar", mata_ajar_options)

# =====================
# APLIKASI FILTER
# =====================
df_filtered = df.copy()

if nama_unit != "Semua":
    df_filtered = df_filtered[df_filtered["Nama Unit"] == nama_unit]

if mata_ajar != "Semua":
    df_filtered = df_filtered[df_filtered["Mata Ajar"] == mata_ajar]

# =====================
# TAMPILKAN HASIL
# =====================
st.subheader(f"Pengajar Nilai Tertinggi - {nama_diklat}")

if df_filtered.empty:
    st.warning("Tidak ada data untuk filter ini.")
else:
    # Urutkan berdasarkan nilai rata-rata
    df_top = df_filtered.sort_values("Rata-Rata", ascending=False).head(10)
    st.dataframe(df_top, use_container_width=True)
