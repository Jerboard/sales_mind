from openai.types.chat import (
    ChatCompletionMessageParam,           # общий union
    ChatCompletionSystemMessageParam,     # "system"
    ChatCompletionUserMessageParam,       # "user"
    ChatCompletionAssistantMessageParam,  # "assistant"
    ChatCompletionToolMessageParam,       # "tool"
)
from datetime import datetime

import db
from init import client_openai
from settings import log_error


async def ask_gpt(prompt: db.Prompt, history: list[db.Message], user_prompt: str) -> tuple[str, dict]:
    try:
        time_start = datetime.now()
        format_prompt = (
            'При ответе форматируй текст. Для форматирования используй строго HTML-теги Telegram Bot API: <b> (жирный);'
            ' <i> (курсив); <u> (подчёркнутый); <s> (зачёркнутый); '
            '<code> (монострочный); <pre> (блок кода); <a href="URL">…</a> (ссылка); '
            '<span class="tg-spoiler">…</span> (спойлер). '
            'Любые другие теги и любая Markdown-разметка запрещены — удаляй их. Используй эмодзи')
        # основной промпт
        messages = [
            ChatCompletionSystemMessageParam(
                role='system',
                content=f'{format_prompt}\n\n{prompt.role}\n\n{prompt.prompt}'
                # content=f'{prompt.role}\n\n{prompt.prompt}\n\nОтвечай использую разметку html для телеграм, не забывай про емодзи'
            )]

        # добавляем историю
        for m in history:
            messages.append(
                ChatCompletionUserMessageParam(
                    role="user",
                    content=m.request,  # текст запроса, который отправил пользователь
                )
            )
            messages.append(
                ChatCompletionAssistantMessageParam(
                    role="assistant",
                    content=m.response,  # полный ответ модели на этот запрос
                )
            )

        # добавляем текущий запрос
        messages.append(
            ChatCompletionUserMessageParam(
                role="user",
                content=user_prompt
            )
        )

        # for i in messages:
        #     print(i)

        response = await client_openai.chat.completions.create(
            model=prompt.model,
            temperature=prompt.temperature,
            presence_penalty=prompt.presence_penalty,
            frequency_penalty=prompt.frequency_penalty,
            timeout=30,
            messages=messages
        )

        usage = response.usage.dict()
        usage['time_answer'] = str(datetime.now() - time_start)

        return response.choices[0].message.content, usage

    except Exception as e:
        log_error(e)

'''
<bound method BaseModel.json of CompletionUsage(completion_tokens=418, prompt_tokens=31, total_tokens=449, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0))>
'''