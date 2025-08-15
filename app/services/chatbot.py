
from openai import OpenAI
from pypdf import PdfReader
import json
from app.core.config import settings
from .tools import record_user_details, record_unknown_question

# Load files
# reader = PdfReader("app/data/linkedin.pdf")
# linkedin = "".join(page.extract_text() or "" for page in reader.pages)

with open("app/data/website_data.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "XYZ Fitness"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s About Us, Workouts, Schedule, FAQ, Testimonials and contact information. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s various workout offerings and other details such as About Us, Contact Us, Testimonials, FAQ, Schedule etc. \
Be professional and engaging, as if talking to a potential client or future investor who came across the website. \
Do not make up information that is not in the summary. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to business. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. If the user is asking for directions ask them to contact the address provided in contact us section "

system_prompt += f"\n\n## Summary:\n{summary}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=settings.DEEPSEEK_BASEURL)

# JSON tool definitions
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}
record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        if tool_name == "record_user_details":
            result = record_user_details(**arguments)
        elif tool_name == "record_unknown_question":
            result = record_unknown_question(**arguments)
        results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
    return results

def chat(message: str, history: list):
    #history = []
    system = system_prompt
    if "patent" in message.lower():
        system += "\n\n## Note: strictly reply in a one liner"

    messages = [{"role": "system", "content": system}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:
        response = client.chat.completions.create(model="deepseek-chat", messages=messages, tools=tools)
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "tool_calls":
            message_obj = response.choices[0].message
            tool_calls = message_obj.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message_obj)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content
