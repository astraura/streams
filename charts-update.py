import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import yfinance as yf
import time
from datetime import  datetime as dt

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
            my_bar.progress( round(i/len(nifty_data)*100))
            i+=1
            #if i>10:
            #    break
    st.success("Done!..")
            

        #st.write (symbol+'.NS')

    nifty= yf.download('^NSEI',period='3y')
    nifty   .to_csv('data/^NSEI.csv')

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
    # Find top 30% performing stocks (relative to the S&P 500)
    for ticker in tickers:
        # Download historical data as CSV for each stock (makes the process faster)
        df = pd.read_csv(path+ticker+'.csv')

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
    rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]

    # Checking Minervini conditions of top 30% of stocks in given list
    #rs_stocks = rs_df['Ticker']
    return rs_df
def get_export_list(rs_df):
    rs_stocks = rs_df['Ticker']
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "Price", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

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
    exportList.to_csv("Nse 200 Momentum.csv")

    return exportList

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


#st.write("Candlestick Pattern Observed table1:")
#st.write(cpattern)
#st.add_selectbox.selected
st.write('Great! \n')


