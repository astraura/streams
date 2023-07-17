from io import StringIO

import requests
import pandas as pd
import streamlit as st
from datetime import datetime as dt
from bs4 import BeautifulSoup
import numpy as np
import plotly.express as px
import time


df200 = pd.DataFrame()
df50 = pd.DataFrame()
dfc = pd.DataFrame()
dfcx1 = pd.DataFrame()
dfcx0 = pd.DataFrame()
dfc0= pd.DataFrame()
dfc1 = pd.DataFrame()
Newlist =[]
PBlist =[]
dfstat = pd.DataFrame()
files = ["Nifty500 52wkNewHigh.csv","Nifty500 52wkFiltered.csv"]
file = files[0]

st.subheader("NSE Stock selection")
st.write("Index Used: Nifty Multicap 300 40:40:20 (Nifty 200 + Small cap 50) ")
st.write( "Selection bases: 52 wk hi, 52 wk Momentum, under Pullback, registering New Highs")
file =""
#data ={'scan_clause': '( {cash} ( market cap > 3000 and latest low < latest sma( latest close , 20 ) and latest close / latest sma( latest close , 20 ) < 1.02 and latest close / latest sma( latest close , 20 ) > 0.95 and latest close > latest sma( latest close , 50 ) and latest sma( latest close , 50 ) >= latest sma( latest close , 200 ) and latest sma( latest close , 20 ) > latest sma( latest close , 50 ) ) ) '}

#cdatas =[]
#cdatas[0] = pd.DataFrame()

#def getFirst():

def getNifty(niftyapiurl, csvfile, csv2):


    headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    with requests.session() as req:
        


        #api0=req.get(niftyapiurl,headers = headers)
        api0= req.get(niftyapiurl, headers = headers,timeout=5)
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
        #req.close()




def GetDataFromChartink(payload):
    Charting_Link = "https://chartink.com/screener/"
    Charting_url = 'https://chartink.com/screener/process'

    payload = {'scan_clause': payload}

    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)

        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
        return df

def getChartink():
    #url0='https://chartink.com/screener/copy-52-week-high-stocks-3625'

    #You need to copy paste condition in below mentioned Condition variable

    #Condition = "( {57960} ( [0] 15 minute close > [-1] 15 minute max ( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma ( volume,20 ) ) ) "


    #Condition = "( {33489} ( latest volume > latest sma( latest volume , 10 ) * 2 ) )" 
    Condition0 = "( {57960} ( latest high = latest max( 260 , latest high ) ) ) "
    Condition1 = '( {57960} ( latest open >=  weekly max( 52 , weekly high ) * 0.85 and 1 day ago close < weekly max( 52 , weekly high ) and latest high < weekly max( 52 , weekly high ) and 1 day ago volume > 1 day ago sma( latest volume , 7 ) and latest close > 1 day ago close and latest sma( latest close , 200 ) < latest close and latest sma( latest close , 50 ) <= latest close and latest sma( latest close , 50 ) > 1 week ago sma( 1 week ago close , 50 ) and latest close / latest sma( latest close , 20 ) < 1.015 and latest volume > 10000 ) ) '
    #Condition2 ='( {46553} ( latest open >= weekly max( 52 , weekly high ) * 0.85 and 1 day ago volume > 10000 and yearly "close - 1 candle ago close / 1 candle ago close * 100" > 15 ) ) '
    #Condition3 = " ( {46553} ( latest high = latest max( 260 , latest high ) ) ) "

    #files = ["Nifty500 52wkNewHigh.csv","Nifty500 52wkFiltered.csv"]
    #file=files[0]
    conditions =[Condition0,Condition1]
    for condition in conditions:
        if condition == Condition0:
            msg = "New 52week highs"
            file=files[0]
        else:
            msg = "Pullback stocks.. "
            file=files[1]
           
        with st.spinner('Wait. Gathering {}..'.format(msg) ):
    

            data = GetDataFromChartink(condition)

            data = data.sort_values(by='per_chg', ascending=False)
            data.to_csv(file)    
            #cdatas.append(data)
            time.sleep(5)

    #return cdatas

def gatherData():
    #dffilter = getChartink()

    niftyapiurl1='https://trendlyne.com/equity/1892/NIFTY200/nifty-200/'
    #niftyapiurl2 = "https://trendlyne.com/equity/910418/NFT500MULT/nifty-500-multicap-50-25-25/"
    niftyapiurl2 ='https://trendlyne.com/equity/910396/SMALLCAP50/nifty-smallcap-50/'
    getNifty(niftyapiurl1, 'Nifty_200tl.csv','Nifty200ret.csv')
   
    getNifty(niftyapiurl2, 'Nifty_50stl.csv','Nifty50sret.csv')

    curd = dt.now().strftime('%Y-%m-%d')

    data=[]
    updated = pd.DataFrame(data, columns=['Date'])
    updated.loc[0,'Date']= curd
    updated.to_csv('Updated3.csv')



dfd = pd.read_csv("Updated3.csv")
last_update = pd.to_datetime(dfd[-1:]['Date'].values[0])

curd = dt.now().strftime('%Y-%m-%d')
data =[]
dtdf = pd.DataFrame(data, columns=['Date'])
dtdf.loc[0,'Date']= curd
curdate = pd.to_datetime(dtdf[-1:]['Date'].values[0])
#curdate
#if pd.Timestamp.now()>last_update:

steps =['Getting Data..', 'Gathering New Highs..','Looking for Pullbacks..']
if curdate  >last_update:
    #getFirst()
    with st.spinner('Wait.  Data needs updation. Gathering 52 weeks data... '):
        gatherData()

    #cdatas = getChartink()
    getChartink()

    df200 = pd.read_csv("Nifty_200tl.csv", index_col=[0])
    df50 = pd.read_csv("Nifty_50stl.csv", index_col=[0])
    ret200 = pd.read_csv('Nifty200ret.csv')
    ret50 = pd.read_csv('Nifty50sret.csv')

    df0= pd.concat([df200,df50], ignore_index=True)
    #df500 # pd.read_csv("Nifty_500multi.csv", index_col=[0])
    indret = (ret50.loc[0,'Return'] + ret200.loc[0,'Return'])/2
    nifty_list = pd.read_csv('NSE_symbols.csv')
    dfc0 =  pd.read_csv("Nifty500 52wkNewHigh.csv", index_col=[0])  #cdatas[0]
    dfc1 =  pd.read_csv("Nifty500 52wkFiltered.csv", index_col=[0])  #cdatas[1]
    Newlist = dfc0['nsecode'].values
    PBlist =  dfc1['nsecode'].values
    #dffilter = pd.read_csv("Chartink.csv", index_col=[0])

else:
    df200 = pd.read_csv("Nifty_200tl.csv", index_col=[0])
    df50 = pd.read_csv("Nifty_50stl.csv", index_col=[0])
    ret200 = pd.read_csv('Nifty200ret.csv')
    ret50 = pd.read_csv('Nifty50sret.csv')

    df0= pd.concat([df200,df50], ignore_index=True)
    #df500 # pd.read_csv("Nifty_500multi.csv", index_col=[0])
    indret = (ret50.loc[0,'Return'] + ret200.loc[0,'Return'])/2

    nifty_list = pd.read_csv('NSE_symbols.csv')
    #dfc0 = cdatas[0]
    #dfc1 = cdatas[1]
    dfc0 =  pd.read_csv("Nifty500 52wkNewHigh.csv", index_col=[0])  #cdatas[0]
    dfc1 =  pd.read_csv("Nifty500 52wkFiltered.csv", index_col=[0])  #cdatas[1]

    Newlist = dfc0['nsecode'].values
    PBlist =  dfc1['nsecode'].values


    



#st.write(''curdate)
st.write('Uptated on:  '  + str(curdate)[0:10])
#st.write(last_update)
st.write('Index return 1 year:  ' + str(indret) +'%') 

#print(df)
dft0 = df0.copy()
#df.replace(to_replace = '-', value = 0, inplace=True)
dft0.rename(columns = {'LTPLast Traded Price':'Last Close'}, inplace = True)
if '3M Price Chart' in dft0.columns:
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

    
    imageurl='https://main.icharts.in/ShowChart.php?symbol={}&period=Daily&chart_size=400&log_chart=0&pr_period=3M&uind1=SMA&uind1_param=20&uind2=SMA&uind2_param=50'.format(symbol)
    #display(Image(url= imageurl))
    #![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)
    #urllib.request.urlretrieve(imageurl,"gfg.png")
    #image = Image.open('gfg.png')
    #st.image(image) 
    st.components.v1.iframe(imageurl, width=None, height=250, scrolling=False)


def chart2(symbol):
    imageurl='https://main.icharts.in/ShowChart.php?symbol={}&period=Weekly&chart_size=400&log_chart=0&pr_period=1Y&uind1=SMA&uind1_param=10&uind2=SMA&uind2_param=30'.format(symbol)
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
        if col=="Symbol" or col=="Company" or col=="Sector" or col=="Stock" or col=="nsecode" or col=="bsecode" or col=='sr' or col=='name':
            pass
        else:
            colnames.append(col)
    #colnames=colnames[except_cols:]    
    st.dataframe(dfx.style.format(subset=colnames, formatter="{:.2f}"))


nifty_list  = pd.read_csv("NSE_symbols.csv") #pd.read_csv("nse_symbols2.csv")
sector_list = pd.read_csv("NSE_symbols.csv")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([' 52 weeks high data ',' New 52 week highs ',' Swing Picks ', 'Stats', 'Charts' ,'Other apps'])

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
    df1['Market Cap (Cr)']=pd.to_numeric(df1['Market Cap (Cr)'])
               
    dfstat= dft0.copy()

    #dfstat= df1.copy()
    #df1.to_csv("Nifty500data.csv")

    index_return = indret

    df1['ret_multiple']= df1['1 Year Return%']/index_return

    df1['RS_Rating'] = df1.ret_multiple.rank(pct=True) * 100
    dfcx0 = df1.copy()  
    dfcx1 = df1.copy()
   
    for col in df1.columns:
        if (col=="Symbol" or col=='Stock Name' or col=='Sector'):
            pass
        else:
            df1[col]= df1[col].astype(float)

    df1=df1[df1['1 Year Return%']>0]
    df1=df1[df1['Monthly Return%']>0]
    
    df1=df1[df1['nearWKL']<-25]
    df1=df1[df1['nearWKH']<30]
    df1=df1[df1['RS_Rating']>70]
    df2 = df1[df1['nearWKH']<12]
    df2 = df1[df1['nearWKH']>5]



    df3 =df1.sort_values(by=['nearWKH'], ascending=[False]).copy()
    df3=df3[df3['nearWKH']<=12]
    df3=df3[df3['nearWKH']>=5]

    df4 = df3.copy()


    #st.subheader(titles[0])
    st.write("Stocks - Ranked and sorted based Relative Strenth and nearness to 52week high.")
    st.write("Relative strength is the rank with reference to returns of stock  vs index ")
    st.write("Filtered stocks are above rank 70/100 and within 30% from 52 week high and 25% above 52 week low.")
    st.write("Stocks nearness to 52 week high is set to min 5% max 12%")
    #df2= df2.style.format({"Close": "{:.2f}"})


    df2=df2.sort_values(by=['nearWKH'], ascending=[False])

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
    df3=df3.sort_values(by=['nearWKH'], ascending=[False])

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
    
    #st.subheader(titles[1])
    #write_formatted(dft0, 1)
    st.subheader("NSE 500 Raw Data: ")
    st.write(dft0)

with tab2:
    st.write('Stocks showing new 52 week highs')
    dfcx0 =  dfcx0[dfcx0['Symbol'].isin(Newlist)].copy()
    for col in dfcx0.columns:
        if (col=="Symbol" or col=='Stock Name' or col=='Sector'):
            pass
        else:
            dfcx0[col]= dfcx0[col].astype(float)    
    dfcx0 = dfcx0[dfcx0['RS_Rating']>70]
    dfcx0 = dfcx0.sort_values(by=["RS_Rating"], ascending=False)

    write_formatted(dfcx0, 3)

    #st.write(df3)
    st.write('No. of records:' + str(len(dfcx0)))
    with st.expander("See Charts of top ten: "):
        

        count=0
        for stock in dfcx0['Symbol']:
            #st.write("Charts of Top ten: ")

            msg =''
            #if df3[df3['Symbol']==stock]['pct_change_1_day'].values[0]>5:
                #msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1
            if count==10:            
                break            
    #st.write(dfcx0)
    #st.write(dfc0)

with tab3:
    x=1
    #getFirst()
    st.subheader("Stocks  in uptrend under pull back: ")
    st.write("Stocks near the support of moving averages 20 / 50 days. ")
    dfcx1 =  dfcx1[dfcx1['Symbol'].isin(PBlist)].copy()
    for col in dfcx1.columns:
        if (col=="Symbol" or col=='Stock Name' or col=='Sector'):
            pass
        else:
            dfcx1[col]= dfcx1[col].astype(float)    

    dfcx1 = dfcx1.sort_values(by=["RS_Rating"], ascending=False)

    write_formatted(dfcx1, 3)

    #st.write(df3)
    st.write('No. of records:' + str(len(dfcx1)))
    with st.expander("See Charts of top ten: "):
        

        count=0
        for stock in dfcx1['Symbol']:
            #st.write("Charts of Top ten: ")

            msg =''
            #if df3[df3['Symbol']==stock]['pct_change_1_day'].values[0]>5:
                #msg= "(Price expansion is more than average. Care!! )"
            st.write(stock  + ' ' + msg)
            chart(stock)
            count +=1
            if count==10:            
                break            


    #st.write(dfcx1)
    #st.write(dfc1)


with tab4:
    #dfstat = dft0[['Stock Name','Symbol','Sector', 'Last Close', 'Market Cap (Cr)', '52wkhi', '52wklo','nearWKH','nearWKL','52wk Range%','Monthly Range%','Monthly Return%', '1 Year Return%']].copy()
    dfstat.replace(to_replace = '-', value = 0, inplace=True)

    dfstat.replace(',','', regex=True, inplace=True)
    dfstat['Market Cap (Cr)']=pd.to_numeric(dfstat['Market Cap (Cr)'])

    dfgr = dfstat.groupby('Sector')
    dfgr3 = dfgr.agg(np.mean)

    dfgr4=dfgr3[["Market Cap (Cr)","52wk Range%","Monthly Range%", "1 Year Return%","Monthly Return%"]].copy()
    dfgr4.rename(columns = {'Monthly Return%':'Last month Return%'}, inplace = True)
    dfgr4=dfgr3.sort_values(by=["1 Year Return%"], ascending=False)
    dfgr4["Sector Name"] =dfgr4.index
    fig = px.pie(dfgr4, values="Market Cap (Cr)", names="Sector Name")
    #fig.show()
    st.write(dfgr4)
    st.write("Chart showing Market Cap ranks (investment flow) sector wise")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.pie(dfgr4, values="1 Year Return%", names="Sector Name")
    st.write("Chart showing Investment appreciation  ranks (returns) sector wise")
    st.plotly_chart(fig, use_container_width=True)

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


with tab6:
    
    #https://streams-b6t5fcv8kjf.streamlit.app/
    #streams ∙ main ∙ charts-ta32.py
    url = "https://share.streamlit.io/astraura/streams/main/weeks52csv.py"
    url2 = "https://share.streamlit.io/astraura/streams/main/charts-ta32.py"
    url3 = "https://share.streamlit.io/astraura/streams/main/weeks52_500.py"
    #st.write("check out similar app  [link](%s)" % url)

    st.markdown("Check out similar apps for [52 weeek analysis Nifty 200 / Nifty 500  link](%s)" % url)
    
    st.markdown("Check out [Nifty 200   Stock Analysis   link](%s)" % url2)