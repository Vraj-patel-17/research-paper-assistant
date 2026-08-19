import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";

function PaperDetails() {
  const { paperId } = useParams();

  const [paper, setPaper] = useState(null);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [bookmarkLoading, setBookmarkLoading] = useState(false);
  const [error, setError] = useState("");
  const [notes, setNotes] = useState([]);
  const [noteContent, setNoteContent] = useState("");
  const [notesLoading, setNotesLoading] = useState(true);
  const [noteSaving, setNoteSaving] = useState(false);
  useEffect(() => {
  async function loadPaper() {
    try {
      const [paperData, bookmarks, notesData] = await Promise.all([
        api.get(`/papers/${paperId}`),
        api.get("/bookmarks"),
        api.get(`/papers/${paperId}/notes`),
      ]);

      setPaper(paperData);
      setNotes(notesData);

      const bookmarked = bookmarks.some(
        (bookmark) => bookmark.paper_id === Number(paperId)
      );

      setIsBookmarked(bookmarked);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
      setNotesLoading(false);
    }
  }

  loadPaper();
}, [paperId]);

  async function handleBookmark() {
    setBookmarkLoading(true);
    setError("");

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
  async function handleAddNote() {
  const content = noteContent.trim();

  if (!content) {
    return;
  }

  setNoteSaving(true);
  setError("");

  try {
    const newNote = await api.post(
      `/papers/${paperId}/notes`,
      { content }
    );

    setNotes((current) => [...current, newNote]);
    setNoteContent("");
  } catch (error) {
    setError(error.message);
  } finally {
    setNoteSaving(false);
  }
}

async function handleDeleteNote(noteId) {
  try {
    await api.delete(`/papers/notes/${noteId}`);

    setNotes((current) =>
      current.filter((note) => note.id !== noteId)
    );
  } catch (error) {
    setError(error.message);
  }
}
  if (loading) {
    return <p>Loading paper...</p>;
  }

  if (error) {
    return (
      <div>
        <p>Error: {error}</p>
        <Link to="/">Back to Papers</Link>
      </div>
    );
  }

  if (!paper) {
    return <p>Paper not found.</p>;
  }

  return (
  <div>
    <Link to="/">← Back to Papers</Link>

    <h1>{paper.title}</h1>

    <p>{paper.authors}</p>

    <p>
      <strong>Published:</strong> {paper.publication_date}
    </p>

    <p>
      <strong>Source:</strong> {paper.source}
    </p>

    {paper.abstract && (
      <div>
        <h2>Abstract</h2>
        <p>{paper.abstract}</p>
      </div>
    )}

    <button onClick={handleBookmark} disabled={bookmarkLoading}>
      {bookmarkLoading
        ? "Updating..."
        : isBookmarked
          ? "Remove Bookmark"
          : "Bookmark"}
    </button>

    <div>
      <h2>Notes</h2>

      <textarea
        placeholder="Write a note about this paper..."
        value={noteContent}
        onChange={(event) => setNoteContent(event.target.value)}
        rows={4}
      />

      <br />

      <button
        onClick={handleAddNote}
        disabled={noteSaving || !noteContent.trim()}
      >
        {noteSaving ? "Saving..." : "Add Note"}
      </button>

      {notesLoading ? (
        <p>Loading notes...</p>
      ) : notes.length === 0 ? (
        <p>No notes yet.</p>
      ) : (
        notes.map((note) => (
          <div key={note.id}>
            <p>{note.content}</p>

            <button onClick={() => handleDeleteNote(note.id)}>
              Delete
            </button>
          </div>
        ))
      )}
    </div>
  </div>
);}

export default PaperDetails;