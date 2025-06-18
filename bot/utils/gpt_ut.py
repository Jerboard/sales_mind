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
            '⚠️ Форматируй текст строго HTML-тегами, которые поддерживает Telegram Bot API.'
            'Разрешены ТОЛЬКО следующие теги (ничего сверх этого списка):\n'
            '<b>…</b> и <strong>…</strong>          — жирный текст\n'
            '<i>…</i> и <em>…</em>                 — курсив\n  '
            '<u>…</u> и <ins>…</ins>              — подчёркнутый \n '
            '<s>…</s>, <strike>…</strike>, <del>…</del> — зачёркнутый \n '
            '<code>…</code>                       — моноширинный фрагмент в строке \n '
            '<pre>…</pre>                        — блок кода (моноширинный, без переносов) \n '
            '<a href="URL">…</a>                  — гиперссылка  \n'
            '<span class="tg-spoiler">…</span>   — спойлер, скрытый до тапа  \n'
            'Любые другие теги или Markdown-разметка (например `*_#[]()`) ЗАПРЕЩЕНЫ и должны быть удалены.\n'
            'Используй эмодзи в ответах'
        )
        # основной промпт
        messages = [
            ChatCompletionSystemMessageParam(
                role='system',
                content=f'{prompt.role}\n\n{prompt.prompt}\n\n{format_prompt}'
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