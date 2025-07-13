import io
import streamlit as st
import litellm

from clear_confirn_dialog import confirm_deletion
from markdown_export import convert_chat_to_markdown
from system_prompts import smart_goals, check_in

system_prompts_map = {
    "SMART Goals": smart_goals,
    "Check-in": check_in,
    "Custom": "",
}

# Set Streamlit page config
st.set_page_config(layout="wide")

# --- SIDEBAR (Master view) ---
with st.sidebar:
    st.title("Mentoring GPTs")
    st.subheader("Your robot mentoring assistant")

    # General API key input
    general_api_key = st.text_input("LLM API Key", type="password")

    st.markdown("### LiteLLM Settings")
    st.text("LiteLLM is a library that allows you to use most LLMs via the same interface. You just need to choose a model and add your credentials. You can even run your local LLM via Ollama")
    llm_api_key = st.text_input("LiteLLM API Key", type="password")
    model = st.text_input("Model (e.g., gpt-4, llama2)", value="gpt-4")
    hostname = st.text_input("Hostname (for self-hosted)", value="http://localhost:11434")
    stage = st.text_input("Stage (for Azure deployments)", value="dev")

    st.markdown("### Choose Custom GPT")
    custom_gpt = st.selectbox(
        "Custom GPT",
        options=list(system_prompts_map.keys()),
        index=0,
    )

    system_prompt = system_prompts_map[custom_gpt] if custom_gpt in system_prompts_map else ""

    st.divider()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.messages:
        md_content = convert_chat_to_markdown(st.session_state.messages)
        buffer = io.BytesIO(md_content.encode("utf-8"))
        st.download_button(
            label="📥 Export Chat as Markdown",
            data=buffer,
            file_name="chat_history.md",
            mime="text/markdown"
        )

    # --- CLEAR CHAT HISTORY ---

    # --- Initialize confirmation dialog flag ---
    if "show_clear_dialog" not in st.session_state:
        st.session_state.show_clear_dialog = False

    # --- Button to trigger dialog ---
    if st.button("🗑️ Clear Chat History"):
        st.session_state.show_clear_dialog = True

    # --- Dialog UI ---
    if st.session_state.show_clear_dialog:
        confirm_deletion("Are you sure you want to clear the chat history? This action cannot be undone.")

# --- MAIN AREA (Detail view / Chat) ---
st.header(f"Chat with {custom_gpt}")

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- LLM Response via LiteLLM ---
    try:
        # Setup LiteLLM config dynamically
        litellm.api_key = llm_api_key or general_api_key
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ],
            api_base=hostname if hostname else None
        )

        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
