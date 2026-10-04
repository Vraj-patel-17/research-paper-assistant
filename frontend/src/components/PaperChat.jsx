import { useEffect, useRef, useState } from 'react';
import { motion as Motion } from 'framer-motion';
import { Check, Copy, Send, Sparkles, Square } from 'lucide-react';
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

function Sources({ sources }) {
  const byPage = new Map();
  (sources ?? []).forEach((source) => {
    if (source.page && !byPage.has(source.page)) byPage.set(source.page, source);
  });

  const pages = [...byPage.values()].sort((a, b) => a.page - b.page);
  if (pages.length === 0) return null;

  return (
    <div className="mt-2 flex flex-wrap items-center gap-1.5 text-xs text-muted-foreground">
      <span>Sources:</span>
      {pages.map((source) => (
        <span
          key={source.page}
          title={source.snippet}
          className="rounded-full bg-accent px-2 py-0.5 text-primary"
        >
          p.{source.page}
        </span>
      ))}
    </div>
  );
}

function PaperChat({ paperId }) {
  const [messages, setMessages] = useState([]); // { id, role, text, sources? }
  const [draft, setDraft] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [error, setError] = useState(null);
  const [copiedId, setCopiedId] = useState(null);

  const lastQuestion = useRef('');
  const scrollRef = useRef(null);
  const abortRef = useRef(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTo({ top: el.scrollHeight, behavior: loading ? 'auto' : 'smooth' });
  }, [messages, status, error, loading]);

  useEffect(() => () => abortRef.current?.abort(), []);

  const ask = async (question, { addUserMessage = true } = {}) => {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    lastQuestion.current = trimmed;

    const assistantId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      ...(addUserMessage
        ? [{ id: crypto.randomUUID(), role: 'user', text: trimmed }]
        : []),
      { id: assistantId, role: 'assistant', text: '', sources: [] },
    ]);
    setError(null);
    setStatus('');
    setLoading(true);

    const controller = new AbortController();
    abortRef.current = controller;

    const updateAssistant = (updater) =>
      setMessages((prev) =>
        prev.map((message) => (message.id === assistantId ? updater(message) : message))
      );

    try {
      await api.stream(
        `/papers/${paperId}/ask/stream`,
        { question: trimmed, top_k: 5 },
        {
          signal: controller.signal,
          onEvent: (event) => {
            if (event.type === 'status') {
              setStatus(event.message);
            } else if (event.type === 'sources') {
              updateAssistant((message) => ({ ...message, sources: event.sources }));
            } else if (event.type === 'token') {
              updateAssistant((message) => ({ ...message, text: message.text + event.text }));
            } else if (event.type === 'error') {
              throw new Error(event.message);
            }
          },
        }
      );
    } catch (err) {
      if (err.name !== 'AbortError') setError(err.message);
    } finally {
      abortRef.current = null;
      setLoading(false);
      setStatus('');
      // Drop the placeholder if nothing was received (error or early stop).
      setMessages((prev) =>
        prev.filter((message) => !(message.id === assistantId && !message.text))
      );
    }
  };

  const stop = () => abortRef.current?.abort();

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

  const lastId = messages.at(-1)?.id;

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

        {messages.map((message) => {
          const isUser = message.role === 'user';
          const isStreaming = loading && message.id === lastId;

          return (
            <Motion.div
              key={message.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className={cn('flex', isUser ? 'justify-end' : 'justify-start')}
            >
              {isUser ? (
                <div className="max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-br-sm bg-primary px-4 py-2.5 text-sm text-primary-foreground">
                  {message.text}
                </div>
              ) : !message.text ? (
                <div
                  className="flex items-center gap-2 rounded-2xl rounded-bl-sm bg-muted px-4 py-3"
                  role="status"
                  aria-live="polite"
                >
                  <span className="flex items-center gap-1">
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.3s]" />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.15s]" />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground" />
                  </span>
                  {status && (
                    <span className="text-xs text-muted-foreground">{status}</span>
                  )}
                </div>
              ) : (
                <div className="max-w-[92%] rounded-2xl rounded-bl-sm bg-muted px-4 py-3">
                  <Markdown>{message.text}</Markdown>
                  {!isStreaming && (
                    <>
                      <Sources sources={message.sources} />
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
                    </>
                  )}
                </div>
              )}
            </Motion.div>
          );
        })}

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
        {loading ? (
          <Button
            type="button"
            variant="outline"
            size="icon"
            aria-label="Stop generating"
            onClick={stop}
          >
            <Square size={14} fill="currentColor" />
          </Button>
        ) : (
          <Button
            type="submit"
            size="icon"
            aria-label="Send question"
            disabled={!draft.trim()}
          >
            <Send size={16} />
          </Button>
        )}
      </form>
    </section>
  );
}

export default PaperChat;