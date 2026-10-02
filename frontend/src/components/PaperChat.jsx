import { useEffect, useRef, useState } from 'react';
import { motion as Motion } from 'framer-motion';
import { Check, Copy, Send, Sparkles } from 'lucide-react';
import { api } from '../api/client.js';
import { cn } from '../lib/utils';
import Button from './ui/Button';
import Markdown from './Markdown';

const SUGGESTIONS = [
  'Summarize the key contributions',
  'What methodology is used?',
  'What are the limitations?',
  'Explain the main result simply',
];

function PaperChat({ paperId }) {
  const [messages, setMessages] = useState([]); // { id, role, text }
  const [draft, setDraft] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copiedId, setCopiedId] = useState(null);

  const lastQuestion = useRef('');
  const scrollRef = useRef(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
  }, [messages, loading, error]);

  const ask = async (question, { addUserMessage = true } = {}) => {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    lastQuestion.current = trimmed;

    if (addUserMessage) {
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: 'user', text: trimmed },
      ]);
    }
    setError(null);
    setLoading(true);

    try {
      const data = await api.post(`/papers/${paperId}/ask`, {
        question: trimmed,
        top_k: 5,
      });
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: 'assistant', text: data.answer },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!draft.trim()) return;
    ask(draft);
    setDraft('');
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  const copyAnswer = async (message) => {
    try {
      await navigator.clipboard.writeText(message.text);
      setCopiedId(message.id);
      setTimeout(() => setCopiedId(null), 1500);
    } catch {
      // Clipboard not available.
    }
  };

  return (
    <section className="flex h-full flex-col">
      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
            <div className="rounded-full bg-accent p-3 text-primary">
              <Sparkles size={22} />
            </div>
            <div>
              <p className="font-medium">Ask anything about this paper</p>
              <p className="text-sm text-muted-foreground">
                Methods, results, or terms you don't recognize.
              </p>
            </div>
            <div className="flex flex-wrap justify-center gap-2">
              {SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => ask(suggestion)}
                  className="cursor-pointer rounded-full border border-border px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:border-primary/50 hover:text-primary"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <Motion.div
            key={message.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className={cn(
              'flex',
              message.role === 'user' ? 'justify-end' : 'justify-start'
            )}
          >
            {message.role === 'user' ? (
              <div className="max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-br-sm bg-primary px-4 py-2.5 text-sm text-primary-foreground">
                {message.text}
              </div>
            ) : (
              <div className="max-w-[92%] rounded-2xl rounded-bl-sm bg-muted px-4 py-3">
                <Markdown>{message.text}</Markdown>
                <div className="mt-2 flex justify-end">
                  <button
                    type="button"
                    onClick={() => copyAnswer(message)}
                    aria-label="Copy answer"
                    className="cursor-pointer text-muted-foreground transition-colors hover:text-primary"
                  >
                    {copiedId === message.id ? (
                      <Check size={14} />
                    ) : (
                      <Copy size={14} />
                    )}
                  </button>
                </div>
              </div>
            )}
          </Motion.div>
        ))}

        {loading && (
          <div
            className="flex w-fit items-center gap-1 rounded-2xl rounded-bl-sm bg-muted px-4 py-3"
            role="status"
            aria-live="polite"
            aria-label="Assistant is typing"
          >
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.3s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.15s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground" />
          </div>
        )}

        {error && (
          <div
            role="alert"
            className="flex items-center gap-3 text-sm text-destructive"
          >
            <span>{error}</span>
            <Button
              variant="outline"
              size="sm"
              onClick={() =>
                ask(lastQuestion.current, { addUserMessage: false })
              }
            >
              Retry
            </Button>
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="flex items-end gap-2 border-t border-border p-3"
      >
        <textarea
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about this paper"
          rows={2}
          disabled={loading}
          className="min-h-10 flex-1 resize-none rounded-lg border border-border bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-2 focus-visible:outline-ring disabled:opacity-60"
        />
        <Button
          type="submit"
          size="icon"
          aria-label="Send question"
          disabled={loading || !draft.trim()}
        >
          <Send size={16} />
        </Button>
      </form>
    </section>
  );
}

export default PaperChat;