import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Nilai Pengajar", layout="wide")

# CSS untuk background putih
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

st.title("📊 Dashboard Nilai Pengajar Tertinggi")

# Baca file Excel langsung dari nama file
file_path = "Penilaian Gabung dengan Nama Unit.xlsx"
df = pd.read_excel(file_path)

# Pastikan kolom yang dibutuhkan ada
required_columns = ["Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]
if not all(col in df.columns for col in required_columns):
    st.error("Kolom yang diperlukan tidak ditemukan di file.")
else:
    # Filter nilai maksimal 5
    df = df[df["Rata-Rata"] <= 5]

    # Dropdown filter
    nama_diklat = st.selectbox("Pilih Nama Diklat", ["Semua"] + sorted(df["Nama Diklat"].dropna().unique().tolist()))
    nama_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df["Nama Unit"].dropna().unique().tolist()))
    mata_ajar = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df["Mata Ajar"].dropna().unique().tolist()))

    # Filter data
    filtered_df = df.copy()
    if nama_diklat != "Semua":
        filtered_df = filtered_df[filtered_df["Nama Diklat"] == nama_diklat]
    if nama_unit != "Semua":
        filtered_df = filtered_df[filtered_df["Nama Unit"] == nama_unit]
    if mata_ajar != "Semua":
        filtered_df = filtered_df[filtered_df["Mata Ajar"] == mata_ajar]

    # Urutkan berdasarkan Rata-Rata tertinggi
    filtered_df = filtered_df.sort_values(by="Rata-Rata", ascending=False)

    # Pilih kolom yang ditampilkan
    show_df = filtered_df[["Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]]

    # Tampilkan tabel
    st.dataframe(show_df, use_container_width=True)

    # Download hasil
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    st.download_button(
        label="📥 Unduh Hasil sebagai Excel",
        data=convert_df(show_df),
        file_name="nilai_pengajar_tertinggi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
