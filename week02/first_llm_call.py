import json
import os
from getpass import getpass

from openai import OpenAI

# The key is never written here. It comes from the environment,
# or is asked for at an invisible prompt.
api_key = os.environ.get("OPENROUTER_API_KEY") or getpass("OpenRouter API key: ")

client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

EMAIL_4 = """FW: FW: complaint!!!
mr. tharindu jayasuriya was promised a call back THREE days ago about a
broken blender, invoice LKR 12,750. nothing yet. how urgent does this
have to be before someone actually replies?? this is my third email."""


def build_prompt(email_text):
    """Return the instruction sent to the model for one customer email."""
    return (
        "Read this customer email and reply with ONLY a JSON object, no other "
        "text, with exactly these keys: name, issue, urgency "
        '(urgency is "high", "medium" or "low").\n\n'
        "Email:\n" + email_text
    )


def parse_llm_reply(text):
    """Parse a model reply as JSON, or report that it was unparseable."""
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "unparseable"}


response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": build_prompt(EMAIL_4)}],
)
print(parse_llm_reply(response.choices[0].message.content))
