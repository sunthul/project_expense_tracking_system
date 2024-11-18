import pandas as pd
import streamlit as st
from datetime import datetime
import requests

API_URL = 'http://localhost:8000'

def analytics_monthly_tab():
    response = requests.get(f'{API_URL}/analytics_monthly/')

    if response.status_code == 200:
        existing_expenses = response.json()
        # Converting JSON to DataFrame
        data = [{'Month': month, 'Total': details['total'], 'Percentage': details['percentage']} for month, details in existing_expenses.items()]
        df = pd.DataFrame(data)
        # st.write(df)

        df_sorted = df.sort_values(by='Percentage', ascending=False).set_index('Month')

        st.title('Expenses Breakdown by Monthly')
        st.bar_chart(data=df_sorted['Percentage'].astype(float), use_container_width=True)

        st.table(df_sorted.style.format({'Percentage': "{:.2f}%"}))
    else:
        st.error('Failed to retrieve expenses')
        existing_expenses = []
