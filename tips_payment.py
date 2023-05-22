from wallet_connect import wallet_connect
import streamlit as st
# connect_button = wallet_connect(label="wallet", key="wallet")
# send_transaction = wallet_connect(label="send", key="send", message="Send Transaction", contract_address="ERC20_ADDRESS", amount="10", to_address="RECIPIENT_ADDRESS")
import web3 
st.set_page_config(layout="wide")


st.title("Wallet Connect")


addy = wallet_connect(label="wallet", key="wallet", chain_name='goerli')
if addy:
    st.write("your address is: ", addy)
else:
    st.write("not connected")


send = wallet_connect(label="send", key="send", message="Send Transaction", contract_address="0xE205181Eb3D7415f15377F79aA7769F846cE56DD", amount="0.0001", to_address="0xba2ef5189b762bd4c9e7f0b50fbbab65193935e8", contract_type="ERC20")

# use web3 py to see if the transaction was successful
# look 



