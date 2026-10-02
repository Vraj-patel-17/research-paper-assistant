import { useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { api } from '../api/client.js';
import { cn } from '../lib/utils';
import Button from './ui/Button';
import Skeleton from './ui/Skeleton';
import Markdown from './Markdown';

function PaperSummary({ paperId }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const run = async (request) => {
    setLoading(true);
    setError(null);
    try {
      const data = await request();
      setSummary(data.summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = () => run(() => api.get(`/papers/${paperId}/summary`));
  const regenerateSummary = () =>
    run(() => api.post(`/papers/${paperId}/summary/regenerate`));

  const retry = summary ? regenerateSummary : fetchSummary;

  return (
    <section className="rounded-xl border border-border bg-card p-5">
      <div className="mb-3 flex items-center justify-between gap-4">
        <h2 className="text-base font-semibold">AI Summary</h2>
        {summary && (
          <Button
            variant="outline"
            size="sm"
            onClick={regenerateSummary}
            disabled={loading}
          >
            <RefreshCw size={14} className={cn(loading && 'animate-spin')} />
            {loading ? 'Regenerating' : 'Regenerate'}
          </Button>
        )}
      </div>

      {!summary && !loading && !error && (
        <Button onClick={fetchSummary}>Summarize paper</Button>
      )}

      {loading && (
        <div role="status" aria-live="polite" className="space-y-2.5">
          <p className="text-sm text-muted-foreground">
            {summary ? 'Regenerating summary…' : 'Generating summary…'}
          </p>
          <Skeleton className="h-3 w-full" />
          <Skeleton className="h-3 w-full" />
          <Skeleton className="h-3 w-5/6" />
          <Skeleton className="h-3 w-3/5" />
        </div>
      )}

      {error && !loading && (
        <div role="alert" className="flex items-center gap-3 text-sm text-destructive">
          <span>{error}</span>
          <Button variant="outline" size="sm" onClick={retry}>
            Retry
          </Button>
        </div>
      )}

      {summary && !loading && <Markdown>{summary}</Markdown>}
    </section>
  );
}

export default PaperSummary;