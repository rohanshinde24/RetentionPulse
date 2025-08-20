function HealthBadge({ status }: { status?: string }) {
  const ok = status === "ok";
  return (
    <div
      className={
        "px-3 py-1 rounded-full text-sm " +
        (ok ? "bg-emerald-100 text-emerald-800" : "bg-rose-100 text-rose-800")
      }
    >
      API: {status || "checking"}
    </div>
  );
}

export default HealthBadge;
