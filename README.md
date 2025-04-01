# 🤖 GitHub API Agent

An intelligent agent that reads the GitHub REST API spec and lets you:
- 🧠 Execute natural language tasks (e.g. "Get user info for octocat")
- ❓ Ask questions about the API (e.g. "How do I create a repo?")
- 🌐 Use via Streamlit UI

## 🚀 Run It

1. Clone the repo

```bash
git clone https://github.com/jplives4surf/APIAgent.git
cd APIAgent

pip install -r requirements.txt

curl -o github_openapi.json https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json

streamlit run app.py

export OPENAI_API_KEY=your-key
export GITHUB_TOKEN=your-github-token
