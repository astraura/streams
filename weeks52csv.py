from io import StringIO

import requests
import pandas as pd
import streamlit as st
from datetime import datetime as dt
from bs4 import BeautifulSoup

df200 = pd.DataFrame()
df500 = pd.DataFrame()
method =[' 52 week high.',' moving averages.']
x=0
st.subheader("NSE Stock selection")

st.write( "Selection bases: 52 wk hi, 52 wk momentum, under Pullback, Volume Price expand, Moving averages, under Correction")
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
    url1 ='https://main.icharts.in/stock-lists/price-volume-expansions.html'
    url2 ='https://main.icharts.in/stock-lists/pullback-in-uptrends.html'
    pvdf =pd.read_html(url1)
    pvdf = pvdf[7]
    cols = pvdf.loc[0,:]
    pvdf.columns=cols
    pvdf= pvdf.loc[1:]
    pvdf.to_csv('Niftypv.csv')
    pvdf =pd.read_html(url2)
    pvdf = pvdf[7]
    cols = pvdf.loc[0,:]
    pvdf.columns=cols
    pvdf= pvdf.loc[1:]
    pvdf.to_csv('Niftypb.csv')


    curd = dt.now().strftime('%Y-%m-%d')

    data=[]
    updated = pd.DataFrame(data, columns=['Date'])
    updated.loc[0,'Date']= curd
    updated.to_csv('Updated2.csv')

    dftech = pd.read_csv("https://main.icharts.in/includes/screener/EODScan.php?export=1")
    #nifty200cos = pd.read_csv('nifty200.csv')[['Symbol','Company Name','Industry']]
    #dftech0 = dftech[dftech['p_symbol'].isin(nifty200cos['Symbol'])].copy()
    #niftycos=nifty200cos[nifty200cos['Symbol'].isin(dftech0['p_symbol'])]
    #dftech.rename(columns={'p_symbol':'Symbol'}, inplace=True)
    #dftech0=pd.merge(dftech0, niftycos)
    dftech.to_csv('Niftyma.csv')


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
    dfpv = pd.read_csv('Niftypv.csv',index_col=[0])
    dfpb = pd.read_csv('Niftypb.csv',index_col=[0])
    dftech = pd.read_csv('Niftyma.csv',index_col=[0])

else:
    df200 = pd.read_csv("Nifty_200tl.csv", index_col=[0])
    df500 = pd.read_csv("Nifty_500multitl.csv", index_col=[0])
    ret200 = pd.read_csv('Nifty200ret.csv')
    ret500 = pd.read_csv('Nifty500ret.csv')
    dfpv = pd.read_csv('Niftypv.csv',index_col=[0])
    dfpb = pd.read_csv('Niftypb.csv',index_col=[0])
    dftech = pd.read_csv('Niftyma.csv',index_col=[0])

genre = st.radio(
    "Select index for Analysis :  ",
    ('Nifty 200 Index',  'Nifty 500 Multicap Index'),horizontal=True)

if genre == 'Nifty 200 Index':
    titles= ["Nifty 200  picks ","Nifty 200 + stocks raw data"]
    df0= df200 # pd.read_csv("Nifty_200.csv", index_col=[0])
    indret = ret200.loc[0,'Return']
    nifty_list2 = pd.read_csv('nifty200.csv')

else:
    titles= ["Nifty 500 multicap (50:25:25) picks ","Nifty 500 multicap + stocks raw data"]
    df0= df500 # pd.read_csv("Nifty_500multi.csv", index_col=[0])
    indret = ret500.loc[0,'Return']
    nifty_list2 = pd.read_csv('NSE_symbols.csv')

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

def symbol2company(symbol):
    try:
        nifcomp = nifty_list[nifty_list['Symbol'].str.lower()==symbol.lower()]['Company Name']
        return nifcomp.values[0]

    except:
                
        return symbol


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

def chart(symbol):
    #st.write(symbol)
    #symbol.replace('&', '%26')
    if symbol=='M&M':
        symbol = 'M%26M'
    if symbol=='J&KBANK':
        symbol='J%26KBANK'    
    if symbol=='L&TFH':
        symbol=='L%26TFH'
    if symbol=='M&MFIN':
        symbol=='M%26MFIN'

    
    imageurl='https://main.icharts.in/ShowChart.php?symbol={}&period=Daily&chart_size=300&log_chart=0&pr_period=3M&uind1=SMA&uind1_param=20&uind2=SMA&uind2_param=50'.format(symbol)
    #display(Image(url= imageurl))
    #![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)
    #urllib.request.urlretrieve(imageurl,"gfg.png")
    #image = Image.open('gfg.png')
    #st.image(image) 
    st.components.v1.iframe(imageurl, width=None, height=250, scrolling=False)


def chart2(symbol):
    imageurl='https://main.icharts.in/ShowChart.php?symbol={}&period=Weekly&chart_size=300&log_chart=0&pr_period=1Y&uind1=SMA&uind1_param=10&uind2=SMA&uind2_param=30'.format(symbol)
    st.components.v1.iframe(imageurl, width=None, height=250, scrolling=False)


def write_formatted(dfx, except_cols):
    colnames=[]
    for col in dfx.columns:
        colnames.append(col)
    colnames=colnames[except_cols:]    
    st.dataframe(dfx.style.format(subset=colnames, formatter="{:.2f}"))

def write_formatted2(dfx):
    colnames=[]
    for col in dfx.columns:
        if col=="Symbol" or col=="Company" or col=="Sector" or col=="Stock":
            pass
        else:
            colnames.append(col)
    #colnames=colnames[except_cols:]    
    st.dataframe(dfx.style.format(subset=colnames, formatter="{:.2f}"))


nifty_list  = pd.read_csv("NSE_symbols.csv") #pd.read_csv("nse_symbols2.csv")
sector_list = pd.read_csv("NSE_symbols.csv")
st.write("Selection strategies / bases: ")
tab1, tab2, tab3, tab4, tab5 = st.tabs([' 52 weeks high ',' Pull Back ', ' Price Volume Expansion ', ' Moving Averages ', 'Charts'])

#st.markdown(
#    """<style>
#div[class*="stTabs"] > label > div[data-testid="stMarkdownContainer"] > p {
#    font-size: 32px;
#}
#    </style>
#    """, unsafe_allow_html=True)

with tab1:
    x=0
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
    df4 = df3.copy()
    df3=df3[df3['nearWKH']<=12]

    st.subheader(titles[0])
    st.write("Stocks - Ranked and sorted based Relative Strenth and nearness to 52week high.")
    st.write("Relative strength is the rank with reference to returns of stock  vs index ")
    st.write("Filtered stocks are above rank 70/100 and within 30% from 52 week high and 25% above 52 week low.")
    st.write("Stocks nearness to 52 week high is set to max 12%")
    #df2= df2.style.format({"Close": "{:.2f}"})



    write_formatted(df2, 3)

    #st.write(df2)
    st.write('No. of records:' + str(len(df2)))
    with st.expander("See Charts of top ten: "):
        

        count=0
        for stock in df2['Symbol']:
            #st.write("Charts of Top ten: ")

            msg =''
            #if df2[df2['Symbol']==stock]['pct_change_1_day'].values[0]>5:
            #    msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1
            if count==10:            
                break


    st.subheader("Momentum stocks sorted on the basis of last monthly return")
    #df3= df3.style.format({"Close": "{:.2f}"})
    write_formatted(df3, 3)

    #st.write(df3)
    st.write('No. of records:' + str(len(df3)))
    with st.expander("See Charts of top ten: "):
        

        count=0
        for stock in df3['Symbol']:
            #st.write("Charts of Top ten: ")

            msg =''
            #if df3[df3['Symbol']==stock]['pct_change_1_day'].values[0]>5:
                #msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1
            if count==10:            
                break
    
    #st.subheader("Stocks under correction for medium term value buying")

    #df4=df4[df4['RS_Rating']>70]
    #df4=df4[df4['nearWKH']<36.8]
    #df4 = df4[df4['nearWKH']>12]
    #df4 = df4[df4['Monthly Return%']>4]

    #st.write(df4)
    
    st.subheader(titles[1])
    #write_formatted(dft0, 1)

    st.write(dft0)

with tab2:
    x=1

    st.subheader("Stocks in uptrend under pull back: ")
    pbdfsel = dfpb[dfpb['Symbol'].isin(nifty_list2['Symbol'].values)]

    pbdfsel=pbdfsel[pbdfsel['LastClose']>pbdfsel['SMA(50)']]
    pbdfsel=pbdfsel[pbdfsel['LastClose']>pbdfsel['EMA(13)']]
    pbdfsel['LastClose']=pbdfsel['LastClose'].astype("float")
    pbdfsel['SMA(50)']=pbdfsel['SMA(50)'].astype("float")

    pbdfsel=pbdfsel[pbdfsel['LastClose']/pbdfsel['SMA(50)']<1.1]
    cols =pbdfsel.columns[0:7]
    pbdfsel = pbdfsel[cols]

    pbdfsel['Company']=pbdfsel['Symbol'].apply(lambda x: symbol2company(x))
    pbdfsel['Sector']=pbdfsel['Symbol'].apply(lambda x: company2sector(x))
    pbdfsel.insert(1,'Stock', pbdfsel.pop('Company'))

    write_formatted2(pbdfsel)
    #st.write(pbdfsel)
    count=0
    with st.expander("See Charts of top ten: "):

        for stock in pbdfsel['Symbol']:
            #st.write("Charts of Top ten: ")

            msg =''
            if pbdfsel[pbdfsel['Symbol']==stock]['% Chg(1 Day)'].values[0]>5:
                msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1
            if count==10:

                break
    st.subheader("Raw Data Pullback stocks")

    cols =dfpb.columns[0:7]
    df = dfpb[cols]
    df['Company']=df['Symbol'].apply(lambda x: symbol2company(x))
    df['Sector']=df['Symbol'].apply(lambda x: company2sector(x))
    #write_formatted2(df)

    st.write(df)
    
with tab3:

    st.subheader("Stocks showing Price Volume expansion and potential to rise: ")
    pvdfsel1 = dfpv[dfpv['Symbol'].isin(nifty_list2['Symbol'].values)]

    pvdfsel1=  pvdfsel1[pvdfsel1['LastClose']>pvdfsel1['SMA(50)']]
    pvdfsel1= pvdfsel1[pvdfsel1['LastClose']>pvdfsel1['EMA(13)']]
    pvdfsel1['LastClose']=pvdfsel1['LastClose'].astype("float")
    pvdfsel1['SMA(50)']=pvdfsel1['SMA(50)'].astype("float")

    pvdfsel1=pvdfsel1[pvdfsel1['LastClose']/pvdfsel1['SMA(50)']<1.1]
    cols =pvdfsel1.columns[0:7]
    #cols[8]='RS_Rating'
    pvdfsel1 = pvdfsel1[cols]


    pvdfsel1['Company']=pvdfsel1['Symbol'].apply(lambda x: symbol2company(x))
    pvdfsel1['Sector']=pvdfsel1['Symbol'].apply(lambda x: company2sector(x))
    pvdfsel1.insert(1,'Stock', pvdfsel1.pop('Company'))

    write_formatted2(pvdfsel1)

    #st.write(pvdfsel1)
    with st.expander("See Charts of top ten: "):

        count=0
        for stock in pvdfsel1['Symbol']:
            #st.write("Charts of Top ten: ")

            msg =''
            if pvdfsel1[pvdfsel1['Symbol']==stock]['% Chg(1 Day)'].values[0]>5:
                msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1
            if count==10:
                
                break



    st.subheader("Raw Data Price Volume Expansion")
    cols =dfpv.columns[0:7]
    df = dfpv[cols]
    df['Company']=df['Symbol'].apply(lambda x: symbol2company(x))
    df['Sector']=df['Symbol'].apply(lambda x: company2sector(x))
    
    #write_formatted2(df)
    st.write(df)

with tab4:
    st.subheader("Selection based on Moving Averages: ")
    dfi = dftech.copy()
    dfi = dftech.drop(columns=['trix', 'candle'])
    dfi.rename(columns={'p_symbol':'Symbol'}, inplace=True)
    dfi = dfi[dfi['Symbol'].isin(nifty_list2['Symbol'].values)]
    dfi['ret_multiple']= dfi['pct_change_1_year']/index_return
    dfi['RS_Rating'] = dfi.ret_multiple.rank(pct=True) * 100
    dfi =dfi[dfi['RS_Rating']>70]

    dfi2 = dfi.copy()
    dfi3= dfi.copy()
    dfi=dfi[dfi['sma_50'] > dfi['sma_200']]
    #dfi=dfi[dfi['sma_13'] > dfi['sma_20']]
    dfi=dfi[dfi['last_close']>dfi['sma_50']]
    dfi=dfi[dfi['last_close']>dfi['sma_20']]
    dfi=dfi[dfi['sma_20']>dfi['sma_50']]

    dfi=dfi[dfi['pct_change_1_day']>0]
    #dfi= dfi[dfi['last_close']-dfi['sma_20']<dfi['atr']*1.5]
    dfi['prev_close']=dfi['last_close']-dfi['last_close']*dfi['pct_change_1_day']/100
    dfi=dfi[(dfi['prev_close']<dfi['sma_20']) | (dfi['prev_close']<dfi['sma_50']) | (dfi['prev_close']<dfi['sma_13'])]
    
    #dfi=dfi[(dfi['prev_close']<dfi['sma_20']) | (dfi['prev_close']<dfi['sma_50']) 
                    #| (dfi['last_close']-dfi['atr'])<dfi['sma_20'] | (dfi['last_close']-dfi['atr'])<dfi['sma_50'] ]

    dfi=dfi[dfi['last_volume']>dfi['avg_volume']]
    cols =dfi.columns[0:9]
    dfi = dfi[cols]
    write_formatted2(dfi)

    with st.expander("See Charts of top ten: "):


        count=0
        for stock in dfi['Symbol']:
            #st.write("Charts of Top ten: ")

            msg =''
            if dfi[dfi['Symbol']==stock]['pct_change_1_day'].values[0]>5:
                msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1

            if count==10:            
                break


    st.subheader("Stocks under correction and near Moving Averages.")

    dfi2=dfi2[dfi2['sma_50'] > dfi2['sma_200']]
    dfi2=dfi2[dfi2['last_close']>dfi2['sma_50']]
    dfi2=dfi2[dfi2['pct_change_1_day']>0]
    dfi2['prev_close']=dfi2['last_close']-dfi2['last_close']*dfi2['pct_change_1_day']/100
    dfi2=dfi2[ (dfi2['prev_close']<dfi2['sma_50'])| (dfi2['prev_close']<dfi2['sma_20'])]
    #dfi2=dfi2[dfi2['last_volume']>dfi2['avg_volume']]
    cols =dfi2.columns[0:9]
    dfi2 = dfi2[cols]
    write_formatted2(dfi2)
    with st.expander("See Charts of top ten: "):

        count=0
        for stock in dfi2['Symbol']:
            #st.write("Charts of Top ten: ")
            msg =''
            if dfi2[dfi2['Symbol']==stock]['pct_change_1_day'].values[0]>5:
                msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1
            if count==10:            
                break

    st.subheader("Raw Data ")
    #dfi2=dfi2[dfi2['last_volume']>dfi2['avg_volume']]
    cols =df3.columns[0:15]
    dfi = df3[cols]

    st.write(dfi3)



with tab5:

    st.subheader('Stock charts app')

    #st.header('Select Stock')
    complist = nifty_list['Symbol'].values.tolist()
    complist.insert(0,'Nifty')
    add_selectbox = st.selectbox(
        "Select the stock for  chart. or type in a few letters of symbol.",
        complist
    )

    if add_selectbox:
        symbol = add_selectbox
        company ="Nifty"
        if symbol != 'Nifty':
            company = nifty_list[nifty_list['Symbol']==symbol]['Company Name']
            company=company.values[0]
        
        #company = company['Company Name']
        st.write("Daily / Weekly charts: ", symbol)
        st.write(company)
        chart(symbol)
        chart2(symbol)
