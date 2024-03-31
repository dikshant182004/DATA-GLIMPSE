import streamlit as st
from streamlit.script_runner import RerunException
import streamlit.components.v1 as components

# Install experimental reroute module
components.declare_component("reroute", url="http://localhost:3001")

def main():
    st.title("Page Navigation Example")
    
    if st.button("Go to Another Page"):
        # Trigger navigation to another page
        components.reroute("/other-page")

if __name__ == "__main__":
    main()