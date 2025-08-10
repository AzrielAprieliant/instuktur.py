import streamlit as st
import pandas as pd

# Konfigurasi halaman (warna putih)
st.set_page_config(page_title="Dashboard Penilaian", layout="wide")

table_style = """
<style>
.styled-table {
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 16px;
    font-family: sans-serif;
    border: 2px solid black;
    background-color: white;
}
.styled-table th, .styled-table td {
    border: 1px solid black;
    padding: 8px 12px;
    text-align: left;
    color: black;
}
.styled-table th {
    background-color: white; /* Header putih */
}
</style>
"""

# Convert DataFrame ke HTML + apply class CSS
html_table = df.to_html(classes="styled-table", index=False)

# Tampilkan
st.markdown(table_style + html_table, unsafe_allow_html=True)
st.title("📊 Dashboard Penilaian Instruktur")

# Load data Excel
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Pastikan kolom Tahun ada
if "Tahun" not in df.columns:
    for col in df.columns:
        if "tgl" in col.lower() or "tanggal" in col.lower():
            df["Tahun"] = pd.to_datetime(df[col]).dt.year
            break

# Dropdown filter
diklat_list = sorted(df["Nama Diklat"].dropna().unique().tolist())  # tanpa "Semua"
unit_list = ["Semua"] + sorted(df["Nama Unit"].dropna().unique().tolist())
mata_ajar_list = ["Semua"] + sorted(df["Mata Ajar"].dropna().unique().tolist())

selected_diklat = st.selectbox("Pilih Nama Diklat", diklat_list)
selected_unit = st.selectbox("Pilih Nama Unit", unit_list)
selected_mata_ajar = st.selectbox("Pilih Mata Ajar", mata_ajar_list)

# Filter data
filtered_df = df[df["Nama Diklat"] == selected_diklat]

if selected_unit != "Semua":
    filtered_df = filtered_df[filtered_df["Nama Unit"] == selected_unit]
if selected_mata_ajar != "Semua":
    filtered_df = filtered_df[filtered_df["Mata Ajar"] == selected_mata_ajar]

# Hapus kolom yang tidak diperlukan
for col in ["Kelas", "Sumber Sheet"]:
    if col in filtered_df.columns:
        filtered_df = filtered_df.drop(columns=[col])

# Urutkan berdasarkan nilai tertinggi (kolom "Rata-Rata")
if "Rata-Rata" in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by="Rata-Rata", ascending=False)

# Tambahkan kolom Ranking
filtered_df.insert(0, "Ranking", range(1, len(filtered_df) + 1))

# Atur urutan kolom
kolom_urut = ["Ranking", "Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]
filtered_df = filtered_df[[kol for kol in kolom_urut if kol in filtered_df.columns]]

# Reset index
filtered_df.reset_index(drop=True, inplace=True)

# Judul tabel
st.subheader("📋 Data Instruktur Nilai Tertinggi")

# Tampilkan tabel
st.dataframe(filtered_df)
