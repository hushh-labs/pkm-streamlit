import streamlit as st
import requests
import json

# Set the FastAPI endpoint URL
API_URL = "https://graphrag-neo4j-53407187172.us-central1.run.app/query"

# Title of the chatbot application
st.title("Your Personal Knowledge Model")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to send query to FastAPI and get a response
def get_response_from_api(query):
    try:
        params = {"hushh_id": 'cc15533b-48b4-4ea2-b53c-e788ab175f2f', "query": query}
        response = requests.get(API_URL, params=params)
        print(f"Raw response: {response.text}")  # Log raw response for debugging
        if response.status_code == 200:
            try:
                response_json = response.json()  # Ensure response is parsed as JSON
                if isinstance(response_json, dict):  # Check if the response is a dictionary
                    answer = response_json.get('answer', "No answer found in response")
                    return answer
                else:
                    return "Error: API response is not a valid JSON object."
            except json.JSONDecodeError:
                return "Error: Received invalid JSON from the API."
        else:
            return f"Error: {response.status_code} - {response.reason}"
    except Exception as e:
        return f"Error: {str(e)}"

# Accept user input
if prompt := st.chat_input("Type your query here..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response from the API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response_from_api(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
