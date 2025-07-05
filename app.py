# app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8005"  # Make sure this matches your FastAPI port!

st.set_page_config(page_title="📄 RAG File Summarizer", layout="centered")
st.title("📄 DocDigest - File Summarizer + QA")
st.markdown("Upload a PDF to get a **summary** and ask a **question** based on the document.")

uploaded_file = st.file_uploader("📎 Upload a PDF", type=["pdf"])

if uploaded_file:
    file_bytes = uploaded_file.read()

    with st.spinner("📤 Uploading file and summarizing..."):
        files = {"file": (uploaded_file.name, file_bytes, "application/pdf")}
        try:
            
            response = requests.post(f"{API_URL}/summarize", files=files)
        except Exception as e:
            st.error(f"🚨 Error contacting API: {e}")
            st.stop()

    if response.status_code == 200:
        summary = response.json().get("summary", "")
        st.subheader("📌 Summary")
        st.success(summary)
    else:
        st.error("❌ Failed to get summary from backend.")
        st.stop()

    # Divider
    st.markdown("---")

    # QA Section
    st.subheader("💬 Ask a Question")
    question = st.text_input("What would you like to know from the document?")

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a valid question.")
        else:
            with st.spinner("🧠 Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/ask",
                        data={"question": question}
                    )
                except Exception as e:
                    st.error(f"🚨 Error contacting API: {e}")
                    st.stop()

            if response.status_code == 200:
                answer = response.json().get("answer", "")
                st.subheader("✅ Answer")
                st.info(answer)
            else:
                st.error("❌ Failed to get an answer from backend.")


st.subheader("📥 Export Flashcards to Anki (.apkg)")
if st.button("Export to Anki"):
    with st.spinner("📦 Generating Anki Deck..."):
        try:
            response = requests.post(f"{API_URL}/export-flashcards")
            if response.status_code == 200:
                url = response.json()["download_url"]
                st.success("Flashcards exported! Click below to download.")
                st.markdown(f"[⬇ Download Flashcards]({API_URL}{url})", unsafe_allow_html=True)
            else:
                st.error("Failed to generate Anki deck.")
        except Exception as e:
            st.error(f"Error exporting to Anki: {e}")
