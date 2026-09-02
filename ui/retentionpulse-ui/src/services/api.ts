export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export type CustomerData = {
  gender: string; SeniorCitizen: number; Partner: "Yes" | "No"; Dependents: "Yes" | "No";
  tenure: number; PhoneService: "Yes" | "No"; MultipleLines: string; InternetService: "DSL" | "Fiber optic" | "No";
  OnlineSecurity: string; OnlineBackup: string; DeviceProtection: string; TechSupport: string;
  StreamingTV: string; StreamingMovies: string; Contract: "Month-to-month" | "One year" | "Two year";
  PaperlessBilling: "Yes" | "No"; PaymentMethod: string; MonthlyCharges: number; TotalCharges: number;
};
export type Prediction = { prediction: string; churn_probability: number; threshold: number };
export type ShapFeature = { name: string; abs_shap: number; shap: number };
export type CustomerSummary = { customer_id: string; gender: string; tenure: number; contract: string; internet_service: string; monthly_charges: number; churn_probability: number | null; prediction: string | null; risk_category: "Low" | "Medium" | "High" | null };
export type CustomerDetail = CustomerSummary & { attributes: CustomerData };
export type Dashboard = { total_customers: number; observed_churn_rate: number; scored_customers: number; average_risk: number | null; high_risk_customers: number };
export type UploadResult = { total_rows: number; successful_rows: number; failed_rows: number; predictions: Array<Prediction & { row: number }>; errors: Array<{ row: number; message: string }> };

export class ApiError extends Error { constructor(message: string, public status?: number) { super(message); } }
async function request<T>(path: string, init?: RequestInit): Promise<T> { const response = await fetch(`${API_BASE}${path}`, init); const body = await response.json().catch(() => null); if (!response.ok) throw new ApiError(body?.error?.message || body?.detail || "The service could not complete that request.", response.status); return body as T; }
export const api = {
  health: () => request<{ status: string; customer_count: number }>("/health"), dashboard: () => request<Dashboard>("/dashboard"),
  customers: (params: URLSearchParams) => request<{ items: CustomerSummary[]; total: number; page: number; page_size: number }>(`/customers?${params}`),
  customer: (id: string) => request<CustomerDetail>(`/customers/${id}`), explanation: (id: string) => request<{ customer: CustomerDetail; top_features: ShapFeature[] }>(`/customers/${id}/explain`),
  predict: (data: CustomerData) => request<Prediction>("/predict", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
  explain: (data: CustomerData) => request<{ top_features: ShapFeature[] }>("/explain?top_k=5", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
  upload: (csv: string) => request<UploadResult>("/predict/upload", { method: "POST", headers: { "Content-Type": "text/csv" }, body: csv }), templateUrl: `${API_BASE}/csv-template`,
};
