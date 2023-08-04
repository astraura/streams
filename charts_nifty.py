import requests
import pandas as pd
import streamlit as st

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}



sess = requests.Session()
cookies = dict()
url_nif ='https://www.nseindia.com/market-data/live-equity-market'
def set_cookie():
    request = sess.get(url_nif, headers=headers, timeout=5)
    cookies = dict(request.cookies)
url200='https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20200'
url500='https://www.nseindia.com/api/equity-stockIndices?index=NIFTY500%20MULTICAP%2050%3A25%3A25'

def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        #return response.text
        return response.json()
    return ""
#url200='https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20200'
#url500=''
data=[]
apidata1=get_data(url200)
apidata2=get_data(url500)
def get_df(apidata):
    for item in apidata['data']:
        data.append([
            item['symbol'], item['lastPrice'], item['previousClose'], item['yearHigh'], item['yearLow'], item['perChange365d'],  item['nearWKH'], item['nearWKL'], item['perChange30d']] )

    cols=['Symbol','Close','lastClose','yearHigh','yearLow', 'return1y', 'nearWKH','nearWKL', 'return1m']

    df = pd.DataFrame(data, columns=cols)
    return df
df1= get_df(apidata1)    
df2= get_df(apidata2)
st.write(df1)
st.write(df2)
