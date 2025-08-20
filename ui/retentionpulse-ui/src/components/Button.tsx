export default function Button({
  children,
  onClick,
  disabled,
  variant = "primary",
}: {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "ghost";
}) {
  const base =
    "px-4 py-2 rounded-xl inline-flex items-center gap-2 transition-colors shadow-sm";
  const styles = {
    primary: disabled
      ? "bg-gray-300 text-white"
      : "text-white bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 shadow",
    secondary: "border bg-white hover:bg-gray-50",
    ghost: "text-indigo-700 hover:bg-indigo-50",
  } as const;
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${styles[variant]}`}
    >
      {children}
    </button>
  );
}
