import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { Bookmark } from "lucide-react";
import "./Bookmarks.css";
function Bookmarks() {
  const [bookmarks, setBookmarks] = useState([]);
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [removingIds, setRemovingIds] = useState(new Set());

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
    setRemovingIds((current) => new Set(current).add(paperId));
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
      setRemovingIds((current) => {
        const next = new Set(current);
        next.delete(paperId);
        return next;
      });
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
          {papers.map((paper) => {
            const isBookmarked = !removingIds.has(paper.id);
            return (
              <div className="bookmark-card" key={paper.id}>
                <div className="bookmark-content">
                  <h2>
                    <Link to={`/papers/${paper.id}`}>{paper.title}</Link>
                  </h2>

                  <p>{paper.authors}</p>

                  <p className="bookmark-source">{paper.source}</p>
                </div>

                <button
                  type="button"
                  className={`bookmark-toggle ${isBookmarked ? "is-active" : ""}`}
                  onClick={() => removeBookmark(paper.id)}
                  aria-pressed={isBookmarked}
                  aria-label={
                    isBookmarked ? "Remove bookmark" : "Add bookmark"
                  }
                  title={isBookmarked ? "Remove bookmark" : "Add bookmark"}
                >
                  <Bookmark
                    size={22}
                    fill={isBookmarked ? "currentColor" : "none"}
                    strokeWidth={2}
                  />
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Bookmarks;