# introduction  // author: Divit Chandel
import streamlit as st
from openai import OpenAI
import json


# Configurations and Initializations
st.set_page_config(
    page_title="Uncencored AI Chatbot",
    page_icon="🏁",
    layout="centered",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- AI Setup ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Sidebar & info
with st.sidebar:
    st.title("🏁 Uncencored AI Chatbot")
    st.markdown(
        """
        ## Instructions
        - Type your question in the input box below.
        - Press Enter to get a response from the AI.
        
        ## Disclaimer
        This chatbot is for educational purposes only. The creators are not responsible for any misuse of the AI's responses.
        """
    )
    st.divider()
    st.write("**⚙️ Settings**")
    
    # SETTINGS
    system_instruction = st.text_area("Custom System Instruction", placeholder="e.g., You are a helpful assistant...")
    
    st.write(" ")

    # --- Upload and load previous chat ---
    uploaded_file = st.file_uploader("Load Chat (JSON)", type=["json"])
    if uploaded_file is not None:
        loaded_data = json.load(uploaded_file)
        if isinstance(loaded_data, list):
            st.session_state["messages"] = loaded_data
            st.success("✅ Chat loaded successfully!")
    
    # --- Download current chat ---
    if st.button("Download Chat as JSON", type="primary", icon="💾", width="stretch"):
        chat_json = json.dumps(st.session_state["messages"], indent=2)
        st.download_button(
            label="Click to Download",
            data=chat_json,
            file_name="chat_history.json",
            mime="application/json",
        )

    st.divider()

    # set defalt value to today
    st.date_input("", value="today", label_visibility="hidden")
    st.success(icon="✅", body=f"The bot is now ready to chat & convorse freely! last logged")

    # clear chat button
    if st.button("Clear chat", type="primary", icon="🗑️"):
        st.session_state["messages"] = []

    st.divider()
    

# main page start from here
chat_container = st.container(
        horizontal=False,
        horizontal_alignment="center",  # tf this doesn't work
        vertical_alignment="top",
        height=600,
        border=True,
    )

# initialize session state for messages
with st.spinner("Waiting for input..."):  # TODO: Make it's height long like double the default using custom css
    user_input = st.chat_input("Type your question here...", key="chat_input", accept_file=False)

    if user_input:
        # append user message
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # include system instruction (if any)
        messages_for_ai = []
        if system_instruction.strip():
            messages_for_ai.append({"role": "system", "content": system_instruction})

        # then add all chat messages
        messages_for_ai.extend(st.session_state["messages"])


        # --- AI CALL ---
        completion = client.chat.completions.create(
            extra_body={},
            model="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            messages=messages_for_ai,
        )
        ai_response = completion.choices[0].message.content

        # append AI message
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})

# render chat history (preserves across reruns)
with chat_container:
    for msg in st.session_state["messages"]:
        role = "human" if msg["role"] == "user" else "ai"
        with st.chat_message(role):
            st.markdown(msg["content"])
