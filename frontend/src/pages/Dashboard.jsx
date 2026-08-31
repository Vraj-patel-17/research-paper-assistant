import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import { Link } from "react-router-dom";
import "./Dashboard.css";

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

  // Fetch papers
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

        // Ignore results from a superseded request
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
  }, [offset, query, sort]);

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
    setError("");
    setOffset((prev) => prev); // no-op trigger; see note below
    // simplest reliable retry: bump requestId-independent state
    setSort((prev) => prev);
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1 className="dashboard-title">Research Papers</h1>
        <p className="dashboard-subtitle">
          Discover and explore research papers.
        </p>

        <div className="dashboard-controls">
          <div className="search-wrapper">
            <label htmlFor="paper-search" className="sr-only">
              Search papers
            </label>
            <input
              id="paper-search"
              className="dashboard-search"
              type="text"
              placeholder="Search papers..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />

            {search && (
              <button
                className="search-clear"
                onClick={() => setSearch("")}
                aria-label="Clear search"
                type="button"
              >
                ×
              </button>
            )}
          </div>

          <label htmlFor="paper-sort" className="sr-only">
            Sort papers
          </label>
          <select
            id="paper-sort"
            className="dashboard-sort"
            value={sort}
            onChange={handleSort}
          >
            <option value="latest">Latest</option>
            <option value="oldest">Oldest</option>
            <option value="title">Title</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="dashboard-error" role="alert">
          <span>Couldn't load papers: {error}</span>
          <button type="button" onClick={handleRetry}>
            Retry
          </button>
        </div>
      )}

      {loading ? (
        <div className="paper-list" aria-busy="true">
          {Array.from({ length: 4 }).map((_, i) => (
            <div className="paper-card paper-card-skeleton" key={i} />
          ))}
        </div>
      ) : papers.length === 0 && !error ? (
        <p className="dashboard-empty">
          {query
            ? `No papers found for "${query}".`
            : "No papers found."}
        </p>
      ) : (
        <div className={`paper-list${fetching ? " is-fetching" : ""}`}>
          {papers.map((paper) => (
            <Link to={`/papers/${paper.id}`} className="paper-card" key={paper.id}>
              <h2 className="paper-title">{paper.title}</h2>

              <div className="paper-meta">
                <span>
                  {Array.isArray(paper.authors)
                    ? paper.authors.join(", ")
                    : paper.authors}
                </span>
                <span>
                  {paper.publication_date
                    ? new Date(paper.publication_date).toLocaleDateString(
                        undefined,
                        { year: "numeric", month: "short", day: "numeric" }
                      )
                    : "—"}
                </span>
                <span>{paper.source}</span>
                </div>
                </Link>
            
          ))}
          </div>
      )}

      {!loading && papers.length > 0 && (
        <div className="pagination">
          <button onClick={handlePrevious} disabled={offset === 0}>
            Previous
          </button>

          <span className="pagination-page">
            Page {offset / LIMIT + 1}
          </span>

          <button onClick={handleNext} disabled={!hasNext}>
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default Dashboard;