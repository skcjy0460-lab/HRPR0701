from openai import OpenAI
import json

client = OpenAI()
try:
    resp = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": "안녕하세요"}],
        max_tokens=100
    )
    print("Response type:", type(resp))
    print("Response:", resp)
    print("Choices:", resp.choices)
    if resp.choices:
        print("Content:", resp.choices[0].message.content)
    else:
        print("No choices returned")
        print("Full response dict:", resp.model_dump())
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
