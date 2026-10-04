import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import {
  ArrowLeft,
  Bookmark,
  BookOpen,
  ExternalLink,
  MessageSquare,
  Sparkles,
  StickyNote,
} from "lucide-react";
import { api } from "../api/client";
import useMediaQuery from "../hooks/useMediaQuery";
import { cn } from "../lib/utils";
import PaperSummary from "../components/PaperSummary";
import PaperChat from "../components/PaperChat";
import PaperNotes from "../components/PaperNotes";
import Button from "../components/ui/Button";
import Skeleton from "../components/ui/Skeleton";
import Tabs from "../components/ui/Tabs";

const MOBILE_TABS = [
  { id: "paper", label: "Paper", icon: BookOpen },
  { id: "assistant", label: "Assistant", icon: Sparkles },
];

function getPdfEmbedUrl(url) {
  if (!url) return null;
  return url.replace("/abs/", "/pdf/");
}

function PaperDetails() {
  const { paperId } = useParams();
  const isDesktop = useMediaQuery("(min-width: 1024px)");

  const [paper, setPaper] = useState(null);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [actionError, setActionError] = useState("");
  const [bookmarkLoading, setBookmarkLoading] = useState(false);

  const [tab, setTab] = useState("chat");
  const [mobileView, setMobileView] = useState("paper");
  const [noteCount, setNoteCount] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function loadPaper() {
      try {
        const [paperData, bookmarks] = await Promise.all([
          api.get(`/papers/${paperId}`),
          api.get("/bookmarks"),
        ]);

        if (cancelled) return;

        setPaper(paperData);
        setIsBookmarked(
          bookmarks.some((bookmark) => bookmark.paper_id === String(paperId))
        );
      } catch (err) {
        if (!cancelled) setLoadError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadPaper();
    return () => {
      cancelled = true;
    };
  }, [paperId]);

  async function handleBookmark() {
    setBookmarkLoading(true);
    setActionError("");

    try {
      if (isBookmarked) {
        await api.delete(`/bookmarks/${paperId}`);
        setIsBookmarked(false);
      } else {
        await api.post(`/bookmarks/${paperId}`, {});
        setIsBookmarked(true);
      }
    } catch (err) {
      setActionError(err.message);
    } finally {
      setBookmarkLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="space-y-4 p-6">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-8 w-2/3" />
        <Skeleton className="h-4 w-1/3" />
        <Skeleton className="mt-6 h-[60vh] w-full" />
      </div>
    );
  }

  if (loadError || !paper) {
    return (
      <div className="mx-auto max-w-md px-4 py-20 text-center">
        <p className="font-medium">
          {loadError ? `Couldn't load paper: ${loadError}` : "Paper not found."}
        </p>
        <Link to="/" className="mt-4 inline-block text-primary hover:underline">
          Back to papers
        </Link>
      </div>
    );
  }

  const authors = Array.isArray(paper.authors)
    ? paper.authors.join(", ")
    : paper.authors;

  const assistantTabs = [
    { id: "chat", label: "Chat", icon: MessageSquare },
    { id: "overview", label: "Overview", icon: Sparkles },
    { id: "notes", label: "Notes", icon: StickyNote, badge: noteCount },
  ];

  const reader = (
    <div className="flex h-full flex-col bg-muted/40">
      <div className="flex items-center justify-between border-b border-border px-4 py-2">
        <span className="flex items-center gap-2 text-sm font-medium">
          <BookOpen size={16} />
          Paper
        </span>
        {paper.pdf_url && (
          <a
            href={paper.pdf_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-primary"
          >
            Open in new tab
            <ExternalLink size={12} />
          </a>
        )}
      </div>

      {paper.pdf_url ? (
        <iframe
          src={getPdfEmbedUrl(paper.pdf_url)}
          title={`${paper.title} PDF`}
          className="min-h-0 w-full flex-1 border-0 bg-white"
        />
      ) : (
        <div className="flex flex-1 items-center justify-center p-6 text-sm text-muted-foreground">
          No PDF available for this paper.
        </div>
      )}
    </div>
  );

  const assistant = (
    <div className="flex h-full flex-col bg-background">
      <Tabs
        tabs={assistantTabs}
        value={tab}
        onChange={setTab}
        layoutId="assistant-tab-underline"
        className="px-2"
      />

      <div className="min-h-0 flex-1">
        <div className={cn("h-full", tab !== "chat" && "hidden")}>
          <PaperChat paperId={paper.id} />
        </div>

        <div
          className={cn(
            "h-full space-y-4 overflow-y-auto p-4",
            tab !== "overview" && "hidden"
          )}
        >
          {paper.abstract && (
            <section className="rounded-xl border border-border bg-card p-5">
              <h2 className="mb-2 text-base font-semibold">Abstract</h2>
              <p className="text-sm leading-relaxed text-muted-foreground">
                {paper.abstract}
              </p>
            </section>
          )}
          <PaperSummary paperId={paper.id} />
        </div>

        <div
          className={cn(
            "h-full overflow-y-auto p-4",
            tab !== "notes" && "hidden"
          )}
        >
          <PaperNotes paperId={paper.id} onCountChange={setNoteCount} />
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex h-[calc(100vh-3.5rem)] flex-col">
      <header className="border-b border-border px-4 py-3 sm:px-6">
        <Link
          to="/"
          className="mb-2 inline-flex items-center gap-1 text-sm text-muted-foreground transition-colors hover:text-primary"
        >
          <ArrowLeft size={14} />
          Back to papers
        </Link>

        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h1 className="line-clamp-2 text-lg font-semibold leading-snug sm:text-xl">
              {paper.title}
            </h1>
            <p className="mt-1 line-clamp-1 text-sm text-muted-foreground">
              {authors}
            </p>
            <div className="mt-1 flex flex-wrap gap-x-4 text-xs text-muted-foreground">
              <span>Published {paper.publication_date}</span>
              <span>{paper.source}</span>
            </div>
          </div>

          <Button
            variant={isBookmarked ? "primary" : "outline"}
            size="icon"
            onClick={handleBookmark}
            disabled={bookmarkLoading}
            aria-pressed={isBookmarked}
            aria-label={isBookmarked ? "Remove bookmark" : "Add bookmark"}
            title={isBookmarked ? "Remove bookmark" : "Add bookmark"}
          >
            <Bookmark
              size={18}
              fill={isBookmarked ? "currentColor" : "none"}
              strokeWidth={2}
            />
          </Button>
        </div>

        {actionError && (
          <p role="alert" className="mt-2 text-sm text-destructive">
            {actionError}
          </p>
        )}
      </header>

      {isDesktop ? (
        <div className="min-h-0 flex-1">
          <PanelGroup direction="horizontal" autoSaveId="reader-layout">
            <Panel defaultSize={58} minSize={30}>
              {reader}
            </Panel>
            <PanelResizeHandle className="w-1.5 bg-border transition-colors hover:bg-primary/60 data-[resize-handle-state=drag]:bg-primary" />
            <Panel defaultSize={42} minSize={28}>
              {assistant}
            </Panel>
          </PanelGroup>
        </div>
      ) : (
        <>
          <Tabs
            tabs={MOBILE_TABS}
            value={mobileView}
            onChange={setMobileView}
            layoutId="mobile-view-underline"
            className="px-2"
          />
          <div className="min-h-0 flex-1">
            <div className={cn("h-full", mobileView !== "paper" && "hidden")}>
              {reader}
            </div>
            <div className={cn("h-full", mobileView !== "assistant" && "hidden")}>
              {assistant}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default PaperDetails;