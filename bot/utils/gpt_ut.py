
import db
from init import client_openai


async def ask_gpt(prompt: db.Prompt, user_prompt: str) -> str:
    response = await client_openai.chat.completions.create(
        model=prompt.model,
        # model=prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        timeout=30
    )
    return response.choices[0].message.content

