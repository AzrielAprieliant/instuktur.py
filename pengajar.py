import streamlit as st
import pandas as pd
import plotly.express as px
import traceback

st.set_page_config(page_title="Dashboard Instruktur", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* Pastikan background putih */
html, body, [data-testid="stAppViewContainer"] {
    background-color: white !important;
    color: black !important;
}

/* Sidebar putih */
section[data-testid="stSidebar"] {
    background-color: white !important;
}

/* Selectbox: lebar & tinggi lebih kecil */
div[data-testid="stSelectbox"] {
    width: 300px !important;
}
div[data-baseweb="select"] > div {
    min-height: 30px !important;
    padding: 4px 8px !important;
    font-size: 13px !important;
    background-color: #ffffff !important;
    color: #003366 !important;
    border-radius: 6px !important;
    border: 1px solid #d0d7df !important;
}

/* Label */
label {
    font-size: 13px !important;
    color: #003366 !important;
}

/* Dataframe supaya responsif */
[data-testid="stDataFrame"] table {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# Fungsi utama
# ===============================
def main():
    path = "Penilaian Gabung dengan Nama Unit.xlsx"

    # Load data dengan penanganan error
    try:
        df = pd.read_excel(path)
    except FileNotFoundError:
        st.error(f"File Excel tidak ditemukan: `{path}`. Pastikan file ada di folder yang sama dengan app.py")
        return
    except Exception:
        st.error("Gagal membaca file Excel. Detail error:")
        st.text(traceback.format_exc())
        return

    # Cek kolom yang dibutuhkan
    required_cols = ["Nama Diklat", "Nama Unit", "Mata Ajar", "Instruktur", "Tahun", "Rata-Rata"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Dataframe tidak memiliki kolom yang dibutuhkan: {missing}")
        st.write("Kolom yang tersedia:", list(df.columns))
        return

    # Bersihkan dan ubah tipe
    df["Rata-Rata"] = pd.to_numeric(df["Rata-Rata"], errors="coerce")
    # Jika ada nilai di atas 100 (format persen?), koreksi seperti sebelumnya
    df.loc[df["Rata-Rata"] > 100, "Rata-Rata"] = df["Rata-Rata"] / 10000
    df["Rata-Rata"] = df["Rata-Rata"].round(2)

    st.title("📊 Dashboard Penilaian Instruktur")

    # --- Filter: Nama Diklat ---
    nama_diklat_opts = sorted(df["Nama Diklat"].dropna().unique().tolist())
    nama_diklat_opts = ["Semua"] + nama_diklat_opts if nama_diklat_opts else ["Semua"]
    nama_diklat = st.selectbox("📘 Pilih Nama Diklat", nama_diklat_opts, index=0)
    df_diklat = df if nama_diklat == "Semua" else df[df["Nama Diklat"] == nama_diklat]

    # --- Filter: Nama Unit ---
    unit_opts = sorted(df_diklat["Nama Unit"].dropna().unique().tolist())
    unit_opts = ["Semua"] + unit_opts if unit_opts else ["Semua"]
    unit_kerja = st.selectbox("🏢 Pilih Nama Unit", unit_opts, index=0)
    df_unit = df_diklat if unit_kerja == "Semua" else df_diklat[df_diklat["Nama Unit"] == unit_kerja]

    # --- Filter: Mata Ajar ---
    mata_ajar_opts = sorted(df_unit["Mata Ajar"].dropna().unique().tolist())
    if not mata_ajar_opts:
        # Kalau kosong, beri peringatan dan gunakan seluruh df_unit
        st.warning("Tidak ada opsi 'Mata Ajar' untuk kombinasi filter ini — menampilkan semua Mata Ajar.")
        filtered_df = df_unit.copy()
    else:
        mata_ajar = st.selectbox("📖 Pilih Mata Ajar", ["Semua"] + mata_ajar_opts, index=0)
        filtered_df = df_unit if mata_ajar == "Semua" else df_unit[df_unit["Mata Ajar"] == mata_ajar]

    # Jika setelah filter tidak ada data, tampilkan pesan dan stop
    if filtered_df.empty:
        st.warning("⚠️ Tidak ada data setelah filter. Coba ubah kombinasi filter.")
        return

    # --- Buat ranking top instruktur (satu baris per instruktur) ---
    top_instruktur = (
        filtered_df.sort_values(by="Rata-Rata", ascending=False)
        .groupby("Instruktur", as_index=False)
        .first()
        .sort_values(by="Rata-Rata", ascending=False)
        .reset_index(drop=True)
    )
    # Tambah kolom peringkat
    top_instruktur.index += 1
    top_instruktur.insert(0, "Peringkat", top_instruktur.index)

    # Tampilkan tabel
    st.markdown("### 📋 Tabel Peringkat Instruktur")
    st.dataframe(
        top_instruktur[["Peringkat", "Instruktur", "Mata Ajar", "Nama Diklat", "Nama Unit", "Tahun", "Rata-Rata"]],
        use_container_width=True,
        height=450
    )

    # Bar chart
    st.markdown("### 📈 Grafik Peringkat Instruktur (Bar Chart)")
    try:
        fig_bar = px.bar(
            top_instruktur,
            x="Instruktur",
            y="Rata-Rata",
            color="Rata-Rata",
            text="Rata-Rata",
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(xaxis_title=None, yaxis_title="Nilai Rata-Rata", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)
    except Exception:
        st.error("Gagal membuat bar chart. Detail:")
        st.text(traceback.format_exc())

    # Box plot (distribusi)
    st.markdown("### 📦 Distribusi Nilai Rata-Rata (Box Plot)")
    try:
        fig_box = px.box(
            filtered_df,
            y="Rata-Rata",
            points="all",
            title="Distribusi Nilai Rata-Rata Instruktur"
        )
        fig_box.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_box, use_container_width=True)
    except Exception:
        st.error("Gagal membuat box plot. Detail:")
        st.text(traceback.format_exc())

    # Trend per tahun (jika tersedia lebih dari 1 tahun)
    if df["Tahun"].nunique() > 1:
        st.markdown("### 🗓️ Tren Nilai Rata-Rata per Tahun")
        try:
            df_trend = df.groupby("Tahun")["Rata-Rata"].mean().reset_index()
            fig_line = px.line(df_trend, x="Tahun", y="Rata-Rata", markers=True, title="Rata-Rata Instruktur per Tahun")
            fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_line, use_container_width=True)
        except Exception:
            st.error("Gagal membuat line chart. Detail:")
            st.text(traceback.format_exc())

# ===============================
# Jalankan aplikasi dalam blok try/except
# supaya kalau ada error ditampilkan dengan jelas di UI
# ===============================
if __name__ == "__main__":
    try:
        main()
    except Exception:
        st.error("Terjadi error tak terduga. Detail:")
        st.text(traceback.format_exc())
