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

file_path = "Penilaian Gabung dengan Nama Unit.xlsx"
df = pd.read_excel(file_path)

required_columns = ["Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]
if not all(col in df.columns for col in required_columns):
    st.error("Kolom yang diperlukan tidak ditemukan di file.")
else:
    df = df[df["Rata-Rata"] <= 5]

    
    nama_diklat = st.selectbox("Pilih Nama Diklat", sorted(df["Nama Diklat"].dropna().unique().tolist()))

    df_diklat = df[df["Nama Diklat"] == nama_diklat]

    nama_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df_diklat["Nama Unit"].dropna().unique().tolist()))

    mata_ajar = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df_diklat["Mata Ajar"].dropna().unique().tolist()))

    filtered_df = df_diklat.copy()
    if nama_unit != "Semua":
        filtered_df = filtered_df[filtered_df["Nama Unit"] == nama_unit]
    if mata_ajar != "Semua":
        filtered_df = filtered_df[filtered_df["Mata Ajar"] == mata_ajar]

    filtered_df = filtered_df.sort_values(by="Rata-Rata", ascending=False).reset_index(drop=True)
    filtered_df.insert(0, "Ranking", range(1, len(filtered_df) + 1))

    show_df = filtered_df[["Ranking", "Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]]


    st.subheader("🏆 Pengajar Nilai Tertinggi")
    
    # Misalnya show_df sudah jadi
    show_df = show_df.reset_index(drop=True)  # Hilangkan index Pandas

    # Kalau ada kolom 'index' atau sisa hasil merge, drop juga
    if 'index' in show_df.columns:
    show_df = show_df.drop(columns=['index'])

    # Tampilkan langsung
    st.dataframe(show_df)


    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    st.download_button(
        label="📥 Unduh Hasil sebagai Excel",
        data=convert_df(show_df),
        file_name="nilai_pengajar_tertinggi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
