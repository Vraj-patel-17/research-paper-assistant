import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { motion as Motion } from "framer-motion";
import { Calendar, ChevronLeft, ChevronRight, Search, X } from "lucide-react";
import { api } from "../api/client";
import { cn } from "../lib/utils";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import Skeleton from "../components/ui/Skeleton";

const LIMIT = 20;
const MIN_QUERY_LENGTH = 2;

function Dashboard() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState("");

  const [offset, setOffset] = useState(0);
  const [hasNext, setHasNext] = useState(false);

  const [search, setSearch] = useState("");
  const [query, setQuery] = useState("");

  const [sort, setSort] = useState("latest");
  const [reloadKey, setReloadKey] = useState(0);

  const requestId = useRef(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      const value = search.trim();
      const next = value.length >= MIN_QUERY_LENGTH ? value : "";

      setQuery((prev) => (prev === next ? prev : next));
      setOffset(0);
    }, 400);

    return () => clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    const id = ++requestId.current;

    async function loadPapers() {
      setFetching(true);
      setError("");

      try {
        const params = new URLSearchParams({
          limit: String(LIMIT),
          offset: String(offset),
          sort,
        });

        if (query) {
          params.set("q", query);
        }

        const data = await api.get(`/papers?${params.toString()}`);

        if (id !== requestId.current) return;

        setPapers(data.items);
        setHasNext(data.has_next);
      } catch (err) {
        if (id !== requestId.current) return;
        setError(err.message);
      } finally {
        if (id === requestId.current) {
          setLoading(false);
          setFetching(false);
        }
      }
    }

    loadPapers();
  }, [offset, query, sort, reloadKey]);

  function handleSort(event) {
    setSort(event.target.value);
    setOffset(0);
  }

  function handleNext() {
    if (hasNext) setOffset(offset + LIMIT);
  }

  function handlePrevious() {
    if (offset > 0) setOffset(Math.max(0, offset - LIMIT));
  }

  function handleRetry() {
    setReloadKey((key) => key + 1);
  }

  return (
    <div className="mx-auto w-full max-w-5xl px-4 pb-12 pt-8 sm:px-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Research Papers</h1>
        <p className="mt-1 text-muted-foreground">
          Discover and explore research papers.
        </p>

        <div className="mt-6 flex flex-col gap-3 sm:flex-row">
          <div className="relative flex-1">
            <label htmlFor="paper-search" className="sr-only">
              Search papers
            </label>
            <Search
              size={16}
              className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
            />
            <Input
              id="paper-search"
              type="text"
              placeholder="Search papers..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              className="pl-9 pr-9"
            />
            {search && (
              <button
                type="button"
                onClick={() => setSearch("")}
                aria-label="Clear search"
                className="absolute right-2 top-1/2 -translate-y-1/2 cursor-pointer rounded p-1 text-muted-foreground transition-colors hover:text-foreground"
              >
                <X size={16} />
              </button>
            )}
          </div>

          <label htmlFor="paper-sort" className="sr-only">
            Sort papers
          </label>
          <select
            id="paper-sort"
            value={sort}
            onChange={handleSort}
            className="h-10 cursor-pointer rounded-lg border border-border bg-background px-3 text-sm focus-visible:outline-2 focus-visible:outline-ring"
          >
            <option value="latest">Latest</option>
            <option value="oldest">Oldest</option>
            <option value="title">Title</option>
          </select>
        </div>
      </div>

      {error && (
        <div
          role="alert"
          className="mb-4 flex items-center justify-between gap-3 rounded-lg border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive"
        >
          <span>Couldn't load papers: {error}</span>
          <Button variant="outline" size="sm" onClick={handleRetry}>
            Retry
          </Button>
        </div>
      )}

      {loading ? (
        <div className="flex flex-col gap-3" aria-busy="true">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : papers.length === 0 && !error ? (
        <p className="py-16 text-center text-muted-foreground">
          {query ? `No papers found for "${query}".` : "No papers found."}
        </p>
      ) : (
        <div
          className={cn(
            "flex flex-col gap-3 transition-opacity",
            fetching && "opacity-60"
          )}
        >
          {papers.map((paper, index) => {
            const authors = Array.isArray(paper.authors)
              ? paper.authors.join(", ")
              : paper.authors;

            return (
              <Motion.div
                key={paper.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: Math.min(index, 8) * 0.04 }}
                whileHover={{ y: -2 }}
              >
                <Link
                  to={`/papers/${paper.id}`}
                  className="group block rounded-xl border border-border bg-card p-5 transition-shadow hover:border-primary/50 hover:shadow-lg"
                >
                  <h2 className="mb-2 line-clamp-2 text-lg font-semibold leading-snug transition-colors group-hover:text-primary">
                    {paper.title}
                  </h2>
                  <p className="mb-3 line-clamp-1 text-sm text-muted-foreground">
                    {authors}
                  </p>
                  <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                    <span className="inline-flex items-center gap-1">
                      <Calendar size={12} />
                      {paper.publication_date
                        ? new Date(paper.publication_date).toLocaleDateString(
                            undefined,
                            { year: "numeric", month: "short", day: "numeric" }
                          )
                        : "—"}
                    </span>
                    <span className="rounded-full bg-accent px-2 py-0.5 text-primary">
                      {paper.source}
                    </span>
                  </div>
                </Link>
              </Motion.div>
            );
          })}
        </div>
      )}

      {!loading && papers.length > 0 && (
        <div className="mt-8 flex items-center justify-center gap-4">
          <Button variant="outline" size="sm" onClick={handlePrevious} disabled={offset === 0}>
            <ChevronLeft size={16} />
            Previous
          </Button>

          <span className="text-sm text-muted-foreground">
            Page {offset / LIMIT + 1}
          </span>

          <Button variant="outline" size="sm" onClick={handleNext} disabled={!hasNext}>
            Next
            <ChevronRight size={16} />
          </Button>
        </div>
      )}
    </div>
  );
}

export default Dashboard;