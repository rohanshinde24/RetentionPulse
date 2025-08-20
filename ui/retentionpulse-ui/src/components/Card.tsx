export default function Card({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={
        "rounded-2xl p-[1px] bg-gradient-to-br from-indigo-200/60 via-emerald-200/60 to-blue-200/60 " +
        (className || "")
      }
    >
      <div className="rounded-2xl bg-white/90 backdrop-blur shadow-sm">
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}
