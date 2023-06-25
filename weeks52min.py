import requests
import pandas as pd
import json
import streamlit as st

niftyapiurl='https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20200'
niftyurl='https://www.nseindia.com/market-data/live-equity-market'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}

with requests.session() as req:
    req.get(niftyurl,headers = headers)

    api_req=req.get(niftyapiurl,headers = headers).json()
    
data=[]

for item in api_req['data']:
    data.append([
        item['symbol'], item['lastPrice'], item['previousClose'], item['yearHigh'], item['yearLow'], item['perChange365d'],  item['nearWKH'], item['nearWKL'], item['perChange30d']] )

cols=['Symbol','Close','lastClose','yearHigh','yearLow', 'return1y', 'nearWKH','nearWKL', 'return1m']

df = pd.DataFrame(data, columns=cols)
#print(df)

df['HiLoRange%'] = round((df['yearHigh']/df['yearLow']-1)*100,2)
index_return = df[df['Symbol']=='NIFTY 200']['return1y'].values[0]

dfi = df.iloc[0:1].copy()
dfs = df.iloc[1:].copy()
df1 = dfs[dfs['return1y']!='-'].copy()
df1['ret_multiple']= df1['return1y']/index_return
df1['RS_Rating'] = df1.ret_multiple.rank(pct=True) * 100

df1.replace('-',0)
df1['return1y'] = df1['return1y'].astype(float)
df1['nearWKH'] = df1['nearWKH'].astype(float)
df1['nearWKL'] = df1['nearWKL'].astype(float)

df1=df1[df1['return1y']>0]
df1=df1[df1['nearWKL']<-25]
df1=df1[df1['nearWKH']<30]
df1=df1[df1['RS_Rating']>70]

df1=df1.sort_values(by=['return1y','nearWKH'], ascending=[False, True])

df2 = df1[df1['nearWKH']<12]
df3 =df1.sort_values(by=['return1m','nearWKH'], ascending=[False, True]).copy()
df3=df3[df3['nearWKH']<12]

st.subheader("Nifty 200 picks based on 52 week high.")
st.write("Ranked and sorted based Relative Strenth and nearness to 52week high.")
st.write("Relative strength is the rank with reference to returns of stock  vs index ")
st.write("Filtered stocks above rank 70/100 and within 30% from 52 week high and 25% above 52 week low.")
st.write("Stocks nearness to 52 week high max 12%")
df2= df2.style.format({"Close": "{:.2f}"})

st.write(df2)
st.write("Momentum stocks sorted on the basis of last monthly return")
df3= df3.style.format({"Close": "{:.2f}"})

st.write(df3)
st.subheader("Nifty 200 + stocks raw data")
dfi= dfi.style.format({"Close": "{:.2f}"})

st.write(dfi)
dfs= dfs.style.format({"Close": "{:.2f}"})

st.write(dfs) 
