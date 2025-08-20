import Gauge from "./Gauge";
import PredictionBadge from "./PredictionBadge";
import ShapBars from "./ShapBars";

type Prediction = {
  prediction: string;
  churn_probability: number;
  threshold: number;
} | null;
type Explain = {
  top_features?: { name: string; abs_shap: number; shap: number }[];
  error?: string;
} | null;

export default function ResultsPanel({
  pred,
  exp,
  decisionThreshold,
}: {
  pred: Prediction;
  exp: Explain;
  decisionThreshold?: number;
}) {
  const prob =
    typeof pred?.churn_probability === "number" &&
    Number.isFinite(pred.churn_probability)
      ? pred!.churn_probability
      : null;
  const percent = prob !== null ? Math.round(prob * 100) : null;
  const label = prob !== null ? `${(prob * 100).toFixed(1)}%` : "—";

  return (
    <section className="bg-white rounded-2xl shadow p-5">
      <h2 className="text-lg font-medium mb-4">Results</h2>

      <div className="border rounded-xl p-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600">Decision threshold</div>
          <div className="text-sm font-medium">
            {pred?.threshold ?? decisionThreshold ?? 0.5}
          </div>
        </div>
        <div className="mt-2">
          <div className="text-sm text-gray-600">Churn probability</div>
          <Gauge percent={percent} />
          <div className="mt-1 text-sm font-semibold">{label}</div>
        </div>
        <div className="mt-2">
          <PredictionBadge value={pred?.prediction} />
        </div>
      </div>

      <div className="border rounded-xl p-4">
        <div className="text-sm text-gray-600 mb-2">
          Top feature contributions (|SHAP|)
        </div>
        {exp?.error ? (
          <div className="text-sm text-rose-600">{exp.error}</div>
        ) : (
          <ShapBars items={exp?.top_features} />
        )}
      </div>
    </section>
  );
}
