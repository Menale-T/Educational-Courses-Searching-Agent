import os
import sys
import streamlit as st
from src.main import run


st.write("Welcome,I am a course finding assistant. Write the type of courses you want to learrn and I will find you the best matches from the web instantly with detailed information and recommendation.")
query = st.text_input("type here")

if query:
    waiting_msg = st.write(f"Searching {query} from web... ")

search_btn = st.button("Search",type="primary")
if search_btn:
    
    output = run(query)
    o_p = st.text_area(output)
    
