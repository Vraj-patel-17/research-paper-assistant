import httpx

headers = {
    "User-Agent": "ResearchPaperAssistant/1.0 (your_email@example.com)"
}

with httpx.Client(
    headers=headers,
    follow_redirects=True,
    timeout=30.0,
) as client:
    response = client.get(
        "http://export.arxiv.org/api/query",
        params={
            "search_query": "cat:cs.AI",
            "max_results": 1,
        },
    )

print(response.status_code)
print(response.text[:300])