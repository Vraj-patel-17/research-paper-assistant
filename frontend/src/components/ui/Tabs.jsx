import { motion as Motion } from "framer-motion";
import { cn } from "../../lib/utils";

function Tabs({ tabs, value, onChange, layoutId = "tab-underline", className }) {
  return (
    <div
      role="tablist"
      className={cn("flex gap-1 border-b border-border", className)}
    >
      {tabs.map(({ id, label, icon: Icon, badge }) => {
        const active = id === value;

        return (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={active}
            onClick={() => onChange(id)}
            className={cn(
              "relative flex cursor-pointer items-center gap-2 px-3 py-2.5 text-sm font-medium transition-colors",
              active
                ? "text-primary"
                : "text-muted-foreground hover:text-foreground"
            )}
          >
            {Icon && <Icon size={16} />}
            {label}
            {badge ? (
              <span className="rounded-full bg-accent px-1.5 text-xs text-primary">
                {badge}
              </span>
            ) : null}
            {active && (
              <Motion.span
                layoutId={layoutId}
                className="absolute inset-x-0 -bottom-px h-0.5 bg-primary"
              />
            )}
          </button>
        );
      })}
    </div>
  );
}

export default Tabs;