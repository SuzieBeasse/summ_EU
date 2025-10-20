import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="summ_eu", # => Quick reference - Streamlit
    page_icon="🇪🇺",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

# Then continue with your app
st.title(" __Summ EU__ "
         )

st.sidebar.markdown(f'''# Welcome to __Summ EU__''')
st.sidebar.markdown(f'''
                    ## Your European Parliament transcripts querying assistant''')
st.sidebar.markdown(f"""
                    Enter a question about European debates and politics to get started

                    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("What were the latest environmental policies discussed?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

response = "" # Needs to be the response from the API

# Display assistant response in chat message container
with st.chat_message("assistant"):
    st.markdown(response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})
