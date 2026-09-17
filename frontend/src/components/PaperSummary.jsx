import { useState } from 'react';
import { api } from '../api/client.js';
import './PaperSummary.css';

function PaperSummary({ paperId }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get(`/papers/${paperId}/summary`);
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
      const data = await api.post(`/papers/${paperId}/summary/regenerate`);
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

      {loading && !summary && (
        <div className="summary-loading">Generating summary...</div>
      )}

      {error && (
        <div className="summary-error">
          {error}
          <button onClick={retry}>Retry</button>
        </div>
      )}

      {summary && <p className="summary-text">{summary}</p>}
    </section>
  );
}

export default PaperSummary;