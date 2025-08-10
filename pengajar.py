import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Pengajar Nilai Tertinggi", layout="wide")

# CSS untuk background putih dan tabel border
st.markdown("""
    <style>
    .main {
        background-color: white;
        color: black;
    }
    table.styled-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 16px;
        min-width: 400px;
        border: 1px solid #dddddd;
    }
    table.styled-table th, table.styled-table td {
        border: 1px solid #dddddd;
        padding: 8px 12px;
        text-align: left;
        color: black;
        background-color: white;
    }
    table.styled-table th {
        background-color: #f2f2f2;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Hilangkan kolom sumber sheet jika ada
if "Sumber Sheet" in df.columns:
    df = df.drop(columns=["Sumber Sheet"])

# Dropdown 1: Nama Diklat (semua muncul)
pilihan_diklat = st.selectbox("Pilih Nama Diklat", sorted(df["Nama Diklat"].unique().tolist()))

# Filter berdasarkan diklat
df_filtered = df[df["Nama Diklat"] == pilihan_diklat]

# Dropdown 2: Nama Unit (hanya yang ada di diklat terpilih)
pilihan_unit = st.selectbox("Pilih Nama Unit", sorted(df_filtered["Nama Unit"].unique().tolist()))
df_filtered = df_filtered[df_filtered["Nama Unit"] == pilihan_unit]

# Dropdown 3: Mata Ajar (hanya yang ada di unit terpilih)
pilihan_mata = st.selectbox("Pilih Mata Ajar", sorted(df_filtered["Mata Ajar"].unique().tolist()))
df_filtered = df_filtered[df_filtered["Mata Ajar"] == pilihan_mata]

# Urutkan berdasarkan nilai tertinggi
if "Nilai" in df_filtered.columns:
    df_filtered = df_filtered.sort_values(by="Nilai", ascending=False)

# Tampilkan tabel dengan border
html_table = df_filtered.to_html(classes="styled-table", index=False)
st.markdown(html_table, unsafe_allow_html=True)
