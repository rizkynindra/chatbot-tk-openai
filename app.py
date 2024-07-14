from openai import OpenAI
import streamlit as st
import toml

secrets = toml.load("streamlit/secrets.toml")
client = OpenAI(api_key=secrets["OPENAI_API_KEY"])
st.title("Chat Bot BPJSTK")

# client.api_key = secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0125:bpjs-ketenagakerjaan::9kYHphv8"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:bpjs-ketenagakerjaan::9kYHphv8",
            messages=[
                {
                    # "role": "system",
                    # "content": [
                    #     {
                    #         "type": "text",
                    #         "text": "Kamu adalah seorang customer service BPJS Ketenagakerjaan yang ramah. Jawablah pertanyaan - pertanyaan seputar BPJS Ketenagakerjaan. Jika ada pertanyaan diluar BPJS Ketenagakerjaan silakan jawab dengan 'Maaf saya tidak mengerti, saya hanya bisa membantumu dengan informasi seputar BPJS Ketenagakerjaan'. Jawablah pertanyaan sesuai dengan Bahasa yang digunakan dalam pertanyaan dan jawablah pertanyaan layaknya kamu berbicara dengan manusia."
                    #     }
                    # ],

                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            if response.choices[0].delta.content:
                full_response += response.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})