import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Dashboard Nilai Pengajar", layout="wide")

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

st.title("📊 Dashboard Nilai Pengajar Tertinggi")

file_path = "Data_Gabung.xlsx"
df = pd.read_excel(file_path)

required_columns = ["Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]
if not all(col in df.columns for col in required_columns):
    st.error("Kolom yang diperlukan tidak ditemukan di file.")
else:
    df = df[df["Rata-Rata"] <= 5]

    # Semua dropdown ambil opsi dari df asli (tanpa filter)
    nama_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df["Nama Unit"].dropna().unique().tolist()))
    nama_diklat = st.selectbox("Pilih Nama Diklat", ["Semua"] + sorted(df["Nama Diklat"].dropna().unique().tolist()))
    mata_ajar = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df["Mata Ajar"].dropna().unique().tolist()))

    # Filter data hanya sekali di sini
    df_filtered = df.copy()
    if nama_unit != "Semua":
        df_filtered = df_filtered[df_filtered["Nama Unit"] == nama_unit]
    if nama_diklat != "Semua":
        df_filtered = df_filtered[df_filtered["Nama Diklat"] == nama_diklat]
    if mata_ajar != "Semua":
        df_filtered = df_filtered[df_filtered["Mata Ajar"] == mata_ajar]

    df_filtered = df_filtered.drop_duplicates(
    subset=["Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]
    )

    # Ranking
    df_filtered = df_filtered.sort_values(by="Rata-Rata", ascending=False).reset_index(drop=True)
    df_filtered.insert(0, "Ranking", range(1, len(df_filtered) + 1))

    show_df = df_filtered[["Ranking", "Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]]

    st.subheader("🏆 Pengajar Nilai Tertinggi")
    st.dataframe(show_df, use_container_width=True, hide_index=True)
