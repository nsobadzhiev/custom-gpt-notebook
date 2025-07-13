import streamlit as st

@st.dialog("Confirm Deletion")
def confirm_deletion(dialog_message: str):
    st.write(dialog_message)
    if st.button("✅ Yes, clear it"):
        st.session_state.messages.clear()
        st.session_state.show_clear_dialog = False
        st.toast("Chat history cleared.", icon="🧹")
        st.rerun()
    if st.button("❌ Cancel"):
        st.session_state.show_clear_dialog = False
        st.rerun()
