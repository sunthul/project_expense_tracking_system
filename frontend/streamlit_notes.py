import streamlit as st
from click import option

# Text Elements
st.header('Streamlit Core Features')
st.subheader('Text Elements')
st.text('This is a simple text element.')

# Data Display
st.subheader('Data Display')
st.write('Here is a simple table:')
st.table({'Column 1':[1,2,3],
          'Column 2':[4,5,6]})

# Charts
st.subheader('Charts')
st.line_chart([1,2,3,4])

# User Input
st.subheader('User Input')
value = st.slider('Select a value', 0, 100)
st.write(f'Selected value: {value}')

# Checkbox
if st.checkbox('Show/Hide'):
    st.write('Checkbox is checked')

# Select Box
option = st.checkbox('Select a number',[1,2,3,4], label_visibility='collapsed')
st.write(f'You selected: {option}')

# Multiselect
options = st.multiselect('Select multiple numbers', [1,2,3,4])
st.write(f'You selected: {options}')