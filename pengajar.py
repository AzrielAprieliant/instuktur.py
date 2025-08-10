import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="📊 Dashboard Instruktur", layout="wide", initial_sidebar_state="collapsed")
st.title("📊 Dashboard Penilaian Instruktur")

# Load data
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# ===== DROPDOWN 1 - Nama Diklat =====
diklat_list = sorted(df["Nama Diklat"].dropna().unique())
diklat = st.selectbox("Pilih Nama Diklat", diklat_list)

# ===== DROPDOWN 2 - Nama Unit (filter dari diklat) =====
unit_list = sorted(df[df["Nama Diklat"] == diklat]["Nama Unit"].dropna().unique())
unit = st.selectbox("Pilih Nama Unit", unit_list)

# ===== DROPDOWN 3 - Mata Ajar (filter dari diklat & unit) =====
mata_ajar_list = sorted(df[(df["Nama Diklat"] == diklat) & (df["Nama Unit"] == unit)]["Mata Ajar"].dropna().unique())
mata_ajar = st.selectbox("Pilih Mata Ajar", mata_ajar_list)

# ===== Filter Data =====
df_filtered = df[
    (df["Nama Diklat"] == diklat) &
    (df["Nama Unit"] == unit) &
    (df["Mata Ajar"] == mata_ajar)
]

# ===== CSS Styling Tabel =====
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
    background-color: white;
    color: black;
}
.styled-table th, .styled-table td {
    border: 1px solid black;
    padding: 8px 12px;
    text-align: left;
    background-color: white;
    color: black;
}
.styled-table th {
    background-color: white;
    color: black;
}
</style>
"""

# ===== Tampilkan Tabel =====
if not df_filtered.empty:
    html_table = df_filtered.to_html(classes="styled-table", index=False)
    st.markdown(table_style + f"<div class='table-container'>{html_table}</div>", unsafe_allow_html=True)
else:
    st.warning("⚠ Tidak ada data untuk filter yang dipilih.")
