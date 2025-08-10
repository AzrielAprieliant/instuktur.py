import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="📊 Dashboard Instruktur", layout="wide", initial_sidebar_state="collapsed")
st.title("📊 Dashboard Penilaian Instruktur")

# Load data
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Dropdown filter (tanpa "Semua")
unit_list = sorted(df["Nama Unit"].dropna().unique())
mata_ajar_list = sorted(df["Mata Ajar"].dropna().unique())

unit = st.selectbox("Pilih Nama Unit", unit_list)
mata_ajar = st.selectbox("Pilih Mata Ajar", mata_ajar_list)

# Filter data sesuai pilihan (tanpa filter tahun)
df_filtered = df[
    (df["Nama Unit"] == unit) &
    (df["Mata Ajar"] == mata_ajar)
]

# CSS styling tabel (warna putih + border hitam + scroll)
table_style = """
<style>
.table-container {
    max-height: 500px; 
    overflow-y: auto;
    border: 2px solid black;
    background-color: white;
}
.styled-table {
    border-collapse: collapse;
    font-size: 16px;
    font-family: sans-serif;
    width: 100%;
    color: black;
    background-color: white;
}
.styled-table th, .styled-table td {
    border: 1px solid black;
    padding: 8px 12px;
    text-align: left;
}
.styled-table th {
    background-color: white;
    color: black;
}
</style>
"""

# Tampilkan tabel
if not df_filtered.empty:
    html_table = df_filtered.to_html(classes="styled-table", index=False)
    st.markdown(table_style + f"<div class='table-container'>{html_table}</div>", unsafe_allow_html=True)
else:
    st.warning("⚠ Tidak ada data untuk filter yang dipilih.")
