import streamlit as st
import sys
import os
sys.path.append(".")
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Auto & Laptop Manual Assistant",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Automotive & Laptop Manual Assistant")
st.caption("Ask questions about Toyota Fortuner, Innova Crysta, Dell, HP and Lenovo manuals")

@st.cache_resource
def load_rag():
    from src.rag_chain import ask, retriever
    return ask

ask = load_rag()

with st.sidebar:
    st.header("📊 Index Info")
    st.metric("PDFs indexed", "5")
    st.metric("Total pages", "1,290")
    st.metric("Total chunks", "3,977")
    st.metric("Embedding model", "MiniLM-L6-v2")
    st.metric("LLM", "LLaMA 3.1 (Groq)")
    st.divider()
    st.caption("Manuals covered:")
    st.caption("🚗 Toyota Fortuner 2025")
    st.caption("🚗 Toyota Innova Crysta 2024")
    st.caption("💻 Dell Inspiron 15 3000")
    st.caption("💻 HP Laptop")
    st.caption("💻 Lenovo ThinkPad X250")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg:
            with st.expander("📄 View Sources"):
                for s in msg["sources"]:
                    st.caption(f"• {s}")

if prompt := st.chat_input("Ask about your vehicle or laptop..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching manuals..."):
            answer, sources = ask(prompt)
        st.markdown(answer)
        with st.expander("📄 View Sources"):
            for s in sources:
                st.caption(f"• {s}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })