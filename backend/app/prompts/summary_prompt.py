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
    6. Keep the summary under 300 words.

    Return only the summary.
    """