import streamlit as st
from datetime import datetime
import requests

from add_update_ui import add_update_tab
from analytics_category_ui import analytics_category_tab
from analytics_monthly_ui import analytics_monthly_tab

API_URL = 'http://localhost:8000'

st.title('Expense Tracking System')

tab1, tab2, tab3 = st.tabs(['Add/Update', 'Analytics_by_Category','Analytics_by_Monthly'])

with tab1:
    add_update_tab()

with tab2:
    analytics_category_tab()

with tab3:
    analytics_monthly_tab()