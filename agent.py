# agent.py
import json
import requests
import openai
from typing import Optional

class GitHubAPIAgent:
    def __init__(self, openapi_path: str, github_token: Optional[str] = None):
        with open(openapi_path, 'r') as f:
            self.schema = json.load(f)
        self.base_url = "https://api.github.com"
        self.token = github_token

    def get_headers(self):
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def execute_task(self, task_description: str) -> dict:
        """ Use GPT to choose endpoint and generate correct request """
        prompt = f"""
        You are an API expert. You are using the GitHub REST API.
        The user wants to: "{task_description}"

        Based on the OpenAPI spec, suggest:
        1. HTTP method
        2. Endpoint path
        3. Example URL
        4. Example headers
        5. Example JSON body (if needed)

        OpenAPI paths: {list(self.schema['paths'].keys())[:40]}

        Return as JSON object like:
        {{
          "method": "GET",
          "path": "/users/{{username}}",
          "url": "https://api.github.com/users/octocat",
          "headers": {{}},
          "body": null
        }}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        plan = json.loads(response['choices'][0]['message']['content'])
        return self.make_request(plan)

    def make_request(self, plan: dict) -> dict:
        print(f"\n[Calling] {plan['method']} {plan['url']}")
        resp = requests.request(
            plan['method'],
            plan['url'],
            headers={**self.get_headers(), **plan.get('headers', {})},
            json=plan.get('body')
        )
        try:
            return resp.json()
        except Exception:
            return {"error": "Failed to parse response", "status": resp.status_code}

    def answer_question(self, question: str) -> str:
        """ Use GPT to answer a question about the API """
        prompt = f"""
        You are the GitHub API assistant. Using the following OpenAPI paths:
        {list(self.schema['paths'].keys())[:50]}

        Answer this question: "{question}"
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
