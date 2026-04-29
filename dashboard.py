import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Dashboard Kualitas Udara", layout="wide")

@st.cache_data
def load_data(file_name, station_name):
    df = pd.read_csv(file_name)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    df['Station'] = station_name
    return df

BASE_DIR = Path(__file__).resolve().parent

df_A = load_data(BASE_DIR / "Aq_Ao_clean.csv", "Aotizhongxin")
df_B = load_data(BASE_DIR / "Aq_Ch_clean.csv", "Changping")

df_all = pd.concat([df_A, df_B])

st.title("📊 Dashboard Komparasi Kualitas Udara")
st.markdown("Membandingkan Polusi PM2.5 antara Stasiun Aotizhongxin dan Stasiun Changping")

st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", df_all['year'].unique())


df_filtered = df_all[df_all['year'] == selected_year]

st.subheader(f"Ringkasan Polusi Tahun {selected_year}")
col1, col2 = st.columns(2)

mean_A = df_filtered[df_filtered['Station'] == 'Aotizhongxin']['PM2.5'].mean()
mean_B = df_filtered[df_filtered['Station'] == 'Changping']['PM2.5'].mean()

with col1:
    st.metric("Rata-rata PM2.5 (Aotizhongxin)", f"{mean_A:.2f} µg/m³")
with col2:
    st.metric("Rata-rata PM2.5 (Changping)", f"{mean_B:.2f} µg/m³")

st.divider()


st.subheader(f"Perbandingan Tren Polusi PM2.5 per Bulan ({selected_year})")


monthly_trend = df_filtered.groupby(['month', 'Station'])['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly_trend, x='month', y='PM2.5', hue='Station', marker='o', ax=ax, palette=['royalblue', 'orange'])
ax.axhline(15, color='red', linestyle='--', alpha=0.5, label='Batas Aman WHO (15)')


ax.set_xlabel("Bulan")
ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
ax.set_xticks(range(1, 13)) 
ax.legend()


st.pyplot(fig)