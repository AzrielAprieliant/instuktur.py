import streamlit as st
import pandas as pd


st.set_page_config(page_title="Dashboard Instruktur", layout="wide", initial_sidebar_state="collapsed")
st.title("📊 Dashboard Penilaian Instruktur")


df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")


df = df.rename(columns={
    "Nama": "Nama",
    "Nama Diklat": "Nama Diklat",
    "Mata Ajar": "Mata Ajar",
    "Nama Unit": "Nama Unit",
    "Tahun": "Tahun",
    "Rata-Rata": "Nilai"
})

# Perbaiki nilai agar tidak ada angka aneh
df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce")
df = df[df["Nilai"].between(0, 5)] 


pilihan_diklat = st.selectbox("Pilih Nama Diklat", ["Semua"] + sorted(df["Nama Diklat"].unique().tolist()))


if pilihan_diklat != "Semua":
    df_filtered = df[df["Nama Diklat"] == pilihan_diklat]
    pilihan_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df_filtered["Nama Unit"].unique().tolist()))
    pilihan_mata = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df_filtered["Mata Ajar"].unique().tolist()))
else:
    df_filtered = df.copy()
    pilihan_unit = st.selectbox("Pilih Nama Unit", ["Semua"] + sorted(df["Nama Unit"].unique().tolist()))
    pilihan_mata = st.selectbox("Pilih Mata Ajar", ["Semua"] + sorted(df["Mata Ajar"].unique().tolist()))


if pilihan_unit != "Semua":
    df_filtered = df_filtered[df_filtered["Nama Unit"] == pilihan_unit]


if pilihan_mata != "Semua":
    df_filtered = df_filtered[df_filtered["Mata Ajar"] == pilihan_mata]


df_filtered = df_filtered.sort_values(by="Nilai", ascending=False)
df_filtered.insert(0, "Ranking", range(1, len(df_filtered) + 1))


df_filtered = df_filtered[["Ranking", "Nama", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Nilai"]]


st.subheader("📋 Data Instruktur Nilai Tertinggi")


st.markdown("""
<style>
table {
    border-collapse: collapse;
    width: 100%;
    border: 2px solid white;
}
th, td {
    border: 1px solid white;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

st.dataframe(df_filtered, use_container_width=True)
