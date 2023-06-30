from io import StringIO

import requests
import pandas as pd
import streamlit as st
from datetime import datetime as dt
from bs4 import BeautifulSoup

df200 = pd.DataFrame()
df500 = pd.DataFrame()
st.subheader("NSE Stock selection based on 52 week high.")


def getNifty(niftyapiurl, csvfile, csv2):


    headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    with requests.session() as req:
        


        #api0=req.get(niftyapiurl,headers = headers)
        api0= req.get(niftyapiurl, headers = headers,timeout=15)
        nif200soup = BeautifulSoup(api0.content, 'html.parser')

        ind = float(nif200soup.find("span",class_="LpriceCP").get_text().strip())
        indchg = float(nif200soup.find_all("span",class_="growth-first-heading")[5].get_text().strip())
        ind_return = pd.DataFrame(data, columns=['Return'])
        ind_return.loc[0,'Return']= round(indchg/ind*100,2)

        api0= api0.text.replace("&nbsp","")

        df00 = pd.read_html(api0)[0]
        df00.to_csv(csvfile)
        ind_return.to_csv(csv2)
        #return ind_return


def gatherData():

    niftyapiurl1='https://trendlyne.com/equity/1892/NIFTY200/nifty-200/'
    niftyapiurl2 = "https://trendlyne.com/equity/910418/NFT500MULT/nifty-500-multicap-50-25-25/"
    getNifty(niftyapiurl1, 'Nifty_200tl.csv','Nifty200ret.csv')
    getNifty(niftyapiurl2, 'Nifty_500multitl.csv','Nifty500ret.csv')
   
    curd = dt.now().strftime('%Y-%m-%d')

    data=[]
    updated = pd.DataFrame(data, columns=['Date'])
    updated.loc[0,'Date']= curd
    updated.to_csv('Updated2.csv')

dfd = pd.read_csv("Updated2.csv")
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
    df200 = pd.read_csv("Nifty_200tl.csv", index_col=[0])
    df500 = pd.read_csv("Nifty_500multitl.csv", index_col=[0])
    ret200 = pd.read_csv('Nifty200ret.csv')
    ret500 = pd.read_csv('Nifty500ret.csv')


else:
    df200 = pd.read_csv("Nifty_200tl.csv", index_col=[0])
    df500 = pd.read_csv("Nifty_500multitl.csv", index_col=[0])
    ret200 = pd.read_csv('Nifty200ret.csv')
    ret500 = pd.read_csv('Nifty500ret.csv')

genre = st.radio(
    "Select index for Analysis ",
    ('Nifty 200',  'Nifty 500 Multicap'))

if genre == 'Nifty 200':
    titles= ["Nifty 200 picks ","Nifty 200 + stocks raw data"]
    df0= df200 # pd.read_csv("Nifty_200.csv", index_col=[0])
    indret = ret200.loc[0,'Return']

else:
    titles= ["Nifty 500 multicap picks ","Nifty 500 multicap + stocks raw data"]
    df0= df500 # pd.read_csv("Nifty_500multi.csv", index_col=[0])
    indret = ret500.loc[0,'Return']

#st.write(''curdate)
st.write('Uptated on:  '  + str(last_update)[0:10])
#st.write(last_update)
st.write('Index return 1 year:  ' + str(indret) +'%') 

#print(df)
dft0 = df0.copy()
#df.replace(to_replace = '-', value = 0, inplace=True)
dft0.rename(columns = {'LTPLast Traded Price':'Last Close'}, inplace = True)
dft0.drop(['3M Price Chart'], axis=1, inplace=True,)
#df.columns = ['Stock Name', 'Open', 'High', 'Low', 'prev close','Close', 'chg','chg%', 'Volume','Value', 'yearHigh','yearLow', 'return1y', 'return1m']
#df = df.drop (columns= ['Open', 'High', 'Low'])
#df.replace(',','', regex=True, inplace=True)
#st.write(df)

def company2symbol(company):
    try:
        company = company.replace('(',"")
        company = company.replace(')',"")
        nifsymbol = nifty_list[nifty_list['Company Name'].str.lower()==company.lower()]['Symbol']
        return nifsymbol.values[0]

        

    except:
        try:
            nifsymbol = nifty_list[nifty_list['Company Name'].str.contains(company[:10])]['Symbol']
            return nifsymbol.values[0]
        except:
            try: 
                
                nifsymbol = nifty_list[nifty_list['Company Name'].str.contains(company[:5])]['Symbol']
                return nifsymbol.values[0]
            except:
                
                return company


def company2symbol2(company):

    try:

        
        symbol = company.replace("'","") 
        symbol = symbol.replace('Ltd.',"")
        symbol = symbol.replace('(',"")
        symbol = symbol.replace(')',"")   
        symbol = symbol.replace('-'," ")
        symbol = symbol.lower()
        symbol = symbol.split(' ')
        symbol2= symbol[0].strip()
        length = min(len(symbol),2)
        symbol =' '.join(symbol[0:length]).strip()
        
        nifsymbol = nifty_list[nifty_list['ncompany']==symbol ]['SYMBOL']
        return nifsymbol.values[0]
    except:
        try:
            nifsymbol = nifty_list[nifty_list['ncompany'].str.contains(symbol[:6])]['SYMBOL']
            return nifsymbol.values[0]
        except:
            return company

def company2sector(symbol):
    try:
        
        sector = sector_list[sector_list['Symbol']==symbol]['Industry']
        return sector.values[0]
    except:
        return 'N/A'

def h52w(symbol):
    try:
        
        high = dft0[dft0['Symbol']==symbol]['1 Year High low(%)']
        return float(high.values[0].split(' ')[-1])
    except:
        return 0
    
def l52w(symbol):
    try:
        
        low = dft0[dft0['Symbol']==symbol]['1 Year High low(%)']
        return float(low.values[0].split(' ')[-3])
    except:
        return 0
def hmon(symbol):
    
    try:
        
        low = dft0[dft0['Symbol']==symbol]['Month High Low (%)']
        return float(low.values[0].split(' ')[-1])
    except:
        return 0    
    
    
def lmon(symbol):
    
    try:
        
        low = dft0[dft0['Symbol']==symbol]['Month High Low (%)']
        return float(low.values[0].split(' ')[-3])
    except:
        return 0    
def lweek(symbol):
    
    try:
        
        low = dft0[dft0['Symbol']==symbol]['Week High Low (%)']
        return float(low.values[0].split(' ')[-3])
    except:
        return 0      
def returns(symbol, field):
    try:
        
        ret = dft0[dft0['Symbol']==symbol][field]
        return float(ret.values[0].split(' ')[2].replace('%',''))
    except:
        return 0      

def write_formatted(dfx, except_cols):
    colnames=[]
    for col in dfx.columns:
        colnames.append(col)
    colnames=colnames[except_cols:]    
    st.dataframe(dfx.style.format(subset=colnames, formatter="{:.2f}"))

nifty_list  = pd.read_csv("NSE_symbols.csv") #pd.read_csv("nse_symbols2.csv")
sector_list = pd.read_csv("NSE_symbols.csv")

dft0['Symbol'] =dft0['Stock Name']
dft0['Symbol']=dft0['Symbol'].apply(lambda x: company2symbol(x))
dft0['Sector']=dft0['Symbol'].apply(lambda x: company2sector(x))

dft0['WkLow']= dft0['Symbol'].apply(lambda x: lweek(x))
dft0['MonHi']= dft0['Symbol'].apply(lambda x: hmon(x))

dft0['MonLow']= dft0['Symbol'].apply(lambda x: lmon(x))
dft0['52wkhi']=dft0['Symbol'].apply(lambda x: h52w(x))
dft0['52wklo']=dft0['Symbol'].apply(lambda x: l52w(x))
dft0['nearWKH'] = dft0.apply(lambda x: (1-x['Last Close'] / x['52wkhi']) * 100, axis=1)
dft0['nearWKL'] = dft0.apply(lambda x: (1-x['Last Close'] / x['52wklo']) * 100, axis=1)

dft0['Monthly Range%'] = dft0.apply(lambda x: ((x['MonHi'] / x['MonLow'])-1) * 100, axis=1)

dft0['52wk Range%'] = dft0.apply(lambda x: ((x['52wkhi'] / x['52wklo'])-1) * 100, axis=1)
dft0['Monthly Return%'] = dft0['Symbol'].apply(lambda x: returns(x, 'Month High Low (%)'))
dft0['1 Year Return%'] = dft0['Symbol'].apply(lambda x: returns(x, '1 Year High low(%)'))
dft0['3 Year Return%'] = dft0['Symbol'].apply(lambda x: returns(x, '3 Year High low(%)'))

dft0.fillna(0)
dft0.replace(to_replace = '-', value = 0, inplace=True)

dft0.replace(',','', regex=True, inplace=True)

dft0 = dft0.loc[:, ~dft0.columns.str.contains('^Unnamed')]
df1 = dft0[['Stock Name','Symbol','Sector', 'Last Close', 'Market Cap (Cr)', '52wkhi', '52wklo','nearWKH','nearWKL','52wk Range%','Monthly Range%','Monthly Return%', '1 Year Return%']].copy()
#df.columns = ['Stock Name','Symbol', 'Sector',  'Last Close', 'chg','chg%', 'Volume','Value', 'yearHigh','yearLow',
              #'return1y', 'return1m']
index_return = indret

df1['ret_multiple']= df1['1 Year Return%']/index_return

df1['RS_Rating'] = df1.ret_multiple.rank(pct=True) * 100

for col in df1.columns:
    if (col=="Symbol" or col=='Stock Name' or col=='Sector'):
        pass
    else:
        df1[col]= df1[col].astype(float)

df1=df1[df1['1 Year Return%']>0]
df1=df1[df1['nearWKL']<-25]
df1=df1[df1['nearWKH']<30]
df1=df1[df1['RS_Rating']>70]

df1=df1.sort_values(by=['1 Year Return%','nearWKH'], ascending=[False, True])

df2 = df1[df1['nearWKH']<12]

df3 =df1.sort_values(by=['Monthly Return%','nearWKH'], ascending=[False, True]).copy()
df3=df3[df3['nearWKH']<12]

st.subheader(titles[0])
st.write("Stocks - Ranked and sorted based Relative Strenth and nearness to 52week high.")
st.write("Relative strength is the rank with reference to returns of stock  vs index ")
st.write("Filtered stocks are above rank 70/100 and within 30% from 52 week high and 25% above 52 week low.")
st.write("Stocks nearness to 52 week high is set to max 12%")
#df2= df2.style.format({"Close": "{:.2f}"})



write_formatted(df2, 3)

#st.write(df2)
st.write('No. of records:' + str(len(df2)))

st.write("Momentum stocks sorted on the basis of last monthly return")
#df3= df3.style.format({"Close": "{:.2f}"})
write_formatted(df3, 3)

#st.write(df3)
st.write('No. of records:' + str(len(df3)))

st.subheader(titles[1])
#write_formatted(dft0, 1)

st.write(dft0)
