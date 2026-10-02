import { cn } from "../../lib/utils";

const variants = {
  primary: "bg-primary text-primary-foreground hover:opacity-90",
  outline: "border border-border bg-transparent hover:bg-accent hover:text-primary",
  ghost: "bg-transparent hover:bg-accent hover:text-primary",
  destructive: "bg-transparent text-destructive hover:bg-destructive/10",
};

const sizes = {
  sm: "h-8 px-3 text-sm",
  md: "h-10 px-4 text-sm",
  icon: "h-9 w-9",
};

function Button({
  variant = "primary",
  size = "md",
  type = "button",
  className,
  ...props
}) {
  return (
    <button
      type={type}
      className={cn(
        "inline-flex cursor-pointer items-center justify-center gap-2 rounded-lg font-medium transition-colors",
        "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
        "disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    />
  );
}

export default Button;