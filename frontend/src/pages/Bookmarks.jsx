import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";

function Bookmarks() {
  const [bookmarks, setBookmarks] = useState([]);
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadBookmarks() {
      try {
        const bookmarkData = await api.get("/bookmarks");

        setBookmarks(bookmarkData);

        const paperData = await Promise.all(
          bookmarkData.map((bookmark) =>
            api.get(`/papers/${bookmark.paper_id}`)
          )
        );

        setPapers(paperData);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadBookmarks();
  }, []);

  async function removeBookmark(paperId) {
    try {
      await api.delete(`/bookmarks/${paperId}`);

      setBookmarks((current) =>
        current.filter((bookmark) => bookmark.paper_id !== paperId)
      );

      setPapers((current) =>
        current.filter((paper) => paper.id !== paperId)
      );
    } catch (error) {
      setError(error.message);
    }
  }

  if (loading) {
    return <h1>Loading bookmarks...</h1>;
  }

  if (error) {
    return <h1>Error: {error}</h1>;
  }

  return (
    <div>
      <h1>Bookmarks ({papers.length})</h1>

      {papers.length === 0 ? (
        <p>You haven't bookmarked any papers yet.</p>
      ) : (
        papers.map((paper) => (
          <div key={paper.id}>
            <h2>
              <Link to={`/papers/${paper.id}`}>
                {paper.title}
              </Link>
            </h2>

            <p>{paper.authors}</p>

            <button onClick={() => removeBookmark(paper.id)}>
              Remove Bookmark
            </button>
          </div>
        ))
      )}
    </div>
  );    
}

export default Bookmarks;