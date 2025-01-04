# from Top_functions import *
import streamlit as st
import os, time, base64
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.sql import text
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    layout="wide",
    page_icon="🤖",
    )

# Database connection parameters
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
TG_BOT_OWNER_ID = int(os.getenv('TG_BOT_OWNER_ID'))
today_year = datetime.now().year

def format_number(num):
    if not num:
        return 0
    if type(num) is dict:
        print(num)
        return 0
    if type(num) is not str and not float and not int:
        return num
    if type(num) is str:
        try:
            num = float(num)
        except Exception as e:
            return num
    positive = 1 if num >= 0 else -1
    num = abs(num)
    if num >= 1000:
        num = int(num)
        num = num * positive
        num = format(num, ',')
        return num
    if num >= 100:
        num = int(num)
        return num * positive
    if num >= 1:
        num = round(num, 2)
        return num * positive
    if num < 0.0001:
        return num * positive
    if num < 1:
        after_0_num = str(num).split('.')[-1]
        list_number = list(after_0_num)
        for i in range(len(list_number)):
            if int(list_number[i]) != 0:
                zero_num = i
                break
        num = round(num, zero_num + 3)
        return num * positive
    
def display_header():
    st.markdown(f"<h1 style='text-align: center;'>{today_year} Expenditure Dashboard</h1>", unsafe_allow_html=True)

def read_plot_expenditure_table():
    today_year = datetime.now().year
    query = f"SELECT Date, Time, Spent, Category, Merchant, ItemName, Price FROM user_expenditures_record WHERE From_id = {TG_BOT_OWNER_ID} AND Date LIKE '{today_year}%' ORDER BY Date, Time"
    df = pd.DataFrame(engine.connect().execute(text(query)).fetchall())
    
    # Making 'Spent' column numeric and splitting data based on expenditure size
    df['Spent'] = pd.to_numeric(df['Spent'])

    # Make total spent of each month
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%Y-%m')
    df_month = df.groupby('Date').sum(numeric_only=True).reset_index()
    # drop price column from df_month
    df_month = df_month.drop(columns=['Price'])

    # st.dataframe(df_month)
    
    df_large = df[df['Spent'] > 10000]
    df_small = df[df['Spent'] <= 10000]

    def plot_pie_chart(data, title, column='Category', limit=6):
        fig, ax = plt.subplots()
        
        # Aggregate data: keep the top 5 and combine the rest into 'Others'
        top_categories = data.groupby(column)['Spent'].sum().nlargest(limit).index
        aggregated_data = data.copy()
        aggregated_data.loc[~aggregated_data[column].isin(top_categories), column] = 'Others'
        grouped_data = aggregated_data.groupby(column)['Spent'].sum()

        # Plot the pie chart with aggregated data
        grouped_data.plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax)
        ax.set_title(title)
        ax.set_ylabel('')  # Hides the 'Spent' label on the y-axis
        st.pyplot(fig)


    def plot_bar_chart(data, title, column='Category', limit=12):
        fig, ax = plt.subplots()

        # Aggregate data: keep the top 5 and combine the rest into 'Others'
        top_categories = data.groupby(column)['Spent'].sum().nlargest(limit).index
        aggregated_data = data.copy()
        aggregated_data.loc[~aggregated_data[column].isin(top_categories), column] = 'Others'
        grouped_data = aggregated_data.groupby(column)['Spent'].sum()

        # Plot the bar chart with aggregated data
        grouped_data.plot(kind='bar', ax=ax)
        ax.set_title(title)
        ax.set_ylabel('Spent')
        st.pyplot(fig)
    
    small_col_1, small_col_2 = st.columns(2)
    with small_col_1: plot_pie_chart(df_small, 'Small Expenditure by Category', column='Category', limit=6)
    with small_col_2: plot_pie_chart(df_small, 'Small Expenditure by Merchant', column='Merchant', limit=6)

    month_col_1, month_col_2 = st.columns(2)
    with month_col_1: plot_pie_chart(df_month, 'Monthly Expenditure by Category', column='Date', limit=4)
    with month_col_2: plot_bar_chart(df_month, 'Monthly Expenditure by Category', column='Date', limit=12)

    with st.expander("View Large Expenditure Chart", expanded=False):
        large_col_1, large_col_2 = st.columns(2)
        with large_col_1: plot_pie_chart(df_large, 'Large Expenditure by Category', column='Category', limit=6)
        with large_col_2: plot_pie_chart(df_large, 'Large Expenditure by Merchant', column='Merchant', limit=6)

    with st.expander("View Expenditure Table", expanded=False): st.dataframe(df)

    # Make a download link to download the dataframe as csv
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{today_year}_expenditure.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

    return 



def main():
    display_header()
    read_plot_expenditure_table()

if __name__ == "__main__":
    main()
