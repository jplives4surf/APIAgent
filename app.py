# app.py
import streamlit as st
from agent import GitHubAPIAgent
import os
import openai
import json

# 🔐 Sidebar input for keys
openai_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
github_token = st.sidebar.text_input("🔐 GitHub Token (optional)", type="password")

if openai_key:
    openai.api_key = openai_key

# Load the agent with schema
agent = GitHubAPIAgent("github_openapi.json", github_token=github_token)

st.set_page_config(page_title="GitHub API Agent", layout="wide")
st.title("🤖 GitHub API Agent")
st.markdown("Ask questions or give tasks like: `Get user info for octocat`, `List repos for torvalds`, etc.")

tab1, tab2 = st.tabs(["🔧 Execute Task", "❓ Ask About API"])

with tab1:
    task = st.text_input("🧠 Describe a task", value="Get user info for octocat")

    if st.button("Execute Task"):
        with st.spinner("Thinking..."):
            try:
                response = agent.execute_task(task)
                st.success("✅ API Call Successful!")
                st.subheader("📦 Response")
                st.json(response)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    question = st.text_input("❓ Ask a question about the GitHub API", value="What endpoint is used to create a repo?")

    if st.button("Answer Question"):
        with st.spinner("Searching docs..."):
            try:
                answer = agent.answer_question(question)
                st.markdown(f"**💡 Answer:** {answer}")
            except Exception as e:
                st.error(f"Error: {e}")
