import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import "./Bookmarks.css";
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
  <div className="bookmarks-page">
    <div className="bookmarks-header">
      <h1>Bookmarks ({papers.length})</h1>
      <p>Your saved research papers</p>
    </div>

    {papers.length === 0 ? (
      <div className="empty-bookmarks">
        <h2>No bookmarks yet</h2>
        <p>You haven't bookmarked any papers yet.</p>

        <Link to="/" className="browse-papers">
          Browse Papers
        </Link>
      </div>
    ) : (
      <div className="bookmark-list">
        {papers.map((paper) => (
          <div className="bookmark-card" key={paper.id}>
            <div className="bookmark-content">
              <h2>
                <Link to={`/papers/${paper.id}`}>
                  {paper.title}
                </Link>
              </h2>

              <p>{paper.authors}</p>

              <p className="bookmark-source">
                {paper.source}
              </p>
            </div>

            <button
              className="remove-bookmark"
              onClick={() => removeBookmark(paper.id)}
            >
              Remove Bookmark
            </button>
          </div>
        ))}
      </div>
    )}
  </div>
);
  
}

export default Bookmarks;