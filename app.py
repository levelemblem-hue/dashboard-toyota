%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("penjualan_mobil_toyota.csv")
df["Bulan"] = pd.to_datetime(df["Bulan"])
df["Tahun"] = df["Bulan"].dt.year
df["BulanNama"] = df["Bulan"].dt.strftime("%B")

st.set_page_config(page_title="Dashboard Penjualan Toyota", layout="wide")

st.title("📊 Dashboard Penjualan Mobil Toyota — Versi Upgrade")

# ----------------------------
# SIDEBAR FILTER
# ----------------------------
st.sidebar.header("🔎 Filter Data")

# Filter Tahun
tahun_list = sorted(df["Tahun"].unique())
pilih_tahun = st.sidebar.selectbox("Pilih Tahun", ["Semua"] + list(tahun_list))

# Filter Bulan
bulan_list = df["BulanNama"].unique()
pilih_bulan = st.sidebar.multiselect("Pilih Bulan", bulan_list)

df_filtered = df.copy()

if pilih_tahun != "Semua":
    df_filtered = df_filtered[df_filtered["Tahun"] == pilih_tahun]

if len(pilih_bulan) > 0:
    df_filtered = df_filtered[df_filtered["BulanNama"].isin(pilih_bulan)]

# ----------------------------
# KPI CARDS
# ----------------------------
st.subheader("📌 Ringkasan Penjualan")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Penjualan", f"{df_filtered['Penjualan'].sum():,}")
col2.metric("Rata-rata Penjualan", f"{df_filtered['Penjualan'].mean():,.2f}")
col3.metric("Penjualan Tertinggi", f"{df_filtered['Penjualan'].max():,}")
col4.metric("Penjualan Terendah", f"{df_filtered['Penjualan'].min():,}")

# ----------------------------
# VISUALISASI
# ----------------------------

# 1. Line Chart
st.subheader("📈 Tren Penjualan (Line Chart)")
fig_line = px.line(df_filtered, x="Bulan", y="Penjualan",
                   markers=True, title="Trend Penjualan Toyota")
st.plotly_chart(fig_line, use_container_width=True)

# 2. Bar Chart
st.subheader("📊 Penjualan per Bulan (Bar Chart)")
fig_bar = px.bar(df_filtered, x="Bulan", y="Penjualan",
                 title="Bar Chart Penjualan Toyota")
st.plotly_chart(fig_bar, use_container_width=True)

# 3. Area Chart
st.subheader("📉 Area Chart Penjualan")
fig_area = px.area(df_filtered, x="Bulan", y="Penjualan",
                   title="Area Chart Penjualan Toyota")
st.plotly_chart(fig_area, use_container_width=True)

# 4. Pie Chart — persentase kontribusi per bulan
st.subheader("🥧 Persentase Kontribusi Penjualan per Bulan")
fig_pie = px.pie(df_filtered, names="BulanNama", values="Penjualan",
                 title="Kontribusi Penjualan Bulanan (%)")
st.plotly_chart(fig_pie, use_container_width=True)
