def convert_chat_to_markdown(messages):
    md_lines = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            md_lines.append(f"**You:**\n{content}\n")
        elif role == "assistant":
            md_lines.append(f"**Assistant:**\n{content}\n")
        else:
            md_lines.append(f"**{role.capitalize()}:**\n{content}\n")
    return "\n---\n".join(md_lines)
