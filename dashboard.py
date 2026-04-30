import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Dashboard Kualitas Udara Beijing", layout="wide")


BASE_DIR = Path(__file__).parent


@st.cache_data
def load_all_data():
  
    def read_csv(file_name, station_name):
        file_path = BASE_DIR / file_name
        if file_path.exists():
            df_temp = pd.read_csv(file_path)
            df_temp['Station_Name'] = station_name
            return df_temp
        else:
            st.error(f"File {file_name} tidak ditemukan!")
            return pd.DataFrame()

    df_a = read_csv("Aq_Ao_clean.csv", "Aotizhongxin")

    df_b = read_csv("Aq_Ch_clean.csv", "Changping")

    if not df_a.empty or not df_b.empty:
        df_all = pd.concat([df_a, df_b], ignore_index=True)

        df_all['date'] = pd.to_datetime(df_all[['year', 'month', 'day']])
        return df_all
    else:
        st.stop()


df = load_all_data()


st.sidebar.header("Filter Dashboard")

list_tahun = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun", list_tahun)


df_filtered = df[df['year'] == selected_year]


st.title(" Dashboard Analisis Kualitas Udara")
st.markdown(f"Menampilkan analisis untuk tahun **{selected_year}**")


st.header("1. Dampak Hujan terhadap Konsentrasi Polutan")
st.subheader("Apakah saat hujan (RAIN > 1) udara menjadi aman (Sesuai Batas WHO)?")

df_hujan = df_filtered[df_filtered['RAIN'] > 1]

if not df_hujan.empty:

    hujan_monthly = df_hujan.groupby('month')[['PM2.5', 'PM10']].mean()

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(hujan_monthly.index, hujan_monthly['PM2.5'], marker='o', label='Rata-rata PM2.5', color='royalblue')
    ax1.plot(hujan_monthly.index, hujan_monthly['PM10'], marker='s', label='Rata-rata PM10', color='seagreen')


    ax1.axhline(15, color='red', linestyle='--', label='Batas Aman PM2.5 WHO (15)')
    ax1.axhline(45, color='orange', linestyle='--', label='Batas Aman PM10 WHO (45)')

    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("Konsentrasi (µg/m³)")
    ax1.set_xticks(range(1, 13))
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)
    

st.divider()


st.header("2. Perbandingan Polusi Ekstrem Antar Stasiun")
st.subheader("Perbandingan Nilai PM2.5 Tertinggi (Max) Per Tahun")


df_max_yearly = df.groupby(['year', 'Station_Name'])['PM2.5'].max().reset_index()


if not df_max_yearly.empty:

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_max_yearly, x='year', y='PM2.5', hue='Station_Name', ax=ax2, palette='Set2')


    ax2.set_title("Nilai PM2.5 Tertinggi (Maksimum) per Tahun", fontsize=14)
    ax2.set_xlabel("Tahun", fontsize=12)
    ax2.set_ylabel("Nilai Max PM2.5 (µg/m³)", fontsize=12)
    ax2.legend(title="Lokasi Stasiun")
    ax2.grid(axis='y', linestyle='--', alpha=0.7)


    st.pyplot(fig2)
    
