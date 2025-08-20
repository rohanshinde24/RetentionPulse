function HealthBadge({ status }: { status?: string }) {
  const ok = status === "ok";
  return (
    <div
      className={
        "inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm " +
        (ok ? "bg-emerald-100 text-emerald-800" : "bg-rose-100 text-rose-800")
      }
    >
      <span className="relative flex h-2 w-2">
        <span
          className={
            "animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 " +
            (ok ? "bg-emerald-500" : "bg-rose-500")
          }
        />
        <span
          className={
            "relative inline-flex h-2 w-2 rounded-full " +
            (ok ? "bg-emerald-600" : "bg-rose-600")
          }
        />
      </span>
      API: {status || "checking"}
    </div>
  );
}

export default HealthBadge;
