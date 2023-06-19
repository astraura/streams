import streamlit as st
import streamlit.components.v1 as components

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import requests
import datetime as dt



nifty_data= pd.read_csv('nifty200.csv')

##Initiate Data
did_it_run = pd.read_csv('ran_once.csv')
did_it_run['Date']=pd.to_datetime(did_it_run['Date'])
last_update =did_it_run['Date'].values[0]

if did_it_run.loc[0,'Date']==dt.date.today():
    ran_already = True
    dft= pd.read_csv('nifty200 trendlyne.csv', index_col=[0])         
    dft0=dft.copy()
    #dft0.rename(columns = {'LTPLast Traded Price':'Last Close'}, inplace = True)
    #dft0.drop(['3M Price Chart'], axis=1, inplace=True,)
        
else: 
    ran_already= False
    #turl ='https://trendlyne.com/stock-screeners/fundamentals/ROCE_A_AVE_3/roce-annual-3yr-avg/highest/index/NIFTY200/nifty-200/'
    #turl ='https://trendlyne.com/stock-screeners/fundamentals/ROCE_A_AVE_3/roce-annual-3yr-avg/highest/index/NIFTY500/nifty-500/'
    turl = 'https://trendlyne.com/equity/1892/NIFTY200/nifty-200/'
    headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }

    rs0= requests.get(turl, headers = headers,timeout=5)
    #print(url)
    #sp = BeautifulSoup(rs.content, 'lxml')
    #sp = sp.replace("")
    
    #VP.at[j,'Symbol']=stocks[j]
    rs= rs0.text.replace("&nbsp","")
    dft = pd.read_html(rs)

    dft0=dft[0].copy()
    dft0.rename(columns = {'LTPLast Traded Price':'Last Close'}, inplace = True)
    dft0.drop(['3M Price Chart'], axis=1, inplace=True,)

def company2symbol(company):

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
    
nifty_list  = pd.read_csv("nse_symbols2.csv")
#nifty_list['ncompany']=nifty_list['ncompany'].apply(lambda x: x.strip())
sector_list = pd.read_csv("nifty500.csv")

dft0['Symbol']=dft0['Stock Name'].apply(lambda x: company2symbol(x))
dft0['Sector']=dft0['Symbol'].apply(lambda x: company2sector(x))
dft0['WkLow']= dft0['Symbol'].apply(lambda x: lweek(x))
dft0['MonHi']= dft0['Symbol'].apply(lambda x: hmon(x))

dft0['MonLow']= dft0['Symbol'].apply(lambda x: lmon(x))
dft0['52wkhi']=dft0['Symbol'].apply(lambda x: h52w(x))
dft0['52wklo']=dft0['Symbol'].apply(lambda x: l52w(x))
dft0['52wkhigap'] = dft0.apply(lambda x: (1-x['Last Close'] / x['52wkhi']) * 100, axis=1)
dft0['Monthly Range%'] = dft0.apply(lambda x: ((x['MonHi'] / x['MonLow'])-1) * 100, axis=1)

dft0['52wk Range%'] = dft0.apply(lambda x: ((x['52wkhi'] / x['52wklo'])-1) * 100, axis=1)
dft0['Monthly Return%'] = dft0['Symbol'].apply(lambda x: returns(x, 'Month High Low (%)'))
dft0['1 Year Return%'] = dft0['Symbol'].apply(lambda x: returns(x, '1 Year High low(%)'))
dft0['3 Year Return%'] = dft0['Symbol'].apply(lambda x: returns(x, '3 Year High low(%)'))

dft0.fillna(0)
dft0 = dft0.loc[:, ~dft0.columns.str.contains('^Unnamed')]
dfnew1 = dft0[['Symbol','Sector', 'Last Close','WkLow','MonHi','MonLow','52wkhi', '52wklo','52wkhigap','52wk Range%','Monthly Range%','Monthly Return%', '1 Year Return%', '3 Year Return%']].copy()

niftyscr = pd.DataFrame()
#dft1.to_csv('nifty trendlyne.csv')
#dft[0].to_csv('nifty200 trendlyne raw.csv')
if not ran_already:
    dft0.to_csv('nifty200 trendlyne.csv')
ran_once = pd.DataFrame()
ran_once.loc[0,'Date']=dt.date.today()
ran_once.to_csv('ran_once.csv', index=False)    

#st.write(str(last_update)
#st.write(ran_already)
#st.write(nifty_list.iloc[0,2])
#st.write(dft0)


def chart(symbol):
    imageurl='https://main.icharts.in/ShowChart.php?symbol={}&period=Daily&chart_size=400&log_chart=0&pr_period=3M&uind1=SMA&uind1_param=20&uind2=SMA&uind2_param=50'.format(symbol)
    #display(Image(url= imageurl))
    #![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)
    #urllib.request.urlretrieve(imageurl,"gfg.png")
    #image = Image.open('gfg.png')
    #st.image(image) 
    st.components.v1.iframe(imageurl, width=None, height=400, scrolling=False)









st.subheader('Stock Selection Analysis: Nifty 200 index stocks')
#genre = st.sidebar.radio(
#     "Select Analysis tables",
#    ('Filtered','Momentum Stocks', 'Swing Picks', 'Charts','Raw Data'))
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Filtered','Momentum Stocks', 'Swing Picks', 'Charts','Raw Data'])
    
#if genre == 'Filtered':
   # data = returns()
   # sorted_data = sorted_returns(data)
with tab1:
    st.subheader("Filtered on  the basis of Returns and gap to 52 week high")
    #st.write(sorted_data)
    gap52 =  float(st.text_input('Select maximum gap or fall from 52 week high %:  ',  12))
    ret1y  = float(st.text_input('Select minimum value values for 1 Year return %: ', 25))
    ret3y = float(st.text_input('Select minimum value values for 3 Year return %: ', 75))    
    monret = float(st.text_input('Select minimum 1 month return %',  7))

    #st.write('Values:', values)
    #st.write(values[1])
    #st.write(dft0)
    #st.write(data)
    
    niftyscr2 =dfnew1[dfnew1['52wkhigap'] <12 ]
    niftyscr2 =dfnew1[dfnew1['52wkhigap'] > 0 ]


    niftyscr2 = niftyscr2[niftyscr2['MonLow']>niftyscr2['52wklo']]
    niftyscr2 = niftyscr2[niftyscr2['WkLow']>niftyscr2['MonLow']]
    niftyscr2 = niftyscr2[niftyscr2['1 Year Return%']> ret1y ]
    niftyscr2 = niftyscr2[niftyscr2['Monthly Return%']> monret ]

    niftyscr2 = niftyscr2[niftyscr2['3 Year Return%']> ret3y]

    #niftyscr = niftyscr2
    st.write(niftyscr2)

with tab2:
#if genre == 'Momentum Stocks':

    st.subheader("Sorted Stock-selection on 1 month return, 1 year return and 52 week high gap ")
    dftop = int(st.text_input("Show top records: ",  30))
    niftyscr= dfnew1.copy()
    niftyscr2 = niftyscr.sort_values(by=['Monthly Return%','1 Year Return%',"52wkhigap"], ascending=[ False, False, True])
    st.write(niftyscr2.head(dftop))

with tab3:
#if genre == 'Swing Picks':
    values = st.slider(
    'Stocks with  range of  correction (gap) to 52 week high: ',
    0.0, 50.0, (5.0, 12.0))
    st.write('Correction % from 52 week high: ' + str(values[0]) + ' - ' + str(values[1]))
    niftyscr2= dfnew1.copy()
    nifty2 = niftyscr2[niftyscr2['52wkhigap'] >= values[0]]
    nifty2 = nifty2[nifty2['52wkhigap'] < values[1]]
    nifty2 = nifty2.sort_values(by=['Monthly Return%','1 Year Return%',"52wkhigap"], ascending=[ False, False, True])
    st.write(nifty2.head(15))

with tab4:
#if genre == 'Charts':
    st.subheader('Stock charts app')

    #st.header('Select Stock')
    complist = nifty_data['Symbol'].values.tolist()
    complist.insert(0,'Nifty')
    add_selectbox = st.selectbox(
        "Select the stock for  chart. or type in a few letters of symbol.",
        complist
    )

    if add_selectbox:
        symbol = add_selectbox
        company ="Nifty"
        if symbol != 'Nifty':
            company = nifty_data[nifty_data['Symbol']==symbol]['Company Name']
            company=company.values[0]
        
        #company = company['Company Name']
        st.write("You have selected: ", symbol)
        st.write(company)
        chart(symbol)

  

with tab5:
#if genre == 'Raw Data':
    #st.write("gompada")
    st.subheader("Database (Raw) of stocks last updated on: ")
    #st.write(str(last_update[0:10]))
    st.write(did_it_run['Date'].values[0])
    st.write(dft0)



    #st.write("UpDate is current. ", last_update)



#st.write("Candlestick Pattern Observed table1:")
#st.write(cpattern)
#st.add_selectbox.selected
st.write('Great! \n')


