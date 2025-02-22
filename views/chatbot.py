import requests
import streamlit as st

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HUGGINGFACE_API_KEY = "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"

def get_response(text):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text}
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

    try:
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            return response_json[0].get("generated_text", "Sorry, I couldn't generate a response.")
        elif "error" in response_json:
            return f"Error: {response_json['error']}"
        else:
            return "Unexpected response format from API."
    except Exception as e:
        return f"API Error: {str(e)}"

st.title("🤖 Chatbot")

user_input = st.text_input("Ask me anything...")
if st.button("Send"):
    response = get_response(user_input)
    st.write("Bot:", response)
