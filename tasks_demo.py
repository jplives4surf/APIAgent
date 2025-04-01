# tasks_demo.py
from agent import GitHubAPIAgent
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

agent = GitHubAPIAgent("github_openapi.json", github_token=GITHUB_TOKEN)

tasks = [
    "Get user info for octocat",
    "List repositories for user torvalds",
    "Get details of a repository called linux by torvalds"
]

for task in tasks:
    print(f"\n🧠 Task: {task}")
    result = agent.execute_task(task)
    print(result)

# Ask a question
print("\n🔍 Question: What endpoint is used to create a repo?")
print(agent.answer_question("What endpoint is used to create a repo?"))
