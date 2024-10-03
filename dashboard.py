import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import streamlit as st
import numpy as np

def create_ssn_and_cnt_df(df):
  ssn_and_cnt_df = df.groupby(by='season').agg({'cnt': ['count', 'sum', 'mean']}).sort_values(by=('cnt', 'sum'), ascending=False).reset_index()
  ssn_and_cnt_df['season'] = ssn_and_cnt_df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

  return ssn_and_cnt_df

def create_wthr_and_cnt_df(df):
  wthr_and_cnt_df = df.groupby(by='weathersit').agg({'cnt': ['count', 'sum', 'mean']}).sort_values(by=('cnt', 'sum'), ascending=False).reset_index()
  wthr_and_cnt_df['weathersit'] = wthr_and_cnt_df['weathersit'].replace({
    1: 'Clear or Partly Cloudy',
    2: 'Mist + Cloudy',
    3: 'Light Snow or Light Rain',
    4: 'Heavy Rain or Heavy Snow'
  })

  return wthr_and_cnt_df

def create_mnth_and_cnt_df(df):
  mnth_and_cnt_df = df.groupby(by='mnth').agg({'cnt': ['sum', 'mean']}).reset_index() 

  return mnth_and_cnt_df

def create_wekdy_and_cnt_df(df):
  wekdy_and_cnt_df = df.groupby(by='weekday').agg({'cnt': ['sum', 'mean']}).reset_index()
  wekdy_and_cnt_df['weekday'] = wekdy_and_cnt_df['weekday'].replace({
      0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'})

  return wekdy_and_cnt_df

def create_hr_and_cnt_df(df):
  hr_and_cnt_df = df.groupby(by='hr').agg({'cnt': ['sum', 'mean']}).reset_index()

  return hr_and_cnt_df

def create_hlday_and_cr_df(df):
  hlday_and_cr_df = df.groupby(by='holiday').agg({'casual': ['sum', 'mean'], 'registered': ['sum', 'mean']}).reset_index()

  return hlday_and_cr_df

def create_wrkday_and_cr_df(df):
  wrkday_and_cr_df = df.groupby(by='workingday').agg({'casual': ['sum', 'mean'], 'registered': ['sum', 'mean']}).reset_index()

  return wrkday_and_cr_df

def create_atemp_and_cnt_df(df):
   df['atemp_category'] = pd.cut(df['atemp'], bins=[0, 0.318, 0.54, 0.666, 0.772, 1],
                                      labels=['Sangat Dingin', 'Dingin', 'Sejuk', 'Hangat', 'Panas'])
   
   atemp_and_cnt_df = df.groupby(by='atemp_category').agg({'cnt': ['sum', 'mean']})

   return atemp_and_cnt_df

hour_df = pd.read_csv('main_data.csv')
hour_df = hour_df.sort_values(by='dteday', ascending=True)

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], errors='coerce')

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()
 
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

ssn_and_cnt_df = create_ssn_and_cnt_df(main_df)
wthr_and_cnt_df = create_wthr_and_cnt_df(main_df)
mnth_and_cnt_df = create_mnth_and_cnt_df(main_df)
wekdy_and_cnt_df = create_wekdy_and_cnt_df(main_df)
hr_and_cnt_df = create_hr_and_cnt_df(main_df)
hlday_and_cr_df = create_hlday_and_cr_df(main_df)
wrkday_and_cr_df = create_wrkday_and_cr_df(main_df)
atemp_and_cnt_df = create_atemp_and_cnt_df(main_df)

st.header('Dashboard :sparkles:')

st.subheader('Total Number of Rental Bikes per Season')

col1, col2, col3 = st.columns(3)

with col1:
    total_records = main_df['cnt'].count()
    st.metric("Total Records", value=total_records)
 
with col2:
    total_bike_rentals = main_df['cnt'].sum() 
    st.metric("Total Bike Rentals", value=total_bike_rentals)
  
max_season_sum = ssn_and_cnt_df[('cnt', 'sum')].max()
max_weather_sum = wthr_and_cnt_df[('cnt', 'sum')].max()

fig, axes = plt.subplots(1, 2, figsize=(15, 8))

sns.barplot(x='season', y=('cnt', 'sum'),
            data=ssn_and_cnt_df, palette=['lightcoral' if v == max_season_sum else 'gray' for v in ssn_and_cnt_df[('cnt', 'sum')]], ax=axes[0])
axes[0].set_title('per Season in 2011-2012')
axes[0].set_xlabel('')
axes[0].set_ylabel('')

sns.barplot(x='weathersit', y=('cnt', 'sum'), data=wthr_and_cnt_df,
            palette=['lightblue' if v == max_weather_sum else 'gray' for v in wthr_and_cnt_df[('cnt', 'sum')]], ax=axes[1])
axes[1].set_title('for Each Weather Situation in 2011-2012')
axes[1].set_xlabel('')
axes[1].set_ylabel('')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, fontsize=9)

plt.tight_layout()
st.pyplot(fig)



st.subheader('Total Number of Rental Bikes')

col1, col2, col3 = st.columns(3)

with col1:
    mean_per_month = mnth_and_cnt_df[('cnt', 'sum')].sum() / mnth_and_cnt_df['mnth'].nunique()
    st.metric("Average Bike Rental per Month", value=round(mean_per_month, 2))
 
with col2:
    mean_per_day = wekdy_and_cnt_df[('cnt', 'sum')].sum() / wekdy_and_cnt_df['weekday'].nunique()
    st.metric("Average Bike Rental per Day", value=round(mean_per_day, 2))

with col3:
    mean_per_hour = hr_and_cnt_df[('cnt', 'sum')].sum() / hr_and_cnt_df['hr'].nunique()
    st.metric("Average Bike Rental per Hour", value=round(mean_per_hour, 2))

sns.set(style="whitegrid")

def get_colors(values, cmap_name='Blues', min_color_value=0.25):
    norm = plt.Normalize(values.min() - (values.max() - values.min()) * min_color_value, values.max())
    cmap = cm.get_cmap(cmap_name)
    return cmap(norm(values))

fig, axes = plt.subplots(1, 3, figsize=(18, 8))

colors = get_colors(mnth_and_cnt_df[('cnt', 'sum')].values)
sns.barplot(
    x=mnth_and_cnt_df.index, 
    y=mnth_and_cnt_df[('cnt', 'sum')], 
    ax=axes[0], 
    palette=colors
)
axes[0].set_title('per Month')
axes[0].set_ylabel('')
axes[0].set_xlabel('')

colors = get_colors(wekdy_and_cnt_df[('cnt', 'sum')].values)
sns.barplot(
    x=wekdy_and_cnt_df['weekday'], 
    y=wekdy_and_cnt_df[('cnt', 'sum')], 
    ax=axes[1], 
    palette=colors
)
axes[1].set_title('per Weekday')
axes[1].set_ylabel('')
axes[1].set_xlabel('')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, fontsize=10)

colors = get_colors(hr_and_cnt_df[('cnt', 'sum')].values)
sns.barplot(
    x=hr_and_cnt_df.index, 
    y=hr_and_cnt_df[('cnt', 'sum')], 
    ax=axes[2], 
    palette=colors
)
axes[2].set_title('per Hour')
axes[2].set_ylabel('')
axes[2].set_xlabel('')

plt.tight_layout()

st.pyplot(fig)



st.subheader('Average Casual and Registered Users per Hour')

col1, col2, col3 = st.columns(3)

with col1:
   st.metric('Total Records', value=total_records)

with col2:
   total_casual = main_df['casual'].sum()
   st.metric("Total Casual Bike Rental", value=total_casual)
  
with col3:
   total_registered = main_df['registered'].sum()
   st.metric("Total Registered Bike Rental", value=total_registered)

labels = ['Casual', 'Registered']

holiday_means = [hlday_and_cr_df.loc[(1, ('casual', 'mean'))], hlday_and_cr_df.loc[(1, ('registered', 'mean'))]]  
nonholiday_means = [hlday_and_cr_df.loc[(0, ('casual', 'mean'))], hlday_and_cr_df.loc[(0, ('registered', 'mean'))]]
workingday_means = [wrkday_and_cr_df.loc[(1, ('casual', 'mean'))], wrkday_and_cr_df.loc[(1, ('registered', 'mean'))]]
nonworkingday_means = [wrkday_and_cr_df.loc[(0, ('casual', 'mean'))], wrkday_and_cr_df.loc[(0, ('registered', 'mean'))]]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(1, 2, figsize=(18, 8))

ax[0].bar(x - width/2, holiday_means, width, label='Holiday', color='lightblue')
ax[0].bar(x + width/2, nonholiday_means, width, label='Non-Holiday', color='lightcoral')

ax[0].set_xlabel('')
ax[0].set_ylabel('')
ax[0].set_title('on Holidays and Non-Holiday', fontsize=12)
ax[0].set_xticks(x)
ax[0].set_xticklabels(labels)
ax[0].legend()

ax[1].bar(x - width/2, workingday_means, width, label='Working Day', color='lightblue')
ax[1].bar(x + width/2, nonworkingday_means, width, label='Non-Working Day', color='lightcoral')

ax[1].set_xlabel('')
ax[1].set_ylabel('')
ax[1].set_title('on Working Days and Non-Working Days', fontsize=11)
ax[1].set_xticks(x)
ax[1].set_xticklabels(labels)
ax[1].legend()

plt.subplots_adjust(wspace=10)

plt.tight_layout()

st.pyplot(fig)


st.subheader('Total Rental Bikes for Each Air Temperature Category')

average_atemp = (main_df['atemp'].mean() * 66) - 16
st.metric('Average Air Temperature', value=round(average_atemp, 2))

max_atemp_sum = atemp_and_cnt_df[('cnt', 'sum')].max()

fig = plt.figure(figsize=(10, 6))
sns.barplot(x='atemp_category', y=('cnt', 'sum'),
            data=atemp_and_cnt_df, palette=['lightcoral' if v == max_atemp_sum else 'gray' for v in atemp_and_cnt_df[('cnt', 'sum')]])

plt.xlabel(None)
plt.ylabel(None)
plt.xticks(rotation=30)

# Tampilkan plot
plt.tight_layout()
st.pyplot(fig)
