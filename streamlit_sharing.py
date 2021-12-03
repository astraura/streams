import streamlit as st
import pandas as pd
from gsheetsdb import connect

st.write("My First Streamlit Web App")

df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
st.write(df)

gsheet= st.secrets["public_gsheets_url"]
st.title("Connect to Google Sheets")
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet}"')
df_gsheet = pd.DataFrame(rows)
st.write(df_gsheet)
