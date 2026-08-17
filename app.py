import streamlit as st
import json
import os

st.set_page_config(page_title="SRIIAGI Security Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ SRIIAGI — AI Red-Teaming & Security Dashboard")
st.markdown("Aapke custom AI security framework ka interactive dashboard.")

# Sidebar controls
st.sidebar.header("Configuration")
model_name = st.sidebar.text_input("Model Name", value="llama3")
base_url = st.sidebar.text_input("Base URL", value="http://localhost:11434/v1")

if st.sidebar.button("Run Security Assessment"):
    st.sidebar.info("Tests running... Please check your terminal for live logs.")
    # Terminal command backend trigger
    exit_code = os.system(f"python runner.py --base-url {base_url} --model {model_name}")
    if exit_code == 0:
        st.sidebar.success("Assessment Completed Successfully!")
    else:
        st.sidebar.error("Error occurred during execution.")

st.markdown("---")
st.subheader("📊 Latest Assessment Report")

# Check if report.md exists
if os.path.exists("report.md"):
    with open("report.md", "r") as f:
        report_content = f.read()
    st.markdown(report_content)
else:
    st.warning("Abhi tak koi report generate nahi hui hai. Side menu se assessment run karein!")