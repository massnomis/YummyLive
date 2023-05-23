from streamlit_webrtc import webrtc_streamer
import av
import streamlit as st
net_placeholder = st.empty()
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    flipped = img[::-1,:,:]
    net_placeholder.write(flipped, channels="BGR")

    return av.VideoFrame.from_ndarray(flipped, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback)