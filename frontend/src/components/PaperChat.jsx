import { useState } from 'react';
import { api } from '../api/client.js';
import './PaperChat.css';

function PaperChat({ paperId }) {
  const [messages, setMessages] = useState([]); // { id, role, text }
  const [draft, setDraft] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendQuestion = async (question) => {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    const userMessage = { id: crypto.randomUUID(), role: 'user', text: trimmed };
    setMessages((prev) => [...prev, userMessage]);
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
    sendQuestion(draft);
    setDraft('');
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  return (
    <section className="paper-chat">
      <div className="paper-chat-messages">
        {messages.length === 0 && (
          <p className="paper-chat-empty">
            Ask something about this paper — a method, a result, a term
            you don't recognize.
          </p>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={
              message.role === 'user'
                ? 'paper-chat-bubble paper-chat-bubble-user'
                : 'paper-chat-bubble paper-chat-bubble-assistant'
            }
          >
            {message.text}
          </div>
        ))}

        {loading && (
          <div
            className="paper-chat-bubble paper-chat-bubble-assistant paper-chat-typing"
            aria-live="polite"
          >
            <span className="paper-chat-dot" />
            <span className="paper-chat-dot" />
            <span className="paper-chat-dot" />
          </div>
        )}

        {error && (
          <div className="paper-chat-error">
            {error}
            <button type="button" onClick={() => sendQuestion(draft || messages.at(-1)?.text)}>
              Retry
            </button>
          </div>
        )}
      </div>

      <form className="paper-chat-composer" onSubmit={handleSubmit}>
        <textarea
          className="paper-chat-input"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about this paper"
          rows={2}
          disabled={loading}
        />
        <button
          type="submit"
          className="paper-chat-send-btn"
          disabled={loading || !draft.trim()}
        >
          Ask
        </button>
      </form>
    </section>
  );
}

export default PaperChat;