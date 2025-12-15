import json
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()  

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = OpenAI(
    api_key=GEMINI_API_KEY, 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

System_prompt = """
You are an expert AI assistant. You solve problems using a strict Chain of Thought process.
Your goal is to reach the answer step-by-step.

RULES:
1. You must output a SINGLE JSON object representing the CURRENT step.
2. Do not output multiple steps in one response.
3. After generating a JSON, stop immediately.
4. Format: {"phase": "START" or "PLAN" or "OUTPUT", "content": "..."}
5. "START": Echo the question.
6. "PLAN": A single reasoning step.
7. "OUTPUT": The final answer.
"""

def get_next_step(messages_history):
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=messages_history,
        temperature=0.2, 
        response_format={"type": "json_object"} 
    )
    return response.choices[0].message.content

print("Enter your question:")
user_input = input()

messages = [
    {"role": "system", "content": System_prompt},
    {"role": "user", "content": user_input}
]

step_count = 0
max_steps = 10 

print("\n--- AI Thinking Process ---\n")

while step_count < max_steps:
    raw_response = get_next_step(messages)
    
    try:
        step_data = json.loads(raw_response)
        phase = step_data.get("phase")
        content = step_data.get("content")
        
        print(f"[{phase}]: {content}")
        
        messages.append({"role": "assistant", "content": raw_response})
        
        if phase == "OUTPUT":
            print("\nDONE.")
            break
            
        step_count += 1
        
    except json.JSONDecodeError:
        print(f"Error parsing JSON: {raw_response}")
        break