import Select from "./Select";
import NumberInput from "./NumberInput";
import TextInput from "./TextInput";

type YesNo = "Yes" | "No";
type ContractType = "Month-to-month" | "One year" | "Two year";
type InternetServiceType = "DSL" | "Fiber optic" | "No";

export type CustomerData = {
  gender: string;
  SeniorCitizen: number;
  Partner: YesNo;
  Dependents: YesNo;
  tenure: number;
  PhoneService: YesNo;
  MultipleLines: string;
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
};

export default function FeatureForm({
  value,
  onChange,
}: {
  value: CustomerData;
  onChange: (next: CustomerData) => void;
}) {
  function update<K extends keyof CustomerData>(key: K, v: CustomerData[K]) {
    onChange({ ...value, [key]: v });
  }

  const noInternet = value.InternetService === "No";

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <Select
          label="Gender"
          value={value.gender}
          onChange={(v) => update("gender", v)}
          options={["Male", "Female"]}
        />
        <Select
          label="Senior Citizen"
          value={String(value.SeniorCitizen)}
          onChange={(v) => update("SeniorCitizen", Number(v))}
          options={["0", "1"]}
        />
        <Select
          label="Partner"
          value={value.Partner}
          onChange={(v) => update("Partner", v as YesNo)}
          options={["Yes", "No"]}
        />
        <Select
          label="Dependents"
          value={value.Dependents}
          onChange={(v) => update("Dependents", v as YesNo)}
          options={["Yes", "No"]}
        />
        <NumberInput
          label="Tenure (months)"
          value={value.tenure}
          onChange={(v) => update("tenure", v)}
          min={0}
        />
        <Select
          label="Phone Service"
          value={value.PhoneService}
          onChange={(v) => update("PhoneService", v as YesNo)}
          options={["Yes", "No"]}
        />
        <Select
          label="Multiple Lines"
          value={value.MultipleLines}
          onChange={(v) => update("MultipleLines", v)}
          options={["No", "Yes", "No phone service"]}
          disabled={value.PhoneService === "No"}
        />
        <Select
          label="Internet Service"
          value={value.InternetService}
          onChange={(v) => update("InternetService", v as InternetServiceType)}
          options={["DSL", "Fiber optic", "No"]}
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <Select
          label="Online Security"
          value={value.OnlineSecurity}
          onChange={(v) => update("OnlineSecurity", v)}
          options={["Yes", "No", "No internet service"]}
          disabled={noInternet}
        />
        <Select
          label="Online Backup"
          value={value.OnlineBackup}
          onChange={(v) => update("OnlineBackup", v)}
          options={["Yes", "No", "No internet service"]}
          disabled={noInternet}
        />
        <Select
          label="Device Protection"
          value={value.DeviceProtection}
          onChange={(v) => update("DeviceProtection", v)}
          options={["Yes", "No", "No internet service"]}
          disabled={noInternet}
        />
        <Select
          label="Tech Support"
          value={value.TechSupport}
          onChange={(v) => update("TechSupport", v)}
          options={["Yes", "No", "No internet service"]}
          disabled={noInternet}
        />
        <Select
          label="Streaming TV"
          value={value.StreamingTV}
          onChange={(v) => update("StreamingTV", v)}
          options={["Yes", "No", "No internet service"]}
          disabled={noInternet}
        />
        <Select
          label="Streaming Movies"
          value={value.StreamingMovies}
          onChange={(v) => update("StreamingMovies", v)}
          options={["Yes", "No", "No internet service"]}
          disabled={noInternet}
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <Select
          label="Contract"
          value={value.Contract}
          onChange={(v) => update("Contract", v as ContractType)}
          options={["Month-to-month", "One year", "Two year"]}
        />
        <Select
          label="Paperless Billing"
          value={value.PaperlessBilling}
          onChange={(v) => update("PaperlessBilling", v as YesNo)}
          options={["Yes", "No"]}
        />
        <TextInput
          label="Payment Method"
          value={value.PaymentMethod}
          onChange={(v) => update("PaymentMethod", v)}
        />
        <NumberInput
          label="Monthly Charges ($)"
          value={value.MonthlyCharges}
          onChange={(v) => update("MonthlyCharges", v)}
          step={0.1}
          min={0}
        />
        <NumberInput
          label="Total Charges ($)"
          value={value.TotalCharges}
          onChange={(v) => update("TotalCharges", v)}
          step={0.1}
          min={0}
        />
      </div>
    </div>
  );
}
