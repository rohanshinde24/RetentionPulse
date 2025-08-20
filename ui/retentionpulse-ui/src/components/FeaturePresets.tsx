import { CustomerData } from "./FeatureForm";

type Preset = { name: string; values: Partial<CustomerData> };

const PRESETS: Preset[] = [
  {
    name: "New Fiber User",
    values: {
      tenure: 2,
      InternetService: "Fiber optic",
      Contract: "Month-to-month",
      MonthlyCharges: 89.0,
      TotalCharges: 178.0,
      PaperlessBilling: "Yes",
    },
  },
  {
    name: "Loyal DSL",
    values: {
      tenure: 48,
      InternetService: "DSL",
      Contract: "Two year",
      MonthlyCharges: 45.0,
      TotalCharges: 2100.0,
      PaperlessBilling: "No",
    },
  },
  {
    name: "No Internet",
    values: {
      InternetService: "No",
      OnlineSecurity: "No internet service",
      OnlineBackup: "No internet service",
      DeviceProtection: "No internet service",
      TechSupport: "No internet service",
      StreamingTV: "No internet service",
      StreamingMovies: "No internet service",
    },
  },
];

export default function FeaturePresets({
  onApply,
}: {
  onApply: (patch: Partial<CustomerData>) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2">
      {PRESETS.map((p) => (
        <button
          key={p.name}
          onClick={() => onApply(p.values)}
          className="px-3 py-1.5 rounded-full text-xs font-medium border bg-white hover:bg-gray-50 shadow-sm"
        >
          {p.name}
        </button>
      ))}
    </div>
  );
}
