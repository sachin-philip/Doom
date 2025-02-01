import streamlit as st
from src.pages.app import render_bot_page

def main():
    st.set_page_config(page_title="Doom Chat", page_icon="🤖")
    render_bot_page()

if __name__ == "__main__":
    main()