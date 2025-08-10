import streamlit as st
import pandas as pd

# Konfigurasi halaman (warna putih)
st.set_page_config(page_title="Dashboard Penilaian", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# Hapus kolom 'Kelas' jika ada
if "Kelas" in filtered_df.columns:
    filtered_df = filtered_df.drop(columns=["Kelas", "Sumber Sheet"])

# Urutkan berdasarkan nilai tertinggi (asumsi kolom 'Nilai' ada)
if "Nilai" in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by="Nilai", ascending=False)

# Reset index agar rapi
filtered_df.reset_index(drop=True, inplace=True)

# Tampilkan hasil
st.dataframe(filtered_df)
