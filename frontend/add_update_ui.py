import streamlit as st
from datetime import datetime
import requests

API_URL = 'http://localhost:8000'

def add_update_tab():
    selected_date = st.date_input('Enter Date',
                                  datetime(2024, 8, 1),
                                  label_visibility='collapsed')

    response = requests.get(f'{API_URL}/expenses/{selected_date}')
    if response.status_code == 200:
        existing_expenses = response.json()
        if not existing_expenses:
            st.info('No expenses found for the selected date.')
        # st.write(existing_expenses)
    else:
        st.error('Failed to retrieve expenses')
        existing_expenses = []

    categories = ['Rent', 'Food', 'Shopping', 'Entertainment', 'Other']

    with st.form(key='expense_form'):
        col1, col2, col3 = st.columns(3)

        # Display column headers
        with col1:
            st.subheader('Amount')
        with col2:
            st.subheader('Category')
        with col3:
            st.subheader('Notes')

        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = 'Shopping'
                notes = ''

            # Display Row
            with col1:
                amount_input = st.number_input('Amount',
                                               min_value=0.0,
                                               step=100.0,
                                               value=amount,
                                               key=f'amount_{i}',
                                               label_visibility='collapsed')
            with col2:
                category_input = st.selectbox('Category',
                                              options=categories,
                                              index=categories.index(category) if category in categories else 0,
                                              key=f'category_{i}',
                                              label_visibility='collapsed')
            with col3:
                notes_input = st.text_input(label='Notes',
                                            value=notes,
                                            key=f'notes_{i}',
                                            label_visibility='collapsed')

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button('Submit')
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            post_response = requests.post(f'{API_URL}/expenses/{selected_date}', json=filtered_expenses)
            if post_response.status_code == 200:
                st.success('Expenses updated successfully!')
            else:
                st.error('Failed to update expenses.')