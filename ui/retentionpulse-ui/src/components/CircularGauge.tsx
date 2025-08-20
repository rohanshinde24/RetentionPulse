type Props = {
  percent: number | null;
  size?: number; // px
  stroke?: number; // px
  label?: string;
};

export default function CircularGauge({ percent, size = 140, stroke = 12, label }: Props) {
  const pct = Math.min(100, Math.max(0, percent ?? 0));
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const dash = (pct / 100) * circumference;

  return (
    <div className="relative inline-flex flex-col items-center justify-center">
      <svg width={size} height={size} className="rotate-[-90deg]">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#E5E7EB" /* gray-200 */
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#4F46E5" /* indigo-600 */
          strokeLinecap="round"
          strokeWidth={stroke}
          strokeDasharray={`${dash} ${circumference - dash}`}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center flex-col">
        <div className="text-2xl font-semibold">
          {percent !== null ? `${pct}%` : "—"}
        </div>
        {label && <div className="text-xs text-gray-500 mt-0.5">{label}</div>}
      </div>
    </div>
  );
}

