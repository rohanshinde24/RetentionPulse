import Gauge from "./Gauge";
import CircularGauge from "./CircularGauge";
import PredictionBadge from "./PredictionBadge";
import ShapBars from "./ShapBars";
import Card from "./Card";

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
    <section className="">
      <h2 className="text-lg font-medium mb-4">Results</h2>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
        <Card className="flex items-center justify-center">
          <CircularGauge percent={percent} label="Churn probability" />
        </Card>
        <Card>
          <div className="text-sm text-gray-600">Decision threshold</div>
          <div className="text-xl font-semibold mt-1">{pred?.threshold ?? decisionThreshold ?? 0.5}</div>
        </Card>
        <Card className="flex items-center justify-center">
          <PredictionBadge value={pred?.prediction} />
        </Card>
      </div>

      <Card>
        <div className="text-sm text-gray-600 mb-2">
          Top feature contributions (|SHAP|)
        </div>
        {exp?.error ? (
          <div className="text-sm text-rose-600">{exp.error}</div>
        ) : (
          <ShapBars items={exp?.top_features} />
        )}
      </Card>
    </section>
  );
}
