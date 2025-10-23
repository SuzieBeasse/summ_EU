import streamlit as st
import streamlit.components.v1 as components
import requests

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
# Url API
url_query = "https://summeu-276701461247.europe-west1.run.app/query_vs"


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("Ask your question about EU debates here"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Query summeu with user input
    try:
        st.session_state.response = requests.get(
            url_query,
            params={"query": prompt}
        ).json()
    except:
        st.markdown("Hoho something went wrong")



# Display assistant response in chat message container
with st.chat_message("assistant"):
    if "response" in st.session_state:
        st.markdown(st.session_state.response['answer'])

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.response['answer']})
