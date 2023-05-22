from streamlit_server_state import server_state, server_state_lock
from streamlit_webrtc import ClientSettings, WebRtcMode, webrtc_streamer
import streamlit as st
from fastapi import FastAPI, WebSocket
from typing import List



app = FastAPI()

def main():
    st.code(server_state)
    # server_state is a module-level object that is shared across all sessions
    # of the Streamlit app. You can use it to store and access user-specific
    # information.
    # lets print the current value of server_state

    try:
        if "webrtc_contexts" not in server_state:
            server_state["webrtc_contexts"] = []
    except:
        try:
            if "webrtc_contexts" not in server_state:
                server_state["webrtc_contexts"] = {}
        except:
            if len(server_state.__dict__) == 0:
                st.session_state["webrtc_contexts"] = {}

    self_ctx = webrtc_streamer(
        key="self",
        mode=WebRtcMode.SENDRECV,
        client_settings=ClientSettings(
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
            media_stream_constraints={"video": True, "audio": True},
        ),
        sendback_audio=False,
    )

    with server_state_lock["webrtc_contexts"]:
        webrtc_contexts = server_state["webrtc_contexts"]
        if self_ctx.state.playing and self_ctx not in webrtc_contexts:
            webrtc_contexts.append(self_ctx)
            server_state["webrtc_contexts"] = webrtc_contexts
        elif not self_ctx.state.playing and self_ctx in webrtc_contexts:
            webrtc_contexts.remove(self_ctx)
            server_state["webrtc_contexts"] = webrtc_contexts

    active_other_ctxs = [
        ctx for ctx in webrtc_contexts if ctx != self_ctx and ctx.state.playing
    ]

    for ctx in active_other_ctxs:
        webrtc_streamer(
            key=str(id(ctx)),
            mode=WebRtcMode.RECVONLY,
            client_settings=ClientSettings(
                rtc_configuration={
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                },
                media_stream_constraints={
                    "video": True,
                    "audio": True,
                },
            ),
            source_audio_track=ctx.output_audio_track,
            source_video_track=ctx.output_video_track,
            desired_playing_state=ctx.state.playing,
        )
    # st.write(ctx.output_video_track)
    # st.write(ctx.output_audio_track)
    # st.write(ctx.state.playing)
    # st.write(ctx.state)
    # st.write(ctx)
    # st.write(self_ctx)
    # st.write(active_other_ctxs)
    # st.write(webrtc_contexts)
    # # st.write(server_state_lock)
    # st.write(server_state_lock["webrtc_contexts"])
    st.write(webrtc_streamer)
    

main()