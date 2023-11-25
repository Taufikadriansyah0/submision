import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv("dashboard/dataDay.csv")
hour_df = pd.read_csv("dashboard/dataHour.csv")


# Fungsi untuk membuat visualisasi per jam
def plot_hourly_counts(df):
    total_counts_per_hour = hour_df.groupby('hr')['cnt'].sum()
# Menampilkan jam dengan total peminjaman tertinggi
    most_used_hour = total_counts_per_hour.idxmax()
    print(f"Jam dengan Peminjaman Sepeda Tertinggi: {most_used_hour}")
# Membuat Bar Chart tanpa menggunakan 'palette' dan menyertakan 'legend=False'
    fig = plt.figure(figsize=(12, 6))
    sns.barplot(x=total_counts_per_hour.index, y=total_counts_per_hour.values, color='skyblue')
    plt.title('Total Peminjaman Sepeda per Jam dalam Sehari selama 2 tahun')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Total Peminjaman')
    st.pyplot(fig)

# Fungsi untuk membuat visualisasi musim
def plot_seasonal_counts(df):
    st.header('Data musim')
    season_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    df['season_label'] = df['season'].map(season_mapping)
    total_counts_per_season = df.groupby('season_label')['cnt'].sum()

    plt.figure(figsize=(8, 8))
    plt.pie(total_counts_per_season, labels=total_counts_per_season.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('viridis'))
    plt.title('Persentase Peminjaman Sepeda per Musim')
    st.pyplot(plt)

# Fungsi untuk membuat visualisasi harian dan bulanan
def plot_daily_and_monthly_counts(df):
    df['dteday'] = pd.to_datetime(df['dteday'])

    # Plot tren harian
    fig = plt.figure(figsize=(12, 6))
    daily_counts = df.groupby('dteday')['cnt'].sum()
    daily_counts.plot(linewidth=0.8)
    plt.title('Tren Harian Penggunaan Sepeda')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Peminjaman')
    st.pyplot(fig)

    # Plot tren bulanan
    st.header('Data Bulanan')
    fig = plt.figure(figsize=(12, 6))
    monthly_counts = df.groupby(['year', 'month'])['cnt'].sum()
    monthly_counts.plot(kind='bar', color='skyblue')
    plt.title('Tren Bulanan Penggunaan Sepeda')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Peminjaman')
    st.pyplot(fig)

# Sidebar untuk memilih dataset dan tanggal
selected_dataset = st.sidebar.radio("Pilih Dataset", ['day_df', 'hour_df'])
start_date = st.sidebar.date_input("Pilih Tanggal Awal", pd.to_datetime("2011-01-01"))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", pd.to_datetime("2012-12-31"))


# Filter dataset berdasarkan tanggal
if selected_dataset == 'day_df':
    day_df['dteday'] = pd.to_datetime(day_df['dteday']).dt.date  # Mengubah datetime menjadi date
    filtered_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
    st.header('Visualisasi Data Harian')
    plot_daily_and_monthly_counts(filtered_df)
    plot_seasonal_counts(filtered_df)
else:
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday']).dt.date  # Mengubah datetime menjadi date
    filtered_df = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]
    st.header('Visualisasi Data Per Jam')
    plot_hourly_counts(filtered_df)

