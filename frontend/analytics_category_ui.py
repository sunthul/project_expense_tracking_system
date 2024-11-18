import pandas as pd
import streamlit as st
from datetime import datetime
import requests

API_URL = 'http://localhost:8000'

def analytics_category_tab():
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input('Start Date', datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input('End Date', datetime(2024, 8, 5))

    if st.button('Get Analytics'):
        payload = {'start_date': start_date.strftime('%Y-%m-%d'),
                   'end_date': end_date.strftime('%Y-%m-%d')}

        response = requests.post(f'{API_URL}/analytics_category/',
                                 json=payload)

        if response.status_code == 200:
            existing_expenses = response.json()
            # st.write(existing_expenses)
        else:
            st.error('Failed to retrieve expenses')
            existing_expenses = []

        data = {
            'Category': list(existing_expenses.keys()),
            'Total': [existing_expenses[category]['total'] for category in existing_expenses],
            'Percentage': [round(existing_expenses[category]['percentage'], 2) for category in existing_expenses]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by='Percentage', ascending=False).set_index('Category')

        st.title('Expenses Breakdown by Category')
        st.bar_chart(data=df_sorted['Percentage'].astype(float), use_container_width=True)

        st.table(df_sorted.style.format({'Percentage': "{:.2f}%"}))

# Example while working with Pandas DataFrame

# df = pd.DataFrame({
#     'Category': ['Rent', 'Shopping', 'Food'],
#     'Total': [1200, 800, 750],
#     'Percentage': [50, 30, 20]
# })
# st.table(df)
