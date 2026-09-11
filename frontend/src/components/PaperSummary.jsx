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
      setSummary(data.summary); // adjust based on your SummaryResponse shape
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!summary && !loading) {
    return <button onClick={fetchSummary} className="summary-btn">Summarize Paper</button>;
  }
  if (loading) return <div className="summary-loading">Generating summary...</div>;
  if (error) {
    return (
      <div className="summary-error">
        {error}
        <button onClick={fetchSummary}>Retry</button>
      </div>
    );
  }

  
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
    return (
    <section className="paper-summary">
      <div className="summary-header">
        <h2>Summary</h2>

        <button
          onClick={regenerateSummary}
          className="summary-regenerate-btn"
          disabled={loading}
        >
          Regenerate
        </button>
      </div>

      <p className="summary-text">{summary}</p>
    </section>
  );
  }

export default PaperSummary;