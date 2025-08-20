function NumberInput({
  label,
  value,
  onChange,
  step,
  min,
  placeholder,
}: {
  label: string;
  value: number;
  onChange: (v: number) => void;
  step?: number;
  min?: number;
  placeholder?: string;
}) {
  const id = label.toLowerCase().replace(/\s+/g, "-");
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium mb-2">
        {label}
      </label>
      <div className="rounded-xl border border-gray-300 bg-white focus-within:ring-2 focus-within:ring-indigo-500">
        <input
          id={id}
          type="number"
          step={step}
          min={min}
          className="w-full rounded-xl px-3 py-2 border-0 bg-transparent focus:outline-none focus:ring-0"
          placeholder={placeholder}
          value={Number.isFinite(value) ? value : 0}
          onChange={(e) => onChange(Number(e.target.value))}
        />
      </div>
    </div>
  );
}
export default NumberInput;
