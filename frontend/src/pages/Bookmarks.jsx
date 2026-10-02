import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AnimatePresence, motion as Motion } from "framer-motion";
import { Bookmark } from "lucide-react";
import { api } from "../api/client";
import Button from "../components/ui/Button";
import Skeleton from "../components/ui/Skeleton";

function Bookmarks() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [removingIds, setRemovingIds] = useState(new Set());

  useEffect(() => {
    async function loadBookmarks() {
      try {
        const bookmarkData = await api.get("/bookmarks");

        const paperData = await Promise.all(
          bookmarkData.map((bookmark) =>
            api.get(`/papers/${bookmark.paper_id}`)
          )
        );

        setPapers(paperData);
      } catch (err) {
        setError(err.message);
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
      setPapers((current) => current.filter((paper) => paper.id !== paperId));
    } catch (err) {
      setError(err.message);
    } finally {
      setRemovingIds((current) => {
        const next = new Set(current);
        next.delete(paperId);
        return next;
      });
    }
  }

  return (
    <div className="mx-auto w-full max-w-4xl px-4 pb-12 pt-8 sm:px-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">
          Bookmarks{!loading && ` (${papers.length})`}
        </h1>
        <p className="mt-1 text-muted-foreground">Your saved research papers</p>
      </div>

      {error && (
        <p
          role="alert"
          className="mb-4 rounded-lg border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive"
        >
          {error}
        </p>
      )}

      {loading ? (
        <div className="flex flex-col gap-3" aria-busy="true">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : papers.length === 0 ? (
        <div className="rounded-xl border border-border px-6 py-14 text-center">
          <div className="mx-auto mb-3 flex h-11 w-11 items-center justify-center rounded-full bg-accent text-primary">
            <Bookmark size={20} />
          </div>
          <h2 className="mb-1 text-lg font-semibold">No bookmarks yet</h2>
          <p className="mb-5 text-sm text-muted-foreground">
            You haven't bookmarked any papers yet.
          </p>
          <Link
            to="/"
            className="inline-block rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
          >
            Browse papers
          </Link>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          <AnimatePresence mode="popLayout">
            {papers.map((paper) => (
              <Motion.div
                key={paper.id}
                layout
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -24 }}
                transition={{ duration: 0.2 }}
                className="flex items-center justify-between gap-4 rounded-xl border border-border bg-card p-5"
              >
                <div className="min-w-0">
                  <h2 className="mb-1 line-clamp-2 text-lg font-semibold leading-snug">
                    <Link
                      to={`/papers/${paper.id}`}
                      className="transition-colors hover:text-primary"
                    >
                      {paper.title}
                    </Link>
                  </h2>
                  <p className="line-clamp-1 text-sm text-muted-foreground">
                    {Array.isArray(paper.authors)
                      ? paper.authors.join(", ")
                      : paper.authors}
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {paper.source}
                  </p>
                </div>

                <Button
                  variant="primary"
                  size="icon"
                  onClick={() => removeBookmark(paper.id)}
                  disabled={removingIds.has(paper.id)}
                  aria-pressed="true"
                  aria-label="Remove bookmark"
                  title="Remove bookmark"
                  className="shrink-0"
                >
                  <Bookmark size={18} fill="currentColor" strokeWidth={2} />
                </Button>
              </Motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}

export default Bookmarks;