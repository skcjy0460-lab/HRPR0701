from openai import OpenAI

client = OpenAI()

# claude-haiku 테스트
for model in ["claude-haiku-4-5", "gemini-3-flash-preview"]:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "안녕하세요. 한 문장으로 답해주세요."}],
            max_tokens=100
        )
        content = resp.choices[0].message.content if resp.choices else None
        print(f"Model {model}: content={content}")
    except Exception as e:
        print(f"Model {model} error: {e}")
