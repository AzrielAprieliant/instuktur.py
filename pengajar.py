import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="📊 Dashboard Penilaian Instruktur", layout="wide", initial_sidebar_state="collapsed")

# CSS untuk memperlebar dropdown
st.markdown("""
<style>
.stSelectbox [data-baseweb="select"] {
    width: 300px !important;
}
</style>
""", unsafe_allow_html=True)

# Judul
st.title("📊 Dashboard Penilaian Instruktur")

# Load data
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Filter Tahun (dengan 'Semua')
tahun_options = ["Semua"] + sorted(df["Tahun"].unique().tolist())
tahun_filter = st.selectbox("Pilih Tahun:", tahun_options)

# Filter Nama Diklat (tanpa 'Semua')
diklat_options = sorted(df["Nama Diklat"].unique().tolist())
diklat_filter = st.selectbox("Pilih Nama Diklat:", diklat_options)

# Filter DataFrame
df_filtered = df.copy()
if tahun_filter != "Semua":
    df_filtered = df_filtered[df_filtered["Tahun"] == tahun_filter]

df_filtered = df_filtered[df_filtered["Nama Diklat"] == diklat_filter]

# Tampilkan data
st.dataframe(df_filtered)

# Hitung nilai rata-rata dan peringkat
ranking = df_filtered.groupby("Instruktur", as_index=False)["Rata-Rata"].mean()
ranking["Peringkat"] = ranking["Rata-Rata"].rank(ascending=False, method="min").astype(int)
ranking = ranking.sort_values(by="Peringkat")

# Tampilkan ranking
st.subheader("🏆 Peringkat Instruktur")
st.dataframe(ranking)
