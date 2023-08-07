import faiss
import numpy as np
import pandas as pd
import requests
import streamlit as st
import os
import json
from dotenv import load_dotenv
import time
# Set the page to wide layout
st.set_page_config(layout="wide")
# Read data from phone.xlsx
data = pd.read_excel('phone2.xlsx')

# Load the Faiss index and title vectors from files
index = faiss.read_index('index.faiss')
title_vectors = np.load('title_vectors.npy')

# Set up Streamlit app
st.title("大豐智慧分機表")
query = st.text_input("請輸入您的問題，將為您找到合適的人:")
load_dotenv()
if query:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENAI_KEY")}'  # Use the environment variable here
    }
    query_data = {
        "model": "text-embedding-ada-002",
        "input": [query]
    }
    response = requests.post('https://api.openai.com/v1/embeddings', headers=headers, json=query_data)
    response_data = response.json()
    query_vector = np.array(response_data['data'][0]['embedding'])

    # Search for nearest neighbors
    k = 5  # Number of nearest neighbors to retrieve
    distances, indices = index.search(np.array([query_vector]), k)

    # Retrieve the matched content
    matched_data = data.iloc[indices[0]]


    def replace_none_with_na(value):
        return '無' if pd.isnull(value) else value
        # Create two columns


    # Create two columns
    col1, col2 = st.columns(2)

    col1.subheader("最符合您問題的五位員工:")
    for i, row in matched_data.iterrows():
        row = row.apply(replace_none_with_na)
        html = """
        <div style="border:1px solid #000; margin:10px; padding:10px;">
            <h5>部門: {dept}</h5>
            <p>姓名: {name}</p>
            <p>分機: {ext}</p>
            <p>私人手機: {privatePhone}</p>
            <p>公務手機: {publicPhone}</p>
            <p>手機簡碼65+分機3碼: {easyCode}</p>
            <p>信箱: {email}</p>
        </div>
        """.format(dept=row['dept'], name=row['name'], ext=row['ext'], privatePhone=row['privatePhone'],
                   publicPhone=row['publicPhone'], easyCode=row['easyCode'], email=row['email'])
        col1.markdown(html, unsafe_allow_html=True)

    top_results_str = json.dumps(json.loads(matched_data.to_json(orient='records')), ensure_ascii=False)

    print(top_results_str)

    api_endpoint = "https://api.openai.com/v1/chat/completions"

    # Generate response using ChatGPT API
    response = requests.post(
        api_endpoint,
        headers={
            'Authorization': f'Bearer {os.getenv("OPENAI_KEY")}',
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "以下為json array 格式的參考資料: " + top_results_str},
                {"role": "assistant", "content": "您好，請問需要我為這些資料做什麼?"},
                {"role": "user", "content": "請根據提供的參考資料，回答以下問題應該要找哪一位人員回答:" + query
                                            + ",若資料沒有能夠回答問題請以下列字句回復: 目前尚無資料，請洽客服"}
            ],
            "temperature": 1,
            "top_p": 1,
            "n": 1
        }
    )
    col2.subheader("GPT生成回覆:")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'choices' in response.json():
        # Extract the generated response
        generated_response = response.json()["choices"][0]["message"]["content"]

        # Print the generated response
        print(generated_response)
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        with col2.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in generated_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        print("No response choices found.")
