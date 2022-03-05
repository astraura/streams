import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import yfinance as yf
import time
from datetime import  datetime as dt
from copy import deepcopy
from ftplib import FTP



path = 'data/'
#driver = webdriver.Chrome()
#chrome_options.add_argument("--headless")


nifty_data= pd.read_csv('nifty200.csv')
tickers = nifty_data['Symbol'].to_list()
df = pd.DataFrame()
df = pd.read_csv('data/ZEEL.csv')
df_new = yf.download('ZEEL.NS', period='1d' )
latest = df_new.index.values[0]
def snapshot():
    my_bar = st.progress(0)
    i=1
    #with open('nifty100.csv') as f:

    for stock in tickers:
        with st.spinner('Wait.. {}'.format(stock)):

        #st.spinner('Wait..updated.' + symbol)
       
        #if "," not in line:
        #    continue
            symbol =  stock  #line.split(",")[2]
            #data = yf.download(symbol+'.NS', start="2020-01-01", end="2020-08-01")
            data = yf.download(symbol+'.NS', period='3y' )
            data.to_csv('data/{}.csv'.format(symbol))

            #df= pd.read_csv('data/{}.csv'.format(symbol))

            my_bar.progress( round(i/len(nifty_data)*100))
            i+=1
            #if i>10:
            #    break

    st.success("Done!..")
            

        #st.write (symbol+'.NS')

    nifty= yf.download('^NSEI',period='3y')
    nifty.to_csv('data/^NSEI.csv')

    return {"Updation: ": "Success!" }





def get_rs_df():
    index_name = '^NSEI' # S&P 500
    returns_multiples = []

    # Index Returns
    index_df = pd.read_csv(path+'^NSEI.csv') 
    #pdr.get_data_yahoo(index_name, start_date, end_date)
    index_df['Percent Change'] = index_df['Adj Close'].pct_change()
    index_return = (index_df['Percent Change'] + 1).cumprod()[-1:].values[0]
    prices =[]
    pivots = {}
    datayday=[]


    # Find top 30% performing stocks (relative to the S&P 500)
    for ticker in tickers:
        # Download historical data as CSV for each stock (makes the process faster)
        df = pd.read_csv(path+ticker+'.csv')
        datayday.append(calc_pivots(df,pivots,ticker))
        # Calculating returns relative to the market (returns multiple)
        df['Percent Change'] = df['Adj Close'].pct_change()
        stock_return = (df['Percent Change'] + 1).cumprod()[-1:].values[0]
    
        returns_multiple = round((stock_return / index_return), 2)
        returns_multiples.extend([returns_multiple])
        
        #print (f'r: {ticker}; Returns Multiple against Nifty 200: {returns_multiple}\n')
        #time.sleep(1)
        #stock_data[ticker]=df
    # Creating dataframe of only top 30%
    #data_sets = pd.DataFrame(stock_data)
    rs_df = pd.DataFrame(list(zip(tickers, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
    rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
    rs_df.to_csv("Nse200_RS.csv")
    rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]

    # Checking Minervini conditions of top 30% of stocks in given list
    #rs_stocks = rs_df['Ticker']
    dataframe3 = pd.DataFrame(datayday)
    dataframe3 = PPSR(dataframe3)
    dataframe3 = WPPSR(dataframe3)
    dataframe3 = MPPSR(dataframe3)
    dataframe3.to_csv('pivots.csv')
    return rs_df
def get_export_list(rs_df):
    rs_stocks = rs_df['Ticker']
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "Price", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
    #exportList2 = pd.DataFrame(columns=['Stock', "RS_Rating", "Price", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

    for stock in rs_stocks:    
        try:
            #ticker = path + stock
            df = pd.read_csv(f'{path+stock}.csv', index_col=0)
            sma = [50, 150, 200]
            for x in sma:
                df["SMA_"+str(x)] = round(df['Adj Close'].rolling(window=x).mean(), 2)
            
            # Storing required values 
            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52week = round(min(df["Low"][-260:]), 2)
            high_of_52week = round(max(df["High"][-260:]), 2)
            RS_Rating = round(rs_df[rs_df['Ticker']==stock].RS_Rating.tolist()[0])
            exportList2 = exportList.append({'Stock': stock, "RS_Rating": RS_Rating ,"Price":currentClose, "50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)
        
            try:
                moving_average_200_20 = df["SMA_200"][-20]
            except Exception:
                moving_average_200_20 = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            condition_1 = currentClose > moving_average_150 > moving_average_200
            
            # Condition 2: 150 SMA and > 200 SMA
            condition_2 = moving_average_150 > moving_average_200

            # Condition 3: 200 SMA trending up for at least 1 month
            condition_3 = moving_average_200 > moving_average_200_20
            
            # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            condition_4 = moving_average_50 > moving_average_150 > moving_average_200
            
            # Condition 5: Current Price > 50 SMA
            condition_5 = currentClose > moving_average_50
            
            # Condition 6: Current Price is at least 30% above 52 week low
            condition_6 = currentClose >= (1.3*low_of_52week)
            
            # Condition 7: Current Price is within 25% of 52 week high
            condition_7 = currentClose >= (.75*high_of_52week)
            
            # If all conditions above are true, add stock to exportList
            if(condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7):
                exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating ,"Price":currentClose, "50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)
                #print (stock + " made the Minervini requirements")
        except Exception as e:
            #print (e)
            print(f"Could not gather data on {stock}")
            continue

    exportList = exportList.sort_values(by='RS_Rating', ascending=False)
    #print('\n', exportList)
    exportList.to_csv("Nse200_Momentum.csv")
    #exportList2.to_csv("Nse200_RS.csv")
    #return exportList

def Asc50(df):
    df['50sma'] = df['Close'].rolling(window=50).mean()
    sma50_10 =df[-40:-39]['50sma'].values[0]
    sma50_05 =df[-10:-9]['50sma'].values[0]
    sma50_00 =df[-1:]['50sma'].values[0]
    if sma50_10<=sma50_05 and sma50_05<=sma50_00:
        return "Asc50"
    elif sma50_10>=sma50_05 and sma50_05>=sma50_00:
        return "Dsc50"
    else:
        return  "Flat"

def calcLevels(df):
    def isSupport(df,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
            and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support
    def isResistance(df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
            and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance

    def isFarFromLevel(l):
        s =  np.mean(df['High'] - df['Low'])
        return np.sum([abs(l-x) < s  for x in levels]) == 0
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]
            if isFarFromLevel(l):
                levels.append((i,l))
        elif isResistance(df,i):
            l = df['High'][i]
            if isFarFromLevel(l):
                levels.append((i,l))

    return levels

def PPSR(data):
    PP = pd.Series((data['High'] + data['Low'] + data['Close']) / 3)
    R1 = pd.Series(2 * PP - data['Low'])
    S1 = pd.Series(2 * PP - data['High'])
    R2 = pd.Series(PP + data['High'] - data['Low'])
    S2 = pd.Series(PP - data['High'] + data['Low'])
    R3 = pd.Series(data['High'] + 2 * (PP - data['Low']))
    S3 = pd.Series(data['Low'] - 2 * (data['High'] - PP))
    psr = {'S3':S3, 'S2':S2, 'S1':S1, 'PP':PP, 'R1':R1,  'R2':R2,  'R3':R3}
    PSR = pd.DataFrame(psr)
    data= data.join(PSR)
    return data

def WPPSR(data):
    PP = pd.Series((data['WHigh'] + data['WLow'] + data['WClose']) / 3)
    R1 = pd.Series(2 * PP - data['WLow'])
    S1 = pd.Series(2 * PP - data['WHigh'])
    R2 = pd.Series(PP + data['WHigh'] - data['WLow'])
    S2 = pd.Series(PP - data['WHigh'] + data['WLow'])
    R3 = pd.Series(data['WHigh'] + 2 * (PP - data['WLow']))
    S3 = pd.Series(data['WLow'] - 2 * (data['WHigh'] - PP))
    psr = {'WS3':S3, 'WS2':S2, 'WS1':S1, 'WPP':PP, 'WR1':R1,  'WR2':R2,  'WR3':R3}
    PSR = pd.DataFrame(psr)
    data= data.join(PSR)
    return data

def MPPSR(data):
    PP = pd.Series((data['MHigh'] + data['MLow'] + data['MClose']) / 3)
    R1 = pd.Series(2 * PP - data['MLow'])
    S1 = pd.Series(2 * PP - data['MHigh'])
    R2 = pd.Series(PP + data['MHigh'] - data['MLow'])
    S2 = pd.Series(PP - data['MHigh'] + data['MLow'])
    R3 = pd.Series(data['MHigh'] + 2 * (PP - data['MLow']))
    S3 = pd.Series(data['MLow'] - 2 * (data['MHigh'] - PP))
    psr = {'MPP':PP, 'MR1':R1, 'MS1':S1, 'MR2':R2, 'MS2':S2, 'MR3':R3, 'MS3':S3}
    PSR = pd.DataFrame(psr)
    data= data.join(PSR)
    return data
#@app.route('/calc')
def calc_pivots(df, pivots,stock):

    #n = -1


    if df.empty:
        return "N/A"
    pivots['Symbol'] = stock
    pivots['Date'] = df.tail(1)['Date'].values[0]
    pivots['Open'] = df.tail(1)['Open'].values[0]
    pivots['High'] = df.tail(1)['High'].values[0]
    pivots['Low'] = df.tail(1)['Low'].values[0]
    pivots['Close'] = df.tail(1)['Close'].values[0]

    supports= calcLevels(df)
    try:
        pivots['MA50'] = Asc50(df)
        if len(supports)>0:
            pivots['S_R1'] = supports[-1:][0][1]
        if len(supports)>1:
            pivots['S_R2'] = supports[-2:-1][0][1]
        else:
            pivots['S_R2'] = 0
        if len(supports)>2:
            pivots['S_R3'] = supports[-3:-2][0][1]
        else:
            pivots['S_R3'] = 0
    except:
        pivots['Support'] = 0
#weekly Data extraction
    f=df.copy()
    f['Date'] = pd.to_datetime(f['Date'])
    f.set_index('Date')
    f.sort_index(inplace=True)
    logic = {'Open'  : 'first',
            'High'  : 'max',
            'Low'   : 'min',
            'Close' : 'last',
            'Volume': 'sum'}
    df3 = f.resample('W', on='Date').apply(logic)
    #df3.index -= to_offset("6D")

    pivots['WOpen'] =  df3[-2:-1]['Open'].values[0]
    pivots['WHigh'] =  df3[-2:-1]['High'].values[0]
    pivots['WLow']  =  df3[-2:-1]['Low'].values[0]
    pivots['WClose'] = df3[-2:-1]['Close'].values[0]

    df4 = f.resample('M', on='Date').apply(logic)
    pivots['MOpen'] =  df4[-2:-1]['Open'].values[0]
    pivots['MHigh'] =  df4[-2:-1]['High'].values[0]
    pivots['MLow']  =  df4[-2:-1]['Low'].values[0]
    pivots['MClose'] = df4[-2:-1]['Close'].values[0]
    #datayday.append(deepcopy(pivots))
    return deepcopy(pivots)



st.subheader('Data updation: Nifty 200 index stocks')
last_update = pd.to_datetime(df[-1:]['Date'].values[0])
day1 = dt.now()
today = day1.date()
yday = dt(today.year,today.month,today.day-1)
#today = pd.to_datetime("today")
yday2 = pd.Timestamp(today.year,today.month,today.day-1)
if latest==yday2:
    st.write("current date is: ", today,latest)
st.write("Database of stocks last updated on:", last_update)
if latest>last_update:
    #st.write("Data is very old needing updation.  Date: ", latest)
    #st.write(latest)
    x=snapshot()
    x= "Data Updated"
    st.write(x)

else:
    st.write("Updated.. Date is current. ", today)
if st.button("Update database"):  

    st.warning('Warning. Page visits external sites to update data. Please wait. It may take sometime.')

    #get_funda_data()
    if latest>last_update:

        x=snapshot()
        x= "Data Updated"
        st.write(x)
    else:
        st.write("UpDate is current. ", last_update)

rs_df = get_rs_df()
get_export_list(rs_df)
#st.write("Candlestick Pattern Observed table1:")
#st.write(cpattern)
#st.add_selectbox.selected

url = st.secrets["url"]
username = st.secrets["username"]
password = st.secrets["password"]
session = FTP(url,username,password)

file = open('pivots.csv','rb')                  # file to send
remotefile = 'httpdocs/stocks/pivots.csv'
session.storbinary('STOR '+remotefile, file)     # send the file
#session.storlines('STOR %s' % 'remotefile.txt', f)  
file.close()   


file = open('Nse200_Momentum.csv','rb')                  # file to send
remotefile = 'httpdocs/stocks/Nse200_Momentum.csv'
session.storbinary('STOR '+remotefile, file)     # send the file
#session.storlines('STOR %s' % 'remotefile.txt', f)  
file.close()   
#ftp_server = FTP('ftp.astraura.in','snm','Gompada2021#')
file = open('Nse200_RS.csv','rb')                  # file to send
remotefile = 'httpdocs/stocks/Nse200_RS.csv'
session.storbinary('STOR '+remotefile, file)     # send the file
#session.storlines('STOR %s' % 'remotefile.txt', f)  
file.close()   
# close file and FTP
session.quit()
st.write('Done. Great! \n')


