import { cn } from "../../lib/utils";

function Skeleton({ className }) {
  return (
    <div
      aria-hidden="true"
      className={cn("animate-pulse rounded-md bg-muted", className)}
    />
  );
}

export default Skeleton;