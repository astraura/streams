from io import StringIO

import requests
import pandas as pd
import streamlit as st
from datetime import datetime as dt

df200 = pd.DataFrame()
df500 = pd.DataFrame()
st.subheader("NSE Stock selection based on 52 week high.")

msg = 'Warning. Page visits external sites to update data. Please wait. It may take a minute.'

def getNifty(niftyapiurl, csvfile):
    niftyurl='https://www.nseindia.com/market-data/live-equity-market'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}
    with requests.session() as req:
        
        req.get("https://www.nseindia.com/", headers=headers) 

        req.get(niftyurl,headers = headers)  # to save cookies

        api0=req.get(niftyapiurl,headers = headers)
        df00 = pd.read_csv(StringIO(api0.text[3:]))
        df00.to_csv(csvfile)
        #return df00


def gatherData():
    msg = 'Warning. Page visits external sites to update data. Please wait. It may take a minute.'

    #st.write(msg)
    st.warning(msg,icon="⚠️")
    niftyapiurl1='https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20200'
    niftyapiurl2 = "https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY500%20MULTICAP%2050%3A25%3A25"
    getNifty(niftyapiurl1, 'Nifty_200.csv')
    getNifty(niftyapiurl2, 'Nifty_500multi.csv')
   
    curd = dt.now().strftime('%Y-%m-%d')

    data=[]
    updated = pd.DataFrame(data, columns=['Date'])
    updated.loc[0,'Date']= curd
    updated.to_csv('Updated.csv')
    msg = ''

dfd = pd.read_csv("Updated.csv")
last_update = pd.to_datetime(dfd[-1:]['Date'].values[0])

curd = dt.now().strftime('%Y-%m-%d')
data =[]
dtdf = pd.DataFrame(data, columns=['Date'])
dtdf.loc[0,'Date']= curd
curdate = pd.to_datetime(dtdf[-1:]['Date'].values[0])
#curdate
#if pd.Timestamp.now()>last_update:
if curdate  >last_update:
    gatherData()
    df200 = pd.read_csv("Nifty_200.csv", index_col=[0])
    df500 = pd.read_csv("Nifty_500multi.csv", index_col=[0])
    msg =''
else:
    df200 = pd.read_csv("Nifty_200.csv", index_col=[0])
    df500 = pd.read_csv("Nifty_500multi.csv", index_col=[0])
    msg=''

genre = st.radio(
    "Select index for Analysis ",
    ('Nifty 200',  'Nifty 500 Multicap'))

if genre == 'Nifty 200':
    titles= ["Nifty 200 picks ","Nifty 200 + stocks raw data"]
    df0= df200 # pd.read_csv("Nifty_200.csv", index_col=[0])
else:
    titles= ["Nifty 500 multicap picks ","Nifty 500 multicap + stocks raw data"]
    df0= df500 # pd.read_csv("Nifty_500multi.csv", index_col=[0])

#st.write(''curdate)
st.write('Uptated on: ' )
st.write(last_update)
st.write(df0)




