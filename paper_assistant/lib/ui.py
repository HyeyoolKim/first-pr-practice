import html

FIELD_META = {
    "purpose": ("목적", "🎯"),
    "methods": ("방법", "🔬"),
    "results": ("결과", "📊"),
    "limitations": ("한계", "⚠️"),
    "future_ideas": ("후속 아이디어", "💡"),
}


def keyword_chips_html(keywords: str) -> str:
    if not keywords:
        return ""
    chips = "".join(
        f'<span class="pa-chip">{html.escape(k.strip())}</span>'
        for k in keywords.split(",")
        if k.strip()
    )
    return chips


def field_block_html(row) -> str:
    parts = []
    for field, (label, icon) in FIELD_META.items():
        value = row[field] or "논문에 명시되지 않음"
        parts.append(
            f'<div class="pa-field-label">{icon} {label}</div>'
            f'<div class="pa-field-text">{html.escape(value)}</div>'
        )
    return "".join(parts)


def build_markdown(row) -> str:
    lines = [f"# {row['title']}", ""]
    for field, (label, icon) in FIELD_META.items():
        lines.append(f"## {icon} {label}")
        lines.append(row[field] or "논문에 명시되지 않음")
        lines.append("")
    if row["keywords"]:
        lines.append(f"**키워드**: {row['keywords']}")
    return "\n".join(lines)
