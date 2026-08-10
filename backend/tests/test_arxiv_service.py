from unittest.mock import MagicMock, patch
import httpx
from app.services.arxiv_services import ArxivService
def test_arxiv_search_success():
    xml_response = """
    <?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <id>http://arxiv.org/abs/1234.5678</id>
            <title>  Test Research Paper  </title>
            <summary>  This is a test abstract.  </summary>
            <published>2026-01-01T00:00:00Z</published>

            <author>
                <name>John Doe</name>
            </author>

            <link
                title="pdf"
                href="https://arxiv.org/pdf/1234.5678"
            />

            <category term="cs.AI"/>
        </entry>
    </feed>
    """

    mock_response = MagicMock()
    mock_response.text = xml_response
    mock_response.raise_for_status.return_value = None

    with patch("app.services.arxiv_services.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = (
            mock_response
        )

        service = ArxivService()

        papers = service.search(
            query="machine learning",
            start=0,
            max_results=20,
        )

    assert len(papers) == 1

    paper = papers[0]

    assert paper.external_id == "1234.5678"
    assert paper.title == "Test Research Paper"
    assert paper.abstract == "This is a test abstract."
    assert paper.authors == ["John Doe"]
    assert str(paper.pdf_url) == "https://arxiv.org/pdf/1234.5678"
    assert paper.categories == ["cs.AI"]

def test_arxiv_search_http_failure():
    with patch("app.services.arxiv_services.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.side_effect = (
            httpx.RequestError("arXiv unavailable")
        )

        service = ArxivService()

        try:
            service.search("machine learning")
            assert False, "Expected RequestError"
        except httpx.RequestError:
            pass

def test_arxiv_search_http_status_error():
    mock_response = MagicMock()

    request = httpx.Request(
        "GET",
        "https://export.arxiv.org/api/query",
    )

    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Internal Server Error",
        request=request,
        response=httpx.Response(500, request=request),
    )

    with patch("app.services.arxiv_services.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = (
            mock_response
        )

        service = ArxivService()

        try:
            service.search("machine learning")
            assert False, "Expected HTTPStatusError"
        except httpx.HTTPStatusError:
            pass

def test_arxiv_search_empty_result():
    xml_response = """
    <?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
    </feed>
    """

    mock_response = MagicMock()
    mock_response.text = xml_response
    mock_response.raise_for_status.return_value = None

    with patch("app.services.arxiv_services.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = (
            mock_response
        )

        service = ArxivService()

        papers = service.search("something_that_does_not_exist")

    assert papers == []