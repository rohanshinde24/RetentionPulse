function PredictionBadge({ value }: { value?: string }) {
  const cls =
    value === "Churn"
      ? "bg-rose-100 text-rose-800"
      : value === "No Churn"
      ? "bg-emerald-100 text-emerald-800"
      : "bg-gray-100 text-gray-700";
  return (
    <span
      className={
        "inline-flex items-center px-3 py-1 rounded-full text-sm " + cls
      }
    >
      {value ?? "Awaiting prediction"}
    </span>
  );
}

export default PredictionBadge;
