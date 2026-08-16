import anthropic

MODEL = "claude-sonnet-5"
MAX_CHARS = 300_000

SYSTEM_PROMPT = (
    "당신은 연구실에서 논문 리뷰를 돕는 보조 연구원입니다. "
    "주어진 논문 텍스트를 읽고 목적, 방법, 결과, 한계, 후속 연구 아이디어를 "
    "한국어로 명확하고 간결하게 정리하세요. 논문에 명시되지 않은 내용은 추측하지 말고 "
    "'논문에 명시되지 않음'이라고 표기하세요."
)

TOOL_SCHEMA = {
    "name": "record_paper_summary",
    "description": "논문의 구조화된 요약을 기록합니다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "논문 제목(원문 또는 추정 제목)"},
            "purpose": {"type": "string", "description": "연구 목적 및 연구 질문"},
            "methods": {"type": "string", "description": "연구 방법론, 데이터, 실험 설계"},
            "results": {"type": "string", "description": "주요 결과 및 발견"},
            "limitations": {"type": "string", "description": "연구의 한계점"},
            "future_ideas": {"type": "string", "description": "후속 연구 아이디어 또는 제안"},
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "핵심 키워드 3~6개",
            },
        },
        "required": [
            "title",
            "purpose",
            "methods",
            "results",
            "limitations",
            "future_ideas",
            "keywords",
        ],
    },
}


def summarize_paper(text: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    truncated = text[:MAX_CHARS]

    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        tools=[TOOL_SCHEMA],
        tool_choice={"type": "tool", "name": "record_paper_summary"},
        messages=[
            {
                "role": "user",
                "content": f"다음 논문 텍스트를 분석해 주세요:\n\n{truncated}",
            }
        ],
    )

    for block in message.content:
        if block.type == "tool_use":
            result = block.input
            for key in ["title", "purpose", "methods", "results", "limitations", "future_ideas"]:
                result.setdefault(key, "논문에 명시되지 않음")
            result.setdefault("keywords", [])
            return result

    raise RuntimeError("Claude로부터 구조화된 응답을 받지 못했습니다.")
