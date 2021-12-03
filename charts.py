import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import talib
from PIL import Image

#image = Image.open('sunrise.jpg')
#st.image(image, caption='Sunrise', use_column_width=True)
#st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")

nifty_data= pd.read_csv('nifty200.csv')

st.title('Stock charts app')

st.sidebar.header('User Input')
add_selectbox = st.sidebar.selectbox(
    "Select the stock for  chart",
    nifty_data['Symbol']
)
#st.write("You have selected: " + add_selectbox)
def chart(df):
    candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['50sma'] = df['Close'].rolling(window=50).mean()

    sma20 = go.Scatter(x=df['Date'], y=df['20sma'], name='SMA20', line={'color': 'red'})
    sma50 = go.Scatter(x=df['Date'], y=df['50sma'], name='SMA50', line={'color': 'green'})

    fig = go.Figure(data=[candlestick, sma20, sma50])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    #fig.show()
    return fig
def chart2(df):
    mfi = talib.MFI(df['High'], df['Low'],df['Close'],df['Volume'],  timeperiod=10)
    mfi3 = talib.SMA(mfi, timeperiod=3)
    prices = df['Close'].values
    (macd, macds, macdh) =talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    rsi10 = talib.RSI(prices, timeperiod=10)

    rsi10line = go.Scatter(x=df['Date'], y=rsi10, name='RSI 10 line', line={'color': 'blue'})
    mfi10line = go.Scatter(x=df['Date'], y=mfi, name='MFI 10 line', line={'color': 'red'})
    mfi3line =  go.Scatter(x=df['Date'], y=mfi3, name='MFI 3SMA line', line={'color': 'orange'})
    fig2 = go.Figure(data=[rsi10line, mfi10line, mfi3line])

    fig2.layout.xaxis.type = 'category'
    fig2.layout.xaxis.rangeslider.visible = False
    #fig2.show()
    return fig2
#chart2(df)


if add_selectbox:
    symbol = add_selectbox
    st.write("You have selected: ", symbol)
    df = pd.read_csv('yearly/{}'.format(symbol)+'.csv')[-300:]

    st.header  = add_selectbox + '  Close \n'
    #st.line_chart(df['Close'])
    figc = chart(df)
    st.plotly_chart(figc, use_container_width=True)
    figc2 = chart2(df)
    st.plotly_chart(figc2, use_container_width=True)
    




#st.write("Candlestick Pattern Observed table1:")
#st.write(cpattern)
#st.add_selectbox.selected
st.write('Great! \n')


