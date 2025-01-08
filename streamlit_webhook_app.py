import streamlit as st
import time
import requests

# Streamlit app
st.title("Webhook Streaming Data")

st.subheader("Incoming Webhook Data")
data_placeholder = st.empty()

# Function to fetch data from the Flask server
def fetch_webhook_data():
    try:
        url = "http://localhost:5100/get_webhook"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Return the list of webhook data
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Real-time data streaming
while True:
    webhook_data_list = fetch_webhook_data()  # Fetch data from the Flask server

    # Display the data
    with data_placeholder.container():
        if webhook_data_list:
            st.write("### Latest Webhook Data")
            for item in webhook_data_list:
                st.json(item)
        else:
            st.write("Waiting for incoming data...")

    # Update every 2 seconds
    time.sleep(2)
