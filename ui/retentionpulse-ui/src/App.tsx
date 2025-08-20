// import { useState } from "react";
// import "./App.css";

// function App() {
//   const [formData, setFormData] = useState({
//     tenure: "",
//     monthlyCharges: "",
//     totalCharges: "",
//   });

//   const [prediction, setPrediction] = useState<string | null>(null);
//   const [loading, setLoading] = useState(false);

//   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   // const handleSubmit = async (e: React.FormEvent) => {
//   //   e.preventDefault();
//   //   setLoading(true);
//   //   setPrediction(null);

//   //   // Map frontend keys → backend keys, and cast numbers
//   //   const payload = {
//   //     gender: "Male",
//   //     SeniorCitizen: 0,
//   //     Partner: "Yes",
//   //     Dependents: "No",
//   //     tenure: Number(formData.tenure),
//   //     PhoneService: "Yes",
//   //     MultipleLines: "No",
//   //     InternetService: "DSL",
//   //     OnlineSecurity: "Yes",
//   //     OnlineBackup: "Yes",
//   //     DeviceProtection: "No",
//   //     TechSupport: "Yes",
//   //     StreamingTV: "No",
//   //     StreamingMovies: "No",
//   //     Contract: "One year",
//   //     PaperlessBilling: "Yes",
//   //     PaymentMethod: "Mailed check",
//   //     MonthlyCharges: Number(formData.monthlyCharges),
//   //     TotalCharges: Number(formData.totalCharges),
//   //   };

//   //   try {
//   //     const response = await fetch("http://127.0.0.1:8000/predict", {
//   //       method: "POST",
//   //       headers: { "Content-Type": "application/json" },
//   //       body: JSON.stringify(payload),
//   //     });

//   //     const data = await response.json();
//   //     setPrediction(data.prediction); // adjust if backend returns differently
//   //   } catch (err) {
//   //     console.error("Error calling API:", err);
//   //     setPrediction("Error fetching prediction");
//   //   } finally {
//   //     setLoading(false);
//   //   }
//   // };
//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);
//     setPrediction(null);

//     // ✅ Match backend field names (PascalCase where required)
//     const payload = {
//       gender: "Male", // hardcoded for now
//       SeniorCitizen: 0, // hardcoded
//       Partner: "Yes", // hardcoded
//       Dependents: "No", // hardcoded
//       tenure: Number(formData.tenure),
//       PhoneService: "Yes", // hardcoded
//       MultipleLines: "No", // hardcoded
//       InternetService: "DSL", // hardcoded
//       OnlineSecurity: "Yes", // hardcoded
//       OnlineBackup: "Yes", // hardcoded
//       DeviceProtection: "No", // hardcoded
//       TechSupport: "Yes", // hardcoded
//       StreamingTV: "No", // hardcoded
//       StreamingMovies: "No", // hardcoded
//       Contract: "One year", // hardcoded
//       PaperlessBilling: "Yes", // hardcoded
//       PaymentMethod: "Mailed check", // hardcoded
//       MonthlyCharges: Number(formData.monthlyCharges),
//       TotalCharges: Number(formData.totalCharges),
//     };

//     try {
//       const response = await fetch("http://127.0.0.1:8000/predict", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(payload),
//       });

//       const data = await response.json();
//       setPrediction(data.prediction);
//     } catch (err) {
//       console.error("Error calling API:", err);
//       setPrediction("Error fetching prediction");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
//       <h1 className="text-3xl font-bold mb-6">RetentionPulse Predictor</h1>

//       <form
//         onSubmit={handleSubmit}
//         className="bg-white p-6 rounded-xl shadow-md w-96 space-y-4"
//       >
//         <div>
//           <label className="block text-sm font-medium">Tenure</label>
//           <input
//             type="number"
//             name="tenure"
//             value={formData.tenure}
//             onChange={handleChange}
//             className="mt-1 block w-full border rounded-md p-2"
//             required
//           />
//         </div>

//         <div>
//           <label className="block text-sm font-medium">Monthly Charges</label>
//           <input
//             type="number"
//             step="0.01"
//             name="monthlyCharges"
//             value={formData.monthlyCharges}
//             onChange={handleChange}
//             className="mt-1 block w-full border rounded-md p-2"
//             required
//           />
//         </div>

//         <div>
//           <label className="block text-sm font-medium">Total Charges</label>
//           <input
//             type="number"
//             step="0.01"
//             name="totalCharges"
//             value={formData.totalCharges}
//             onChange={handleChange}
//             className="mt-1 block w-full border rounded-md p-2"
//             required
//           />
//         </div>

//         <button
//           type="submit"
//           className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
//           disabled={loading}
//         >
//           {loading ? "Predicting..." : "Predict"}
//         </button>
//       </form>

//       {prediction && (
//         <div className="mt-6 p-4 bg-gray-200 rounded-md shadow-md">
//           <p className="text-lg font-semibold">Prediction: {prediction}</p>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;import React, { useEffect, useMemo, useState } from "react";
import React, { useEffect, useMemo, useState } from "react";
import HealthBadge from "./components/HealthBadge";
import FeatureForm from "./components/FeatureForm";
import ResultsPanel from "./components/ResultsPanel";
import FeaturePresets from "./components/FeaturePresets";
import { explain, gatewayHealth, predict } from "./services/api";
import Card from "./components/Card";
import Button from "./components/Button";

// ----------------- Types -----------------
export type YesNo = "Yes" | "No";
export type ContractType = "Month-to-month" | "One year" | "Two year";
export type InternetServiceType = "DSL" | "Fiber optic" | "No";

export interface CustomerData {
  gender: string;
  SeniorCitizen: number; // 0 or 1
  Partner: YesNo;
  Dependents: YesNo;
  tenure: number;
  PhoneService: YesNo;
  MultipleLines: string; // allow "No phone service"
  InternetService: InternetServiceType;
  OnlineSecurity: string;
  OnlineBackup: string;
  DeviceProtection: string;
  TechSupport: string;
  StreamingTV: string;
  StreamingMovies: string;
  Contract: ContractType;
  PaperlessBilling: YesNo;
  PaymentMethod: string;
  MonthlyCharges: number;
  TotalCharges: number;
}

interface PredictionResponse {
  prediction: string;
  churn_probability: number;
  threshold: number;
}

interface ExplainResponse {
  top_features?: { name: string; abs_shap: number; shap: number }[];
  error?: string;
}

// ----------------- Config -----------------
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// ----------------- Defaults -----------------
const defaultCustomer: CustomerData = {
  gender: "Male",
  SeniorCitizen: 0,
  Partner: "Yes",
  Dependents: "No",
  tenure: 24,
  PhoneService: "Yes",
  MultipleLines: "No",
  InternetService: "DSL",
  OnlineSecurity: "Yes",
  OnlineBackup: "Yes",
  DeviceProtection: "No",
  TechSupport: "Yes",
  StreamingTV: "No",
  StreamingMovies: "No",
  Contract: "One year",
  PaperlessBilling: "Yes",
  PaymentMethod: "Mailed check",
  MonthlyCharges: 59.9,
  TotalCharges: 1400.0,
};

// Small helper
const classNames = (...xs: (string | undefined | null | false)[]) =>
  xs.filter(Boolean).join(" ");

// ----------------- Component -----------------
export default function App() {
  const [customer, setCustomer] = useState<CustomerData>(defaultCustomer);
  const [loading, setLoading] = useState(false);
  const [explaining, setExplaining] = useState(false);
  const [pred, setPred] = useState<PredictionResponse | null>(null);
  const [exp, setExp] = useState<ExplainResponse | null>(null);
  const [health, setHealth] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [autoExplain, setAutoExplain] = useState<boolean>(true);

  useEffect(() => {
    gatewayHealth()
      .then(setHealth)
      .catch(() => setHealth({ status: "error" }));
  }, []);

  // inside App component:
  const probRaw = pred?.churn_probability;

  // coerce to number + guard against NaN/Infinity
  const prob = useMemo(() => {
    const n = typeof probRaw === "number" ? probRaw : Number(probRaw);
    return Number.isFinite(n) ? n : null;
  }, [probRaw]);

  const probabilityPct = useMemo(
    () => (prob !== null ? Math.round(prob * 100) : null),
    [prob]
  );
  const probabilityLabel = useMemo(
    () => (prob !== null ? `${(prob * 100).toFixed(1)}%` : "—"),
    [prob]
  );

  async function onPredict() {
    setError(null);
    setPred(null);
    setLoading(true);
    try {
      const j = (await predict(customer)) as PredictionResponse;
      setPred(j);
      if (autoExplain) {
        // brief delay so the UI can show the prediction, then fetch explanation
        setTimeout(() => {
          onExplain();
        }, 250);
      }
    } catch (e: any) {
      setError(e?.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  async function onExplain() {
    setError(null);
    setExp(null);
    setExplaining(true);
    try {
      const j = (await explain(customer, 6)) as ExplainResponse;
      setExp(j);
    } catch (e: any) {
      setError(e?.message || "Explain failed");
    } finally {
      setExplaining(false);
    }
  }

  function update<K extends keyof CustomerData>(key: K, v: CustomerData[K]) {
    setCustomer((c) => ({ ...c, [key]: v }));
  }

  return (
    <div className="min-h-screen text-gray-900">
      <header className="sticky top-0 z-10 bg-white/70 backdrop-blur-md border-b">
        <div className="mx-auto max-w-6xl px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl sm:text-2xl font-semibold tracking-tight">
            RetentionPulse — Churn Scoring
          </h1>
          <HealthBadge status={health?.status} />
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <section>
          <Card>
            <h2 className="text-lg font-medium mb-4">Customer Features</h2>
            <div className="mb-4">
              <FeaturePresets
                onApply={(patch) => setCustomer((c) => ({ ...c, ...patch }))}
              />
            </div>
            <FeatureForm value={customer} onChange={setCustomer} />

            <div className="mt-5 flex flex-wrap items-center gap-3">
              <Button onClick={onPredict} disabled={loading}>
                {loading ? "Scoring..." : "Predict churn"}
              </Button>
              <Button
                onClick={onExplain}
                disabled={explaining}
                variant="secondary"
              >
                {explaining ? "Explaining..." : "Explain (Top-6)"}
              </Button>
              <label className="flex items-center gap-2 text-sm ml-1">
                <input
                  type="checkbox"
                  checked={autoExplain}
                  onChange={(e) => setAutoExplain(e.target.checked)}
                />
                Auto‑explain after predict
              </label>
              <Button
                variant="secondary"
                onClick={() => {
                  setCustomer(defaultCustomer);
                  setPred(null);
                  setExp(null);
                  setError(null);
                }}
              >
                Reset
              </Button>
            </div>

            {error && <p className="mt-3 text-sm text-rose-600">{error}</p>}
          </Card>
        </section>

        <ResultsPanel
          pred={pred}
          exp={exp}
          decisionThreshold={health?.decision_threshold}
        />
      </main>

      <footer className="mx-auto max-w-6xl px-4 py-8 text-xs text-gray-500">
        <div>
          API Base: <code>{API_BASE}</code>
        </div>
        {error && <div className="mt-2 text-rose-600">Error: {error}</div>}
      </footer>
    </div>
  );
}

// ----------------- UI primitives -----------------
function Label({
  htmlFor,
  children,
}: {
  htmlFor?: string;
  children: React.ReactNode;
}) {
  return (
    <label
      htmlFor={htmlFor}
      className="block text-sm font-medium text-gray-700 mb-1"
    >
      {children}
    </label>
  );
}

function Text({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
}) {
  const id = useMemo(() => `t-${label.replace(/\s+/g, "-")}`, [label]);
  return (
    <div>
      <Label htmlFor={id}>{label}</Label>
      <input
        id={id}
        className="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

// function Number({
//   label,
//   value,
//   onChange,
//   step = 1,
//   min,
// }: {
//   label: string;
//   value: number;
//   onChange: (v: number) => void;
//   step?: number;
//   min?: number;
// }) {
//   const id = useMemo(() => `n-${label.replace(/\s+/g, "-")}`, [label]);
//   return (
//     <div>
//       <Label htmlFor={id}>{label}</Label>
//       <input
//         id={id}
//         type="number"
//         step={step}
//         min={min}
//         className="w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
//         value={Number.isFinite(value) ? value : 0}
//         onChange={(e) => onChange(Number(e.target.value))}
//       />
//     </div>
//   );
// }

// function Select({
//   label,
//   value,
//   onChange,
//   options,
// }: {
//   label: string;
//   value: string;
//   onChange: (v: string) => void;
//   options: string[];
// }) {
//   const id = useMemo(() => `s-${label.replace(/\s+/g, "-")}`, [label]);
//   return (
//     <div>
//       <Label htmlFor={id}>{label}</Label>
//       <select
//         id={id}
//         className="w-full rounded-xl border border-gray-300 px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
//         value={value}
//         onChange={(e) => onChange(e.target.value)}
//       >
//         {options.map((o) => (
//           <option key={o} value={o}>
//             {o}
//           </option>
//         ))}
//       </select>
//     </div>
//   );
// }
