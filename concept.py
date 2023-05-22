import streamlit as st

st.title("Live Cooking Show")
st.write("Yummy Lives")




st.markdown("## Concept")
st.markdown(
    """
    This is a rundown of an app that combined food delivery and a live cooking show.


    ### Food Delivery
    The app will allow users to order food from a list of restaurants. 
    The app will also allow users to interact with a live cooking show.
    Within the cooking show, users can add tips and send messages to the chef.
    Live orders are diplayed publically so all users can see what others are ordering.
    There will be a priority queue for the chef to see what orders to cook first, based on the time the order was placed and the amount of tips the user has sent.
    """
)
st.title("Components")

st.markdown(
    """
    The Live Cooking Show
    
    This will be a live stream of the chef cooking the food.
    This will be using streamlit's built in video player.
    """
)

st.markdown(
    """
    The order Matching System 

    This will be a priority queue that will be used to determine what order to cook first.
    This will be using websockets and a rest api for the backend.
    There will be a weight for each order that will be calculated by the time the order was placed and the amount of tips the user has sent.
    The live queue will be displayed on the screen for all users to see.
    """
)

st.markdown(
    """
    Tips and Gifts System   



    This will be a system that allows users to send tips and gifts to the chef.
    This will be done using streamlit and metamask to send the tips and gifts.
    Users will have to send the tips and gifts in the form of USDC on polygon.
    An api key for infura will be needed to connect to the polygon network.
    This will also pick up the users metamask wallet address, as well as the timestamp of the transaction, as well as the amounts sent.
    
    
    """
)






