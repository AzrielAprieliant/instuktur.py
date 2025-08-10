import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Instruktur", layout="wide", initial_sidebar_state="collapsed")
st.title("📊 Dashboard Penilaian Instruktur")

# Load data
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Pastikan kolom yang digunakan sesuai format
df = df.rename(columns=lambda x: x.strip())
df = df.drop(columns=["Sumber Sheet"], errors="ignore")

# Hapus nilai yang bukan angka di kolom Nilai
df = df[pd.to_numeric(df["Nilai"], errors="coerce").notna()]
df["Nilai"] = df["Nilai"].astype(float)

# Filter dropdown dengan "Semua"
pilihan_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df["Nama Unit"].unique().tolist()))
pilihan_mata_ajar = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df["Mata Ajar"].unique().tolist()))

# Filter data
df_filtered = df.copy()
if pilihan_unit != "Semua":
    df_filtered = df_filtered[df_filtered["Nama Unit"] == pilihan_unit]
if pilihan_mata_ajar != "Semua":
    df_filtered = df_filtered[df_filtered["Mata Ajar"] == pilihan_mata_ajar]

# Ranking berdasarkan Nilai tertinggi
df_filtered = df_filtered.sort_values(by="Nilai", ascending=False).reset_index(drop=True)
df_filtered.insert(0, "Ranking", range(1, len(df_filtered) + 1))

# Urutkan kolom
kolom_urut = ["Ranking", "Nama", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Nilai"]
df_filtered = df_filtered[kolom_urut]

# Style tabel
st.markdown(
    """
    <style>
    .styled-table {
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 14px;
        font-family: Arial, sans-serif;
        min-width: 100%;
        background-color: white; /* Background putih */
        border: 2px solid black; /* Border box luar */
    }
    .styled-table th, .styled-table td {
        border: 1px solid black; /* Border tiap sel */
        padding: 8px;
        text-align: left;
    }
    .styled-table th {
        background-color: #f2f2f2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tampilkan tabel dalam HTML agar styling berlaku
st.markdown(df_filtered.to_html(index=False, classes="styled-table"), unsafe_allow_html=True)
