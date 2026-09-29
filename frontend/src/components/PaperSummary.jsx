import { useState } from 'react';
import { api } from '../api/client.js';
import './PaperSummary.css';

const MIN_LOADING_MS = 1200;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function withMinDelay(promise) {
  const [result] = await Promise.all([promise, sleep(MIN_LOADING_MS)]);
  return result;
}

function PaperSummary({ paperId }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await withMinDelay(api.get(`/papers/${paperId}/summary`));
      setSummary(data.summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const regenerateSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await withMinDelay(
        api.post(`/papers/${paperId}/summary/regenerate`)
      );
      setSummary(data.summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const retry = summary ? regenerateSummary : fetchSummary;

  return (
    <section className="paper-summary">
      <div className="summary-header">
        <h2>Summary</h2>
        {summary && (
          <button
            onClick={regenerateSummary}
            className="summary-regenerate-btn"
            disabled={loading}
          >
            {loading ? 'Regenerating...' : 'Regenerate'}
          </button>
        )}
      </div>

      {!summary && !loading && !error && (
        <button onClick={fetchSummary} className="summary-btn">
          Summarize Paper
        </button>
      )}

      {loading && (
        <div className="summary-loading" role="status" aria-live="polite">
          <div className="summary-loading-label">
            <span>{summary ? 'Regenerating summary' : 'Generating summary'}</span>
            <span className="summary-dots" aria-hidden="true">
              <span className="summary-dot" />
              <span className="summary-dot" />
              <span className="summary-dot" />
            </span>
          </div>

          <div className="summary-skeleton" aria-hidden="true">
            <div className="summary-skeleton-line" />
            <div className="summary-skeleton-line" />
            <div className="summary-skeleton-line" />
            <div className="summary-skeleton-line summary-skeleton-line-short" />
          </div>
        </div>
      )}

      {error && !loading && (
        <div className="summary-error">
          {error}
          <button onClick={retry}>Retry</button>
        </div>
      )}

      {summary && !loading && <p className="summary-text">{summary}</p>}
    </section>
  );
}

export default PaperSummary;