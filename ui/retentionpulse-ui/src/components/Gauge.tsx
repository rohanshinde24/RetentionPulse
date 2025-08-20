function Gauge({ percent }: { percent: number | null }) {
  const width = Math.min(100, Math.max(0, percent ?? 0));
  return (
    <div className="mt-1 h-3 w-full bg-gray-100 rounded-full overflow-hidden">
      <div className="h-3 bg-indigo-600" style={{ width: `${width}%` }} />
    </div>
  );
}

export default Gauge;
