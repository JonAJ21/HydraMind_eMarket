import streamlit as st

st.set_page_config(
    page_title="Главная"
)

st.title("Главная")

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = ""


if "counter" not in st.session_state:
    st.session_state['counter'] = 0
    
if st.button("Increment"):
    st.session_state.counter += 1
    st.write(f"{st.session_state.counter}")

if st.button("reset"):
    st.session_state.counter = 0
else:
    st.write(f"did not reset")


# st.write(f"{st.session_state.access_token}")
