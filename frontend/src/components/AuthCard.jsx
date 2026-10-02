import { motion as Motion } from "framer-motion";
import { BookOpen } from "lucide-react";

function AuthCard({ title, subtitle, footer, children }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/40 px-4 py-10">
      <Motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="w-full max-w-sm rounded-2xl border border-border bg-card p-8 shadow-xl"
      >
        <div className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-11 w-11 items-center justify-center rounded-xl bg-accent text-primary">
            <BookOpen size={22} />
          </div>
          <h1 className="text-2xl font-bold">{title}</h1>
          <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
        </div>

        {children}

        <p className="mt-6 text-center text-sm text-muted-foreground">
          {footer}
        </p>
      </Motion.div>
    </div>
  );
}

export default AuthCard;