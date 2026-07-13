from app.core.config import settings
def build_summary_prompt(title: str, full_text: str) -> str:
    return f"""
    You are an expert research assistant.

    Summarize the following research paper.

    Title:
    {title}

    Paper:
    {full_text}

    Your summary should:

    1. Explain the research problem.
    2. Explain the proposed approach.
    3. Mention the important results.
    4. Mention why this paper matters.
    5. Use simple, clear English.
    6. Keep the summary under {settings.SUMMARY_MAX_WORDS} words.

    Return only the summary.
    """
@staticmethod
def build_chat_prompt(question:str,context:str) ->str:
    return f"""
    You are an expert AI research assistant.

    Use ONLY the provided paper context to answer the user's question.

    If the answer cannot be found in the provided context, say:

    "I couldn't find the answer in the provided paper."

    Do not invent information.
    Do not use outside knowledge.

    Paper Context:
    {context}

    User Question:
    {question}

    Answer:
    """.strip()