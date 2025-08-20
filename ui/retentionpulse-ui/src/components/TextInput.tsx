import { useMemo } from "react";

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
      className="block text-sm font-medium text-gray-700 mb-2"
    >
      {children}
    </label>
  );
}

function TextInput({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  const id = useMemo(() => `t-${label.replace(/\s+/g, "-")}`, [label]);
  return (
    <div>
      <Label htmlFor={id}>{label}</Label>
      <div className="rounded-xl border border-gray-300 bg-white focus-within:ring-2 focus-within:ring-indigo-500">
        <input
          id={id}
          placeholder={placeholder}
          className="w-full rounded-xl px-3 py-2 border-0 bg-transparent focus:outline-none focus:ring-0"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      </div>
    </div>
  );
}

export default TextInput;
