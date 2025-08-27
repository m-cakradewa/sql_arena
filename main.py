import streamlit as st
import sqlite3
import pandas as pd
import tutorial
import challenges
from streamlit import session_state as ss

if "page" not in ss:
    ss.page = "tutorial"

def goto_tutorial():
    ss.page = "tutorial"

def goto_challenges():
    ss.page = "challenges"

if "db" not in ss:
    ss.db = "ecommerce"
with st. container(border=1):
    nav1,nav2 = st.columns(2, gap = "large")
    with nav1:
        st.markdown("<div style='text-align: center'><h3>Core Tutorial</h3>", unsafe_allow_html=True)
        c,c1,c = st.columns([.5,1,.5])
        with c1:
            st.image("tutorial.jpeg")
        st.info(
        "This section contains step-by-step SQL tutorials. Each tutorial explains a core SQL concept "
        "and gives you a chance to try it out right away. Expand any card to see the explanation and test your queries.")
        st.write("")
        st.button("Open Tutorial Page", on_click = goto_tutorial, use_container_width = True)

    with nav2:
        st.markdown("<div style='text-align: center'><h3>Real-World Challenges</h3>", unsafe_allow_html=True)
        c,c1,c = st.columns([.5,1,.5])
        with c1:
            st.image("challenges_2.jpeg")
        st.warning(
        "Ready to test your skills? These challenges are designed to help you apply what you've learned in real-world-like scenarios. "
        "Try to solve them on your own using SQL. Expand a challenge to get started.")
        st.write("")
        st.button("Go To Challenges", on_click = goto_challenges, use_container_width = True)
    st.write("")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
if ss.page == "tutorial":
    st.markdown(
    "<h2 style='text-align: center; font-style: italic;'>SQL CORE TUTORIAL</h2>", 
    unsafe_allow_html=True)
    level = tutorial.page()
    if level == "Advanced - Deployment Ready":
        if st.button("Take me to the challenges!", use_container_width = True):
            ss.page = "challenges"
            st.rerun()
elif (ss.page == "challenges"):
    st.markdown(
    "<h2 style='text-align: center; font-style: italic;'>SQL REAL WORLD CHALLENGES</h2>", 
    unsafe_allow_html=True)
    scores = challenges.page()



