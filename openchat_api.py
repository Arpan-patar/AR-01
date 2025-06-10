from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://openrouter.ai/api/v1"
)

def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you are a helpful ai assistant name AR-zero1."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
