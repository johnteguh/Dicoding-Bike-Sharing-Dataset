import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from babel.numbers import format_currency
from pandas import Timestamp
sns.set(style='dark')

def perseason (df):
    season_distribution_mean = df.groupby('season')['cnt'].mean()
    season_distribution_sum = df.groupby('season')['cnt'].sum()

    return season_distribution_mean, season_distribution_sum


def perhari (df,mulai,akhir):
    daily_cnt = df.groupby('dteday')['cnt'].sum()
    mulai = Timestamp(mulai)
    akhir = Timestamp(akhir)
    filtered_daily_cnt = daily_cnt.loc[(daily_cnt.index >= mulai) & (daily_cnt.index <= akhir)]
    return filtered_daily_cnt

df = pd.read_csv("https://raw.githubusercontent.com/johnteguh/Dicoding-Bike-Sharing-Dataset/a998d03901b2f85ff063c7a085d727459247a266/fixed_days.csv")
print(df)
start_date = df["dteday"].min()
end_date = df["dteday"].max()
jenis = None
value = (start_date, end_date)
df["dteday"]=pd.to_datetime(df["dteday"])
min_date = df["dteday"].min()
max_date = df["dteday"].max()


st.header('Bike Sharing Dataset')

with st.sidebar:
    genre = st.selectbox(
        label="What Distribution do you want to see?",
        options=("Please choose here", "Season Distribution", "Date Distribution"),
    )
    jenis = genre
    if genre == "Date Distribution":
        try:
            start_date, end_date = st.date_input(
                label='Rentang Waktu',
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date)
            )
        except ValueError:
            st.error('Please select both a start and end date.')
            start_date = end_date = None

if jenis == "Season Distribution":
    # Sort season_distribution_mean by value
    season_distribution_mean , season_distribution_sum = perseason(df)

    # FILEPATH: /c:/Users/TEGUH/Documents/Kuliah/Semester_6/Bangkit/Dicoding_DataAnalys/Final_Project/Proyek_Analisis_Data.ipynb
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))  # Change nrows to 1 and ncols to 2

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Chart for season_distribution_sum
    sns.barplot(x=season_distribution_sum.index, y=season_distribution_sum.values, hue=season_distribution_sum.index, palette=colors[:len(season_distribution_sum)], ax=ax[0], legend=False)
    ax[0].set_xlabel(None)
    ax[0].set_ylabel(None)
    ax[0].set_title("Season Distribution Sum", loc="center", fontsize=15)
    ax[0].tick_params(axis='y', labelsize=12)  # Change tick params to 'y' for vertical bar chart
    ax[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))  # Format y-axis labels as integers with commas

    # Chart for season_distribution_mean
    sns.barplot(x=season_distribution_mean.index, y=season_distribution_mean.values, hue=season_distribution_mean.index, palette=colors[:len(season_distribution_mean)], ax=ax[1], legend=False)
    ax[1].set_xlabel(None)
    ax[1].set_ylabel(None)
    ax[1].set_title("Season Distribution Mean", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)  # Change tick params to 'y' for vertical bar chart
    ax[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))  # Format y-axis labels as integers with commas

    plt.suptitle("Season Distribution Sum and Mean", fontsize=20)
    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)


if jenis == "Date Distribution":
    perhari(df,start_date,end_date).plot(kind='line', figsize=(10, 6))
    plt.title('Filtered Daily Count')
    plt.xlabel('Date')
    plt.ylabel('Count')

    st.pyplot(plt)