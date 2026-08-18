import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Link } from "react-router-dom";

function Dashboard() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [offset, setOffset] = useState(0);
  const [hasNext, setHasNext] = useState(false);

  const [search, setSearch] = useState("");
  const [query, setQuery] = useState("");

  const [sort, setSort] = useState("latest");

  const limit = 20;

  useEffect(() => {
  const timer = setTimeout(() => {
    const value = search.trim();

    if (value.length === 1) {
      return;
    }

    setOffset(0);
    setQuery(value);
  }, 400);

  return () => clearTimeout(timer);
}, [search]);

  useEffect(() => {
    async function loadPapers() {
      setLoading(true);
      setError("");

      try {
        const params = new URLSearchParams();

        params.set("limit", limit);
        params.set("offset", offset);
        params.set("sort", sort);

        if (query) {
          params.set("q", query);
        }

        const data = await api.get(`/papers?${params.toString()}`);

        setPapers(data.items);
        setHasNext(data.has_next);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadPapers();
  }, [offset, query, sort]);

 


  function handleSort(event) {
    setSort(event.target.value);
    setOffset(0);
  }

  function handleNext() {
    if (hasNext) {
      setOffset(offset + limit);
    }
  }

  function handlePrevious() {
    if (offset > 0) {
      setOffset(offset - limit);
    }
  }


  if (error) {
    return <h1>Error: {error}</h1>;
  }

  return (
    <div>
      <h1>Research Papers</h1>

      <input
            type="text"
            placeholder="Search papers..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />

      <select value={sort} onChange={handleSort}>
        <option value="latest">Latest</option>
        <option value="oldest">Oldest</option>
        <option value="title">Title</option>
      </select>
      {loading && <p>Loading papers...</p>}
      {papers.length === 0 ? (
        <p>No papers found.</p>
      ) : (
        papers.map((paper) => (
          <div key={paper.id}>
            <h2>
              <Link to={`/papers/${paper.id}`}>
                {paper.title}
              </Link>
            </h2>

            <p>{paper.authors}</p>
            <p>{paper.publication_date}</p>
            <p>{paper.source}</p>
          </div>
        ))
      )}

      <div>
        <button
          onClick={handlePrevious}
          disabled={offset === 0}
        >
          Previous
        </button>

        <span>
          {" "} Page {offset / limit + 1} {" "}
        </span>

        <button
          onClick={handleNext}
          disabled={!hasNext}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default Dashboard;