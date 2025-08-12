import streamlit as st
import pandas as pd

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
    # Pastikan hanya nilai <= 5
    df = df[df["Rata-Rata"] <= 5]

    # --- Dropdown Nama Unit (paling atas) ---
    nama_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df["Nama Unit"].dropna().unique().tolist()))

    # Filter berdasarkan Nama Unit
    df_filtered = df.copy()
    if nama_unit != "Semua":
        df_filtered = df_filtered[df_filtered["Nama Unit"] == nama_unit]

    # --- Dropdown Nama Diklat (kedua) ---
    nama_diklat = st.selectbox("Pilih Nama Diklat", ["Semua"] + sorted(df_filtered["Nama Diklat"].dropna().unique().tolist()))

    # Filter berdasarkan Nama Diklat
    if nama_diklat != "Semua":
        df_filtered = df_filtered[df_filtered["Nama Diklat"] == nama_diklat]

    # --- Dropdown Mata Ajar (terakhir) ---
    mata_ajar = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df_filtered["Mata Ajar"].dropna().unique().tolist()))

    # Filter berdasarkan Mata Ajar
    if mata_ajar != "Semua":
        df_filtered = df_filtered[df_filtered["Mata Ajar"] == mata_ajar]

    # Urutkan berdasarkan Rata-Rata
    df_filtered = df_filtered.sort_values(by="Rata-Rata", ascending=False).reset_index(drop=True)
    df_filtered.insert(0, "Ranking", range(1, len(df_filtered) + 1))

    # Data yang ditampilkan
    show_df = df_filtered[["Ranking", "Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]]

    st.subheader("🏆 Pengajar Nilai Tertinggi")
    st.dataframe(show_df, use_container_width=True, hide_index=True) 
