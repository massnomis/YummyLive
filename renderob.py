
import streamlit as st
import requests
import pandas as pd
import uuid
import plotly.express as px
import plotly.graph_objects as go
import time
st.set_page_config(layout="wide")
st.title('ABC/USD Order Book')

response = requests.get('http://localhost:9999/orderbook/')
order_book = response.json()
with st.expander('Order Book'):
    st.write(order_book)
buy_orders = pd.DataFrame(order_book['buy'])
sell_orders = pd.DataFrame(order_book['sell'])

fig = go.Figure(data=[
    go.Bar(name='Buy', x=buy_orders['price'], y=buy_orders['quantity'], marker_color='rgb(0, 255, 0)'),
    go.Bar(name='Sell', x=sell_orders['price'], y=sell_orders['quantity'], marker_color='rgb(255, 0, 0)')
])
# make it red and green
# fig.update_traces(marker_color=['red', 'green'])


# Change the bar mode
fig.update_layout(barmode='group')

st.plotly_chart(fig, use_container_width=True)
import base64

# ...

# Create an HTTP Basic Auth header
username = "alice"
password = "password"
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}

# Create some limit orders
for i in range(50):
    order = {
        "id": str(uuid.uuid4()),
        "type": "buy" if i % 2 == 0 else "sell",
        "price": 100 + i * 10,
        "quantity": 10
    }
    requests.post('http://localhost:9999/order/', json=order, headers=headers)
    time.sleep(1)  # Wait for a second to ensure orders are processed in the correct order
response = requests.get('http://localhost:9999/orderbook/')
order_book = response.json()
with st.expander('Order Book'):
    st.write(order_book)
buy_orders = pd.DataFrame(order_book['buy'])
sell_orders = pd.DataFrame(order_book['sell'])

fig = go.Figure(data=[
    go.Bar(name='Buy', x=buy_orders['price'], y=buy_orders['quantity'], marker_color='rgb(0, 255, 0)'),
    go.Bar(name='Sell', x=sell_orders['price'], y=sell_orders['quantity'], marker_color='rgb(255, 0, 0)')
])
# make it red and green
# fig.update_traces(marker_color=['red', 'green'])


# Change the bar mode
fig.update_layout(barmode='group')

st.plotly_chart(fig, use_container_width=True)
# Create some market orders
for i in range(5):
    order = {
        "id": str(uuid.uuid4()),
        "type": "buy" if i % 2 == 0 else "sell",
        "price": None,
        "quantity": 10
    }
    requests.post('http://localhost:9999/order/', json=order, headers=headers)
    time.sleep(1)  # Wait for a second to ensure orders are processed in the correct order

# Fetch and display the order book
response = requests.get('http://localhost:9999/orderbook/', headers=headers)
order_book = response.json()

# ...

# Fetch and display the order history
response = requests.get('http://localhost:9999/orderhistory/', headers=headers)
order_history = response.json()
st.write(order_history)
# chart it


st.plotly_chart(px.scatter(order_history, x='timestamp', y='price', size='quantity'), use_container_width=True)


# ...
