import streamlit as st
import requests

st.set_page_config(page_title="Resume AI Agent", page_icon="🤖")
st.title("🤖 Resume Improvement Agent")
st.caption("Using Qwen 2 0.5B + LangChain")

BACKEND_URL = "http://localhost:8000"

# --- Automatic Upload Logic ---
uploaded_file = st.file_uploader("Drop your resume PDF here", type="pdf")

if uploaded_file:
    # Use session state to ensure we only upload ONCE per file
    if "last_uploaded" not in st.session_state or st.session_state["last_uploaded"] != uploaded_file.name:
        with st.spinner("Processing PDF automatically..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                res = requests.post(f"{BACKEND_URL}/upload", files=files)
                if res.status_code == 200:
                    st.session_state["ready"] = True
                    st.session_state["last_uploaded"] = uploaded_file.name
                    st.toast("Resume processed!")
                else:
                    st.error("Upload failed.")
            except Exception as e:
                st.error(f"Connection error: {e}")

# --- Suggestions Section ---
st.divider()
if st.session_state.get("ready"):
    if st.button("✨ Get Expert Suggestions", type="primary", use_container_width=True):
        with st.spinner("Analyzing with local AI..."):
            try:
                res = requests.post(f"{BACKEND_URL}/suggestions")
                data = res.json()
                if "suggestions" in data:
                    st.markdown("### 💡 Expert Feedback")
                    st.info(data["suggestions"])
                else:
                    st.error(data.get("error"))
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Waiting for PDF upload...")