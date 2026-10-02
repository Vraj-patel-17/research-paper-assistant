import { useEffect, useState } from "react";
import { AnimatePresence, motion as Motion } from "framer-motion";
import { Trash2 } from "lucide-react";
import { api } from "../api/client";
import Button from "./ui/Button";
import Skeleton from "./ui/Skeleton";

function PaperNotes({ paperId, onCountChange }) {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadNotes() {
      try {
        const data = await api.get(`/papers/${paperId}/notes`);
        if (!cancelled) setNotes(data ?? []);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadNotes();
    return () => {
      cancelled = true;
    };
  }, [paperId]);

  useEffect(() => {
    onCountChange?.(notes.length);
  }, [notes.length, onCountChange]);

  async function handleAddNote() {
    const trimmed = content.trim();
    if (!trimmed || saving) return;

    setSaving(true);
    setError("");

    try {
      const newNote = await api.post(`/papers/${paperId}/notes`, {
        content: trimmed,
      });
      setNotes((current) => [...current, newNote]);
      setContent("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteNote(noteId) {
    try {
      await api.delete(`/papers/notes/${noteId}`);
      setNotes((current) => current.filter((note) => note.id !== noteId));
    } catch (err) {
      setError(err.message);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      handleAddNote();
    }
  }

  return (
    <section className="space-y-4">
      <div className="overflow-hidden rounded-xl border border-border bg-card">
        <textarea
          value={content}
          onChange={(event) => setContent(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Jot down something about this paper…"
          rows={4}
          className="block w-full resize-y bg-transparent p-3 text-sm placeholder:text-muted-foreground focus-visible:outline-none"
        />
        <div className="flex items-center justify-between border-t border-border px-3 py-2">
          <span className="text-xs text-muted-foreground">Ctrl + Enter to save</span>
          <Button
            size="sm"
            onClick={handleAddNote}
            disabled={saving || !content.trim()}
          >
            {saving ? "Saving…" : "Save note"}
          </Button>
        </div>
      </div>

      {error && (
        <p role="alert" className="text-sm text-destructive">
          {error}
        </p>
      )}

      {loading ? (
        <div className="space-y-2">
          <Skeleton className="h-16 w-full" />
          <Skeleton className="h-16 w-full" />
        </div>
      ) : notes.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          Your notes for this paper will appear here.
        </p>
      ) : (
        <ul className="space-y-2">
          <AnimatePresence initial={false}>
            {notes.map((note) => (
              <Motion.li
                key={note.id}
                layout
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -16 }}
                transition={{ duration: 0.2 }}
                className="flex items-start justify-between gap-3 rounded-lg border border-border bg-card p-3"
              >
                <p className="whitespace-pre-wrap text-sm leading-relaxed">
                  {note.content}
                </p>
                <Button
                  variant="destructive"
                  size="icon"
                  className="h-7 w-7 shrink-0"
                  aria-label="Delete note"
                  onClick={() => handleDeleteNote(note.id)}
                >
                  <Trash2 size={14} />
                </Button>
              </Motion.li>
            ))}
          </AnimatePresence>
        </ul>
      )}
    </section>
  );
}

export default PaperNotes;