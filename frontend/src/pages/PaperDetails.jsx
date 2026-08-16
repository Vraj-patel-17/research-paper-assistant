import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";

function PaperDetails() {
  const { paperId } = useParams();

  const [paper, setPaper] = useState(null);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [bookmarkLoading, setBookmarkLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPaper() {
      try {
        const [paperData, bookmarks] = await Promise.all([
          api.get(`/papers/${paperId}`),
          api.get("/bookmarks"),
        ]);
        console.log("BOOKMARK RESPONSE:", bookmarks);
        setPaper(paperData);

        const bookmarked = bookmarks.some(
          (bookmark) => bookmark.paper_id === Number(paperId)
        );

        setIsBookmarked(bookmarked);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadPaper();
  }, [paperId]);

  async function handleBookmark() {
    setBookmarkLoading(true);

    try {
      if (isBookmarked) {
        await api.delete(`/bookmarks/${paperId}`);
        setIsBookmarked(false);
      } else {
        await api.post(`/bookmarks/${paperId}`, {});
        setIsBookmarked(true);
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setBookmarkLoading(false);
    }
  }

  if (loading) {
    return <h1>Loading paper...</h1>;
  }

  if (error) {
    return <h1>Error: {error}</h1>;
  }

  return (
    <div>
      <h1>{paper.title}</h1>

      <p>{paper.authors}</p>

      <p>{paper.publication_date}</p>

      <p>{paper.source}</p>

      <button onClick={handleBookmark} disabled={bookmarkLoading}>
        {bookmarkLoading
          ? "Updating..."
          : isBookmarked
            ? "Remove Bookmark"
            : "Bookmark"}
      </button>
    </div>
  );
}

export default PaperDetails;