import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman (warna putih)
st.set_page_config(page_title="Dashboard Penilaian", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }
    .dataframe-box {
        border: 2px solid #ccc;
        padding: 10px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Dashboard Penilaian Instruktur")

# Load data
df = pd.read_excel("Penilaian Gabung dengan Nama Unit.xlsx")

# Pastikan kolom Tahun ada
if "Tahun" not in df.columns:
    for col in df.columns:
        if "tgl" in col.lower() or "tanggal" in col.lower():
            df["Tahun"] = pd.to_datetime(df[col]).dt.year
            break

# Dropdown filter (tanpa opsi "Semua")
diklat_list = sorted(df["Nama Diklat"].dropna().unique().tolist())
unit_list = sorted(df["Nama Unit"].dropna().unique().tolist())
mata_ajar_list = sorted(df["Mata Ajar"].dropna().unique().tolist())

selected_diklat = st.selectbox("Pilih Nama Diklat", diklat_list)
selected_unit = st.selectbox("Pilih Nama Unit", unit_list)
selected_mata_ajar = st.selectbox("Pilih Mata Ajar", mata_ajar_list)

# Filter data
filtered_df = df[
    (df["Nama Diklat"] == selected_diklat) &
    (df["Nama Unit"] == selected_unit) &
    (df["Mata Ajar"] == selected_mata_ajar)
]

# Hapus kolom tidak perlu
for col in ["Kelas", "Sumber Sheet"]:
    if col in filtered_df.columns:
        filtered_df = filtered_df.drop(columns=[col])

# Urutkan berdasarkan nilai tertinggi
if "Rata-Rata" in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by="Rata-Rata", ascending=False)

# Tambahkan kolom Ranking
filtered_df.insert(0, "Ranking", range(1, len(filtered_df) + 1))

# Atur urutan kolom
kolom_urut = ["Ranking", "Instruktur", "Nama Diklat", "Mata Ajar", "Nama Unit", "Tahun", "Rata-Rata"]
filtered_df = filtered_df[[kol for kol in kolom_urut if kol in filtered_df.columns]]

# Reset index
filtered_df.reset_index(drop=True, inplace=True)

# Tampilkan tabel dengan border box
st.subheader("📋 Data Instruktur Nilai Tertinggi")
st.markdown('<div class="dataframe-box">', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================== Visualisasi ==================
if not filtered_df.empty:
    # Bar Chart
    fig_bar = px.bar(
        filtered_df,
        x="Instruktur",
        y="Rata-Rata",
        title="📊 Nilai Rata-Rata Per Instruktur",
        color="Rata-Rata",
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie Chart
    fig_pie = px.pie(
        filtered_df,
        names="Instruktur",
        values="Rata-Rata",
        title="📊 Persentase Nilai Rata-Rata"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")
