import requests

API_URL = "https://models.inference.ai.azure.com/chat/completions"

MODEL = "gpt-4.1-mini"


def generate_insights(text, intent, github_token):

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Analyze the following document.

    Intent:
    {intent}

    Return:
    - Clean bullet points
    - Short and clear insights

    Document:
    {text[:12000]}
    """

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]