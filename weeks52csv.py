from io import StringIO

import requests
import pandas as pd
import streamlit as st
from datetime import datetime as dt
df200 = pd.DataFrame()
df500 = pd.DataFrame()
st.subheader("NSE Stock selection based on 52 week high.")
msg = "Warning. Page visits external sites to update data. Please wait. It may take a minute."
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
    msg = "Warning. Page visits external sites to update data. Please wait. It may take a minute."

    st.warning(msg, icon="⚠️")
    niftyapiurl1='https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20200'
    niftyapiurl2 = "https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY500%20MULTICAP%2050%3A25%3A25"
    getNifty(niftyapiurl1, 'Nifty_200.csv')
    getNifty(niftyapiurl2, 'Nifty_500multi.csv')
   
    curd = dt.now().strftime('%Y-%m-%d')

    data=[]
    updated = pd.DataFrame(data, columns=['Date'])
    updated.loc[0,'Date']= curd
    updated.to_csv('Updated.csv')
    msg =''

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
#st.write(df0)




#print(df)
df = df0.copy()
df.replace(to_replace = '-', value = 0, inplace=True)
df.columns = ['Symbol', 'Open', 'High', 'Low', 'prev close','Close', 'chg','chg%', 'Volume','Value', 'yearHigh','yearLow',
              'return1y', 'return1m']
df = df.drop (columns= ['Open', 'High', 'Low'])
df.replace(',','', regex=True, inplace=True)
for col in df.columns:
    if (col!="Symbol"):
        df[col]= df[col].astype(float)
#st.write(df)

def write_formatted(dfx):
    st.dataframe(dfx.style.format(subset=['prev close','Close', 'chg','chg%', 'Volume','Value', 'yearHigh','yearLow',
        'return1y', 'return1m','nearWKH','nearWKL','ret_multiple','RS_Rating','HiLoRange%'], formatter="{:.2f}"))

def write_formatted2(dfx):
    st.dataframe(dfx.style.format(subset=['prev close','Close', 'chg','chg%', 'Volume','Value', 'yearHigh','yearLow',
        'return1y', 'return1m'], formatter="{:.2f}"))


#st.dataframe(df.style.format(subset=['prev close','Close', 'chg','chg%', 'Volume','Value', 'yearHigh','yearLow','return1y', 'return1m'], formatter="{:.2f}"))


index_return = float(df.loc[0,'return1y']) #df[df['Symbol']=='NIFTY 200']['return1y'].values[0]

dfi = df.iloc[0:1].copy()
dfs = df.iloc[1:].copy()
df1 = dfs[dfs['return1y']!='-'].copy()

df1.replace('-',0)
df1['Close']= df1['Close'].astype(float)
df1['prev close']= df1['prev close'].astype(float)

df1['yearHigh']= df1['yearHigh'].astype(float)
df1['yearLow']= df1['yearLow'].astype(float)

df1['return1y'] = df1['return1y'].astype(float)
df1['return1m'] = df1['return1m'].astype(float)
df1['ret_multiple']= df1['return1y']/index_return
df1['RS_Rating'] = df1.ret_multiple.rank(pct=True) * 100

df1['HiLoRange%'] = round((df1['yearHigh']/df1['yearLow']-1)*100,2)

df1['nearWKH'] = round((df1['yearHigh']/df1['prev close']-1)*100,2)
df1['nearWKL'] = round((df1['yearLow']/df1['prev close']-1)*100,2)

cols = ['Symbol', 'Close',  'yearHigh','yearLow','nearWKH','nearWKL', 'return1y', 'return1m', 'ret_multiple','RS_Rating','HiLoRange%','prev close', 'chg','chg%', 'Volume','Value']
df1=df1[cols]

df1=df1[df1['return1y']>0]
df1=df1[df1['nearWKL']<-25]
df1=df1[df1['nearWKH']<30]
df1=df1[df1['RS_Rating']>70]

df1=df1.sort_values(by=['return1y','nearWKH'], ascending=[False, True])

df2 = df1[df1['nearWKH']<12]
df3 =df1.sort_values(by=['return1m','nearWKH'], ascending=[False, True]).copy()
df3=df3[df3['nearWKH']<12]

st.subheader(titles[0])
st.write("Stocks - Ranked and sorted based Relative Strenth and nearness to 52week high.")
st.write("Relative strength is the rank with reference to returns of stock  vs index ")
st.write("Filtered stocks are above rank 70/100 and within 30% from 52 week high and 25% above 52 week low.")
st.write("Stocks nearness to 52 week high is set to max 12%")
#df2= df2.style.format({"Close": "{:.2f}"})
write_formatted(df2)

#st.write(df2)
st.write("Momentum stocks sorted on the basis of last monthly return")
#df3= df3.style.format({"Close": "{:.2f}"})
write_formatted(df3)

#st.write(df3)
st.subheader(titles[1])
#dfi= dfi.style.format({"Close": "{:.2f}"})
write_formatted2(dfi)

#st.write(dfi)
#dfs= dfs.style.format({"Close": "{:.2f}"})
write_formatted2(dfs)

#st.write(dfs) 

#st.dataframe(df.style.format(subset=['prev close','Close', 'chg','chg%', 'Volume','Value', 'yearHigh','yearLow','return1y', 'return1m'], formatter="{:.2f}"))
#write_formatted(df)
