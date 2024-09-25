import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load Data
day_df = pd.read_csv("data.csv")
day_df.loc[day_df.weekday == 0, 'holiday'] = 1
day_df.loc[day_df.weekday == 6, 'holiday'] = 1


# Functions for grouping data
def get_weather_data(df):
    """Group data by weather situation and sum the bike rentals."""
    weather_df = df.groupby(by="weathersit").agg({"cnt": ["sum"]})
    weather_df = weather_df.reindex([1, 2, 3, 4], fill_value=0).reset_index()
    weather_df.columns = ['weathersit', 'cnt_sum']
    return weather_df


def get_weekday_data(df):
    """Group data by weekday and get the mean bike rentals."""
    weekday_df = df.groupby(by="weekday").agg({"cnt": ["mean"]}).reset_index()
    weekday_df.columns = ['weekday', 'mean']
    return weekday_df


def get_working_holiday_data(df):
    """Group data by working day and holiday status and sum the bike rentals."""
    holiday_df = df.groupby(['workingday', 'holiday']).agg({"cnt": ["sum"]}).reset_index()
    holiday_df.columns = ['workingday', 'holiday', 'cnt_sum']
    workingday_cnt = holiday_df[holiday_df['workingday'] == 1]['cnt_sum'].sum()
    holiday_cnt = holiday_df[holiday_df['workingday'] == 0]['cnt_sum'].sum()
    return workingday_cnt, holiday_cnt


# Streamlit App
st.title("Bike Rental Report 🚲")

tab1, tab2 = st.tabs(["Berdasarkan cuaca", "Berdasarkan Hari"])

with tab1:
    st.header("Analisis Berdasarkan Cuaca ☁")

    # Sidebar filter for weather codes
    st.sidebar.header("Filter Berdasarkan Kode Cuaca")
    weather_1 = st.sidebar.checkbox('Cuaca 1', value=True)
    weather_2 = st.sidebar.checkbox('Cuaca 2', value=True)
    weather_3 = st.sidebar.checkbox('Cuaca 3', value=True)
    weather_4 = st.sidebar.checkbox('Cuaca 4', value=True)

    # Get weather data
    weather_df = get_weather_data(day_df)

    # Filter the weather data based on the checkbox selections
    selected_weather = []
    if weather_1:
        selected_weather.append(1)
    if weather_2:
        selected_weather.append(2)
    if weather_3:
        selected_weather.append(3)
    if weather_4:
        selected_weather.append(4)

    # Filter the dataframe to only include the selected weather codes
    filtered_weather_df = weather_df[weather_df['weathersit'].isin(selected_weather)]

    # Plot filtered weather data
    plt.figure(figsize=(10, 5))
    colors_ = ['#76c7c0', '#ffcc00', '#ff6f61', '#c44d58']
    plt.barh(
        y="weathersit",
        width="cnt_sum",
        data=filtered_weather_df.sort_values(by="cnt_sum", ascending=False),
        color=colors_[:len(selected_weather)]
    )
    plt.title("Jumlah rental sepeda berdasarkan cuaca", loc="center", fontsize=15)
    plt.xlabel("Total Rentals (dalam juta)")
    plt.ylabel("Kode cuaca")
    plt.yticks(range(min(filtered_weather_df["weathersit"]), max(filtered_weather_df["weathersit"]) + 1, 1))
    plt.tick_params(axis='x', labelsize=12)
    st.pyplot(plt)

    st.write("""
    Kode Cuaca
    1. Cuaca cerah, sedikit berawan, sebagian berawan, sebagian berawan.
    2. Berkabut dan berawan, berkabut dengan awan terputus, berkabut dengan sedikit awan, berkabut.
    3. Salju ringan, hujan ringan dengan badai petir dan awan tersebar, hujan ringan dengan awan tersebar.
    4. Hujan lebat dengan butiran es, badai petir, dan kabut; salju dengan kabut.
    """)

with tab2:
    st.header("Analisis Berdasarkan Hari 📅")

    # Get weekday data
    weekday_df = get_weekday_data(day_df)

    # Plot weekday data
    day = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    plt.figure(figsize=(10, 5))
    sns.barplot(
        y="mean",
        x="weekday",
        data=weekday_df.sort_values(by="mean", ascending=False)
    )
    plt.title("Rata rata rental sepeda berdasarkan hari", loc="center", fontsize=15)
    plt.ylabel("Jumlah rental")
    plt.xlabel(None)
    plt.xticks(range(len(day)), day)
    plt.yticks(range(4000, 5000, 100))
    plt.tick_params(axis='x', labelsize=12)
    plt.ylim(4000, 5000)
    st.pyplot(plt)

    # Clear figure before plotting pie chart
    plt.clf()

    # Get working day vs holiday data
    workingday_cnt, holiday_cnt = get_working_holiday_data(day_df)

    # Plot pie chart
    plt.pie([workingday_cnt, holiday_cnt], labels=['Working Day', 'Holiday'], autopct='%1.1f%%')
    plt.title('Perbandingan rental sepeda antara hari kerja dan hari libur')
    st.pyplot(plt)
